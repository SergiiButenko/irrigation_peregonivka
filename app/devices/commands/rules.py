from datetime import datetime, timedelta
from devices.config.config import Config
from devices.celery_tasks.tasks import try_execure_rule, try_notify_rule
from devices.queries.devices import DeviceQRS
from devices.commands.devices import DeviceCMD
from devices.enums.rules import DiscreteActuatorsType, DiscreteStates, RulesState
from devices.models.rules import Rule, Rules
from devices.schemas.schema import RulesActuatorsList
import uuid


class RulesCMD:

    @staticmethod
    async def analyse_and_enqueue() -> None:
        pass

    @staticmethod
    async def enqueue_notify(rule: Rule) -> None:
        actuator = await DeviceCMD.get_component_by_id(
            rule.device_id, rule.actuator_id
        )

        if actuator.telegram_notify:
            try_notify_rule.apply_async(
                args=[rule.id],
                eta=rule.execution_time - timedelta(minutes=Config.NOTIFY_MIN_BEFORE),
            )

        try_execure_rule.apply_async(args=[rule.id], eta=rule.execution_time)

    @staticmethod
    async def form_rules(rules: RulesActuatorsList) -> Rules:
        res_rules = []
        execution_time = datetime.now() + timedelta(minutes=rules.minutes_delay)
        for index, actuator in enumerate(rules.actuators):
            interval_uuid = uuid.uuid4()

            _actuator = await DeviceQRS.get_component_by_id(
                actuator.device_id, actuator.actuator_id
            )
            intervals_quantity = actuator.rules.intervals
            time_wait = actuator.rules.time_wait
            execution_minutes = actuator.rules.time

            for interval in range(intervals_quantity):
                if DiscreteActuatorsType.has_value(_actuator.usage_type):
                    on_rule = Rule.parse_obj(
                        dict(
                            id=uuid.uuid4(),
                            interval_uuid=interval_uuid,
                            device_id=actuator.device_id,
                            actuator_id=actuator.actuator_id,
                            expected_state=DiscreteStates.ON,
                            execution_time=execution_time,
                            state=RulesState.NEW,
                        )
                    )
                    res_rules.append(on_rule)

                    execution_time = execution_time + timedelta(
                        minutes=execution_minutes
                    )
                    off_rule = Rule.parse_obj(
                        dict(
                            id=uuid.uuid4(),
                            interval_uuid=interval_uuid,
                            device_id=actuator.device_id,
                            actuator_id=actuator.actuator_id,
                            expected_state=DiscreteStates.OFF,
                            execution_time=execution_time,
                            state=RulesState.NEW,
                        )
                    )
                    res_rules.append(off_rule)
                    execution_time = execution_time + timedelta(minutes=time_wait)

            delta_minutes = index * (execution_minutes * intervals_quantity + time_wait)

            execution_time = execution_time + timedelta(minutes=delta_minutes)

        return res_rules
