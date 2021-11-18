from datetime import datetime, timedelta
from devices.models.users import User
from devices.config.config import Config
from devices.celery_tasks.tasks import try_execure_rule, try_notify_rule
from devices.queries.devices import DeviceQRS
from devices.enums.rules import DiscreteActuatorsType, DiscreteStates, RulesState
from devices.models.rules import Rule, Rules
from devices.models.intervals import Interval
from devices.schemas.schema import RulesActuatorsIntervalsList
import uuid


class RulesCMD:

    @staticmethod
    async def analyse_and_enqueue() -> None:
        pass

    @staticmethod
    async def enqueue_notify(rule: Rule) -> None:
        actuator = await DeviceQRS.get_component_by_id(
            rule.device_component_id
        )

        if actuator.telegram_notify:
            try_notify_rule.apply_async(
                task_id=str(rule.id),
                args=[rule.id],
                eta=rule.execution_time - timedelta(minutes=Config.NOTIFY_MIN_BEFORE),
            )

        try_execure_rule.apply_async(
            task_id=str(rule.id),
            args=[rule.id],
            eta=rule.execution_time
            )

    @staticmethod
    async def form_rules(rules: RulesActuatorsIntervalsList, current_user: User) -> Rules:
        res_rules = []
        res_intervals = []
        
        execution_time = datetime.now() + timedelta(minutes=rules.minutes_delay)
        for index, actuator in enumerate(rules.actuators):
            interval_id = uuid.uuid4()

            _actuator = await DeviceQRS.get_component_by_device_id(
                actuator.device_id, actuator.actuator_id
            )
            intervals_quantity = actuator.rules.intervals
            time_wait = actuator.rules.time_wait
            execution_minutes = actuator.rules.time

            res_intervals.append(Interval.parse_obj(
                dict(
                    id=interval_id,
                    device_component_id=_actuator.id,
                    execution_time=execution_time,
                    user_id=current_user.id
                )
            ))

            for _ in range(intervals_quantity):
                if DiscreteActuatorsType.has_value(_actuator.usage_type):
                    on_rule = Rule.parse_obj(
                        dict(
                            id=uuid.uuid4(),
                            interval_id=interval_id,
                            device_component_id=_actuator.id,
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
                            interval_id=interval_id,
                            device_component_id=_actuator.id,
                            expected_state=DiscreteStates.OFF,
                            execution_time=execution_time,
                            state=RulesState.NEW,
                        )
                    )
                    res_rules.append(off_rule)
                    execution_time = execution_time + timedelta(minutes=time_wait)

            delta_minutes = index * (execution_minutes * intervals_quantity + time_wait)

            execution_time = execution_time + timedelta(minutes=delta_minutes)

        return res_intervals, res_rules
