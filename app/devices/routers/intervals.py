from devices.models.intervals import Interval
import uuid
from datetime import datetime
from devices.models.rules import Rule
from devices.commands.devices import DeviceCMD
from devices.enums.rules import RulesPossibleState
from devices.queries.rules import RulesQRS
from devices.commands.rules import RulesCMD
from devices.commands.events import EventsCMD
from devices.commands.intervals import IntervalsCMD
from devices.models.users import User
from devices.schemas.schema import (
    ComponentExpectedState,
    IntervalState,
    RulesComponentsList,
)
from devices.queries.intervals import IntervalsQRS
from fastapi import APIRouter, Depends
from devices.dependencies import get_current_active_user
from devices.service_providers.device_logger import logger

router = APIRouter(
    prefix="/intervals",
    tags=["intervals"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/{interval_id}")
async def get_interval_by_id(
    interval_id: str,
    IntervalsQRS=Depends(IntervalsQRS),
    current_user: User = Depends(get_current_active_user),
):
    return await IntervalsQRS.get_interval(interval_id, current_user)


@router.post("", name="Create set of rules")
async def plan(
    components_rules: RulesComponentsList,
    current_user: User = Depends(get_current_active_user),
):
    """In order to keep device status"""
    logger.info(f"Trying to plan '{components_rules}'")
    intervals, rules = await RulesCMD.form_rules(components_rules, current_user)
    res_rules = []

    for _interval in intervals:
        await IntervalsQRS.create_interval(_interval)

    for _rule in rules:
        rule = await RulesQRS.create_rule(_rule)
        await RulesCMD.enqueue_notify(rule)
        res_rules.append(rule.id)

    return {"rules": res_rules}


@router.put("/{interval_id}/state")
async def change_interval_state(
    interval_id: str,
    interval_state: IntervalState,
    current_user: User = Depends(get_current_active_user),
):
    return await IntervalsQRS.set_interval_state(
        interval_id, interval_state.expected_state, current_user
    )


@router.delete("/{interval_id}")
async def remove_interval(
    interval_id: str,
    state: ComponentExpectedState,
    current_user: User = Depends(get_current_active_user),
):
    interval = await IntervalsCMD.cancel_interval(interval_id, current_user)
    _interval = Interval.parse_obj(
        dict(
            id=uuid.uuid4(),
            device_component_id=interval.device_component_id,
            execution_time=datetime.now(),
            user_id=current_user.id,
        )
    )
    await IntervalsQRS.create_interval(_interval)

    off_rule = Rule.parse_obj(
        dict(
            id=uuid.uuid4(),
            interval_id=_interval.id,
            device_component_id=_interval.device_component_id,
            expected_state=state.expected_state,
            execution_time=datetime.now(),
            state=RulesPossibleState.NEW,
        )
    )
    rule = await RulesQRS.create_rule(off_rule)
    await RulesCMD.enqueue_notify(rule)

    return interval
