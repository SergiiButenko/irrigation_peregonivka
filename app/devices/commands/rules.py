from datetime import datetime, timedelta
from devices.commands import intervals
from devices.service_providers.device_logger import logger
from devices.enums.intervals import IntervalPossibleState
from devices.queries.intervals import IntervalsQRS
from devices.queries.rules import RulesQRS
from devices.queries.components import ComponentsQRS
from devices.models.users import User
from devices.config.config import Config
from devices.celery_tasks.tasks import try_execure_rule, try_notify_rule
from devices.enums.rules import (
    DiscreteActuatorsType,
    DiscreteStates,
    RulesPossibleState,
)
from devices.models.rules import Rule, Rules
from devices.models.intervals import Interval
from devices.schemas.schema import RulesComponentsIntervalsList
import uuid


class RulesCMD:
    @staticmethod
    async def set_rule_state(rule_id: str, rule_state: str, user: User) -> None:
        COMPLETED_STATES = [
            RulesPossibleState.COMPLETED,
            RulesPossibleState.ERROR,
            RulesPossibleState.CANCELED,
        ]

        rule = await RulesQRS.set_rule_state(rule_id, rule_state)
        active_interval_rules = await RulesQRS.get_rules_by_interval_id(
            rule.interval_id, only_active=True
        )
        active_interval_rules = active_interval_rules.__root__

        if rule_state == RulesPossibleState.IN_PROGRESS:
            logger.info("Rule is in progress. Updating interval to in_progres")
            return await IntervalsQRS.set_interval_state(
                rule.interval_id, IntervalPossibleState.IN_PROGRESS, user
            )
        elif len(active_interval_rules) > 0 and rule_state in COMPLETED_STATES:
            logger.info(
                "Rule completed. More rules left to execute. Interval state set to in_progress"
            )
            return await IntervalsQRS.set_interval_state(
                rule.interval_id, IntervalPossibleState.IN_PROGRESS, user
            )
        elif len(active_interval_rules) == 0 and rule_state in COMPLETED_STATES:
            logger.info(
                "Rule completed. No more rules left to execute. Interval state set to completed"
            )
            interval_rules = await RulesQRS.get_rules_by_interval_id(rule.interval_id)
            interval_rules = interval_rules.__root__
            logger.info(interval_rules)

            all_error = all(r.state == RulesPossibleState.ERROR for r in interval_rules)
            all_canceled = all(
                r.state == RulesPossibleState.CANCELED for r in interval_rules
            )

            if all_error:
                logger.info("Updating interval to error")
                return await IntervalsQRS.set_interval_state(
                    rule.interval_id, IntervalPossibleState.ERROR, user
                )
            elif all_canceled:
                logger.info("Updating interval to canceled")
                return await IntervalsQRS.set_interval_state(
                    rule.interval_id, IntervalPossibleState.CANCELED, user
                )
            else:
                logger.info("Updating interval to completed")
                return await IntervalsQRS.set_interval_state(
                    rule.interval_id, IntervalPossibleState.COMPLETED, user
                )

        raise Exception("Error during updating rule and interval state")

    @staticmethod
    async def enqueue_notify(rule: Rule) -> None:
        component = await ComponentsQRS.get_component_by_id(rule.device_component_id)

        if component.telegram_notify:
            try_notify_rule.apply_async(
                task_id=str(rule.id),
                args=[rule.id],
                eta=rule.execution_time - timedelta(minutes=Config.NOTIFY_MIN_BEFORE),
            )

        try_execure_rule.apply_async(
            task_id=str(rule.id), args=[rule.id], eta=rule.execution_time
        )

    @staticmethod
    async def form_rules(
        rules: RulesComponentsIntervalsList, current_user: User
    ) -> Rules:
        res_rules = []
        res_intervals = []

        execution_time = datetime.now() + timedelta(minutes=rules.minutes_delay)
        for index, component in enumerate(rules.components):
            interval_id = uuid.uuid4()

            _component = await ComponentsQRS.get_component_by_id(component.component_id)
            intervals_quantity = component.rules.intervals
            time_wait = component.rules.time * 1.5
            execution_minutes = component.rules.time

            res_intervals.append(
                Interval.parse_obj(
                    dict(
                        id=interval_id,
                        device_component_id=_component.id,
                        execution_time=execution_time,
                        user_id=current_user.id,
                    )
                )
            )

            for _ in range(intervals_quantity):
                if DiscreteActuatorsType.has_value(_component.purpose):
                    on_rule = Rule.parse_obj(
                        dict(
                            id=uuid.uuid4(),
                            interval_id=interval_id,
                            device_component_id=_component.id,
                            expected_state=DiscreteStates.ON,
                            execution_time=execution_time,
                            state=RulesPossibleState.NEW,
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
                            device_component_id=_component.id,
                            expected_state=DiscreteStates.OFF,
                            execution_time=execution_time,
                            state=RulesPossibleState.NEW,
                        )
                    )
                    res_rules.append(off_rule)
                    execution_time = execution_time + timedelta(minutes=time_wait)

            delta_minutes = index * (execution_minutes * intervals_quantity + time_wait)

            execution_time = execution_time + timedelta(minutes=delta_minutes)

        return res_intervals, res_rules
