from devices.schemas.schema import RulesActuatorsList
from devices.commands.rules import RulesCMD
from devices.queries.rules import RulesQRS
from fastapi import APIRouter, Depends
from devices.celery_tasks.tasks import try_execure_rule
from devices.dependencies import get_logger
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/rules",
    tags=["rules"]
)


@router.post("", name="Create set of rules")
async def get_sensor(
    actuators_rules: RulesActuatorsList,
    RulesCMD=Depends(RulesCMD),
    RulesQRS=Depends(RulesQRS),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Trying to plan '{actuators_rules}'")
    rules = await RulesCMD.form_rules(actuators_rules)
    for rule in rules:
        logger.info(rule)
        await RulesQRS.create_rule(rule)
        await RulesCMD.enqueue(rule)

    return {"msg": "Word received"}
