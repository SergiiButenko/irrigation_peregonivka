from devices.messages.TelegramMessages import TelegramMessages
from asgiref.sync import async_to_sync
from datetime import datetime

from devices.service_providers.celery import celery_app
from devices.enums.rules import RulesState
from devices.config.config import Config
from devices.clients.devices import DevicesClient


async def execute_rule(rule_id: str) -> None:
    device_client = DevicesClient(Config.SERVICE_USERNAME, Config.SERVICE_PASSWORD)
    await device_client.login()

    rule = await device_client.get_rule(rule_id)

    await device_client.update_rule_state(rule.id, RulesState.IN_PROGRESS)

    await device_client.update_actuator_state(
        rule.device_id, rule.actuator_id, rule.expected_state
    )

    await device_client.update_rule_state(rule.id, RulesState.SUCCESSFUL)


async def notify_rule(rule_id: str) -> None:
    device_client = DevicesClient(Config.SERVICE_USERNAME, Config.SERVICE_PASSWORD)
    await device_client.login()

    rule = await device_client.get_rule(rule_id)
    actuator = await device_client.get_actuator(rule.device_id, rule.actuator_id)

    now = datetime.now()
    diff = rule.execution_time - now
    minutes = int(divmod(diff.total_seconds(), 60)[0]) + 1

    if minutes <= 2:
        if actuator.usage_type == "irrigation":
            message = TelegramMessages.IRRIGATION_PLANNED_NOW.format(actuator.name)
        elif actuator.usage_type == "lighting":
            message = TelegramMessages.LIGHTING_PLANNED_NOW.format(actuator.name)

    elif minutes > 2:
        if actuator.usage_type == "irrigation":
            message = TelegramMessages.IRRIGATION_PLANNED.format(actuator.name, minutes)
        elif actuator.usage_type == "lighting":
            message = TelegramMessages.LIGHTING_PLANNED.format(actuator.name, minutes)

    await device_client.send_message(message)


@celery_app.task()
def try_execure_rule(rule_id: str) -> None:
    async_to_sync(execute_rule)(rule_id)


@celery_app.task()
def try_notify_rule(rule_id: str) -> None:
    async_to_sync(notify_rule)(rule_id)
