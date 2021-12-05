from devices.commands.components import ComponentsCMD
from devices.clients.notification_service import NotificationServiceClient
from devices.models.users import User
from devices.schemas.schema import RuleState
from devices.commands.rules import RulesCMD
from devices.queries.rules import RulesQRS
from fastapi import APIRouter, Depends
from devices.dependencies import get_current_active_user, get_notification_service

router = APIRouter(
    prefix="/rules", tags=["rules"], dependencies=[Depends(get_current_active_user)]
)


@router.get("/{rule_id}")
async def get_rule_by_id(
    rule_id: str,
):
    return await RulesQRS.get_rule(rule_id)


@router.put("/{rule_id}/state")
async def change_rule_state(
    rule_id: str,
    rule_state: RuleState,
    current_user: User = Depends(get_current_active_user),
    notification_service: NotificationServiceClient = Depends(get_notification_service),
):
    await RulesCMD.set_rule_state(rule_id, rule_state.expected_state, current_user)
    rule = await RulesQRS.get_rule(rule_id)
    await notification_service.send_ws_message(
        "actuator_update",
        await ComponentsCMD.get_component_state(rule.device_component_id, current_user),
    )

    return rule
