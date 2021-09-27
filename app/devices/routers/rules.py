from devices.schemas.schema import RulesActuatorsList, RuleState
from devices.commands.rules import RulesCMD
from devices.queries.rules import RulesQRS
from fastapi import APIRouter, Depends
from devices.dependencies import get_logger

router = APIRouter(
    prefix="/rules",
    tags=["rules"]
)


@router.post("", name="Create set of rules")
async def plan(
    actuators_rules: RulesActuatorsList,
    RulesCMD=Depends(RulesCMD),
    RulesQRS=Depends(RulesQRS),
    logger=Depends(get_logger),
):
    """In order to keep device status"""
    logger.info(f"Trying to plan '{actuators_rules}'")
    rules = await RulesCMD.form_rules(actuators_rules)
    res_rules = []
    
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
    return {'status': 'Completed'}