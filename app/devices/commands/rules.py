from datetime import datetime, timedelta
from devices.config.config import Config
from devices.celery_tasks.tasks import try_execure_rule, try_notify_rule
from devices.queries.devices import DeviceSQL
from fastapi import Depends
from devices.commands.devices import DeviceCMD
from devices.dependencies import get_logger, get_config
from devices.enums.rules import DiscreteActuatorsType, DiscreteStates, RulesState
from devices.models.rules import Rule, Rules
from devices.schemas.schema import RulesActuatorsList
import uuid


class RulesCMD:
    def __init__(
        self,
        deviceCMD: DeviceCMD = Depends(DeviceCMD),
        deviceSQL: DeviceSQL = Depends(DeviceSQL),
        service_logger=Depends(get_logger),
        config=Depends(get_config),
    ):
        self.DeviceCMD = deviceCMD
        self.DeviceSQL = deviceSQL
        self.service_logger = service_logger
        self.config = config

    async def enqueue(self, rule: Rule) -> None:
        return try_execure_rule.apply_async(
            args=[rule.id],
            eta=rule.execution_time
        )

    async def enqueue_notify(self, rule: Rule) -> None:
        try_notify_rule.apply_async(
            args=[rule.id],
            eta=rule.execution_time - timedelta(Config.NOTIFY_MIN_BEFORE)
        )

        self.enqueue(rule)

    async def form_rules(self, rules: RulesActuatorsList) -> Rules:
        res_rules = []
        execution_time = datetime.now() + timedelta(minutes=rules.minutes_delay)
        for index, actuator in enumerate(rules.actuators):
            interval_uuid = uuid.uuid4()
    
            _actuator = await self.DeviceSQL.get_component_by_id(
                actuator.device_id, actuator.actuator_id
            )
            intervals_quantity = actuator.rules.intervals or 1
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
                            state=RulesState.NEW
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
                            state=RulesState.NEW
                        )
                    )
                    res_rules.append(off_rule)
                    execution_time = execution_time + timedelta(
                        minutes=time_wait
                    )

            delta_minutes = index * (
                execution_minutes * intervals_quantity
                + time_wait
            )

            execution_time = execution_time + timedelta(minutes=delta_minutes)

        return res_rules
