from devices.service_providers.device_logger import logger
from devices.messages.TelegramMessages import TelegramMessages
from asgiref.sync import async_to_sync
from datetime import datetime

from devices.service_providers.celery import celery_app
from devices.enums.rules import RulesPossibleState
from devices.enums.intervals import IntervalPossibleState
from devices.config.config import Config
from devices.clients.devices import DevicesClient

INTERVAL_BLOCKED_STATE = [IntervalPossibleState.CANCELED]


async def execute_rule(rule_id: str) -> None:
    device_client = DevicesClient(Config.SERVICE_USERNAME, Config.SERVICE_PASSWORD)
    await device_client.login()

    # Analyse if rule is active
    rule = await device_client.get_rule(rule_id)
    interval = await device_client.get_interval(str(rule.interval_id))

    if interval.state in INTERVAL_BLOCKED_STATE:
        logger.warning("Rule is not going to be executed since interval does not allowing it")
        await device_client.update_rule_state(rule.id, RulesPossibleState.CANCELED)
        return
    #####
    await device_client.update_rule_state(rule.id, RulesPossibleState.IN_PROGRESS)

    await device_client.update_component_state(
        rule.device_component_id, rule.expected_state
    )

    await device_client.update_rule_state(rule.id, RulesPossibleState.COMPLETED)


async def notify_rule(rule_id: str) -> None:
    device_client = DevicesClient(Config.SERVICE_USERNAME, Config.SERVICE_PASSWORD)
    await device_client.login()

    # Analyse if rule is active
    rule = await device_client.get_rule(rule_id)
    interval = await device_client.get_interval(str(rule.interval_id))

    if interval.state in INTERVAL_BLOCKED_STATE:
        logger.warning("Rule is not going to be executed since interval does not allowing it")
        return
    #####

    rule = await device_client.get_rule(rule_id)
    component = await device_client.get_component(rule.device_component_id)

    now = datetime.now()
    diff = rule.execution_time - now
    minutes = int(divmod(diff.total_seconds(), 60)[0]) + 1

    if minutes <= 2:
        if component.purpose == "valve":
            message = TelegramMessages.IRRIGATION_PLANNED_NOW.format(component.name)
        elif component.purpose == "switcher":
            message = TelegramMessages.LIGHTING_PLANNED_NOW.format(component.name)

    elif minutes > 2:
        if component.purpose == "valve":
            message = TelegramMessages.IRRIGATION_PLANNED.format(component.name, minutes)
        elif component.purpose == "switcher":
            message = TelegramMessages.LIGHTING_PLANNED.format(component.name, minutes)

    await device_client.send_message(message)


@celery_app.task()
def try_execure_rule(rule_id: str) -> None:
    async_to_sync(execute_rule)(rule_id)


@celery_app.task()
def try_notify_rule(rule_id: str) -> None:
    async_to_sync(notify_rule)(rule_id)
