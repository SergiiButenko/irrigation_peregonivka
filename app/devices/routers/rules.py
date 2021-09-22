from devices.models.devices import RulesActuatorsList
from devices.commands.rules import RulesCMD
from devices.queries.rules import RulesQRS
from fastapi import APIRouter, Depends

from devices.dependencies import get_logger

router = APIRouter(
    prefix="/rules",
    tags=["rules"]
)


@router.post("", name="Create set of rules")
async def get_sensor(
    actuators_rules: RulesActuatorsList,
    RulesCMD=Depends(RulesCMD),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Trying to plan '{actuators_rules}'")

    # rules = RulesCMD.create_rules(actuators_rules)
    # for rule in rules:
    #     await RulesQRS.create_rule(rule)
    return "OK"
