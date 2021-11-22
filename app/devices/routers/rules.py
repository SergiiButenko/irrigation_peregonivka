from devices.models.users import User
from devices.schemas.schema import RulesComponentsList, RuleState
from devices.commands.rules import RulesCMD
from devices.queries.rules import RulesQRS
from devices.queries.intervals import IntervalsQRS
from fastapi import APIRouter, Depends
from devices.dependencies import get_current_active_user, get_logger

router = APIRouter(
    prefix="/rules",
    tags=["rules"],
    dependencies=[Depends(get_current_active_user)]
)


@router.post("", name="Create set of rules")
async def plan(
    components_rules: RulesComponentsList,
    RulesCMD=Depends(RulesCMD),
    RulesQRS=Depends(RulesQRS),
    IntervalsQRS=Depends(IntervalsQRS),
    logger=Depends(get_logger),
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

    return {'rules': res_rules}


@router.get("/{rule_id}")
async def get_rule_by_id(
    rule_id: str,
    RulesQRS=Depends(RulesQRS),
    logger=Depends(get_logger),
):
    return await RulesQRS.get_rule(rule_id)


@router.put("/{rule_id}/state")
async def change_rule_state(
    rule_id: str,
    rule_state: RuleState,
    RulesQRS=Depends(RulesQRS),
):
    await RulesQRS.set_rule_state(rule_id, rule_state.expected_state)
    return await RulesQRS.get_rule(rule_id)
