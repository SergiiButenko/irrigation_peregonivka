from devices.messages.TelegramMessages import TelegramMessages
from asgiref.sync import async_to_sync
from datetime import datetime

from devices.service_providers.celery import celery_app
from devices.enums.rules import RulesState
from devices.service_providers.httpx_client import HttpxClient
from devices.config.config import Config
from devices.models.rules import Rule
from devices.models.devices import ComponentSql


async def execute_rule(rule_id: str) -> None:
    _rule = await HttpxClient.get(Config.DEVICES_URL + '/rules/' + rule_id)
    rule = Rule.parse_obj(_rule.json())

    await HttpxClient.put(
        url=f"{Config.DEVICES_URL}/rules/{rule.id}/state",
        json={'expected_state': RulesState.IN_PROGRESS}
        )

    await HttpxClient.put(
        url=f"{Config.DEVICES_URL}/devices/{rule.device_id}/actuators/{rule.actuator_id}/state",
        json={'expected_state': rule.expected_state}
        )

    await HttpxClient.put(
        url=f"{Config.DEVICES_URL}/rules/{rule.id}/state",
        json={'expected_state': RulesState.SUCCESSFUL}
        )


async def notify_rule(rule_id: str) -> None:
    _rule = await HttpxClient.get(Config.DEVICES_URL + '/rules/' + rule_id)
    rule = Rule.parse_obj(_rule.json())

    _actuator = await HttpxClient.get(f"{Config.DEVICES_URL}/devices/{rule.device_id}/actuators/{rule.actuator_id}")
    actuator = ComponentSql.parse_obj(_actuator.json())

    now = datetime.now()
    diff = rule.execution_time - now
    minutes = divmod(diff.total_seconds(), 60)
     
    if minutes <= 2 and actuator.type == 'irrigation':
        message = TelegramMessages.IRRIGATION_PLANNED_NOW.format(actuator.name)
    elif minutes > 2 and actuator.type == 'irrigation':
        message = TelegramMessages.IRRIGATION_PLANNED.format(actuator.name, minutes[0])
    elif minutes <= 2 and actuator.type == 'lighting':
        message = TelegramMessages.LIGHTING_PLANNED_NOW.format(actuator.name)
    elif minutes > 2 and actuator.type == 'lighting':
        message = TelegramMessages.LIGHTING_PLANNED.format(actuator.name, minutes[0])

    await HttpxClient.put(
        url=f"{Config.DEVICES_URL}/telegram/{Config.TELEGRAM_CHAT_ID_COTTAGE}/message",
        json={'message': message}
        )


@celery_app.task(acks_late=True)
def try_execure_rule(rule_id: str) -> None:
    async_to_sync(execute_rule)(rule_id)


@celery_app.task(acks_late=True)
def try_notify_rule(rule_id: str) -> None:
    async_to_sync(notify_rule)(rule_id)
