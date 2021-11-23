from devices.enums.intervals import IntervalPossibleState
from devices.enums.rules import RulesPossibleState
from devices.models.rules import DashboardIrrigationRules
from devices.service_providers.sql_db import psql_db
from devices.service_providers.device_logger import logger
from devices.models.intervals import Interval
import uuid


class IntervalsQRS:
    @staticmethod
    async def create_interval(interval: Interval) -> Interval:
        sql = """
        INSERT INTO intervals (
            id, device_component_id, execution_time, user_id
        ) VALUES (
            :id, :device_component_id, :execution_time, :user_id
        ) RETURNING id, device_component_id, execution_time, user_id, state
        """
        result = await psql_db.fetch_one(sql, values=interval.dict(exclude_none=True))

        return Interval.parse_obj(result)

    @staticmethod
    async def get_interval(interval_id: str, user_id: str) -> Interval:
        sql = """SELECT *
        FROM intervals
        WHERE id=:interval_id
        AND user_id=:user_id
        """
        result = await psql_db.fetch_one(
            sql, values={"interval_id": interval_id, "user_id": user_id}
        )

        return Interval.parse_obj(result)

    @staticmethod
    async def get_active_interval_by_component_id(component_id: str, user_id: str) -> Interval:
        sql = """SELECT distinct on (i.id) i.*
        FROM intervals i
        JOIN rules r ON r.interval_id = i.id
        AND r.device_component_id = :component_id
        AND r.state = :rule_state
        AND i.state = :interval_state
        AND r.execution_time > now()
        AND i.user_id = :user_id
        ORDER BY i.id, r.execution_time DESC
        """
        result = await psql_db.fetch_one(
            sql, values={
                "component_id": component_id,
                "user_id": user_id,
                'rule_state': RulesPossibleState.NEW,
                'interval_state': IntervalPossibleState.IN_PROGRESS
                }
        )

        if result is None:
            return None

        return Interval.parse_obj(result)

    @staticmethod
    async def set_interval_state(interval_id, state, user_id: uuid.UUID) -> None:
        sql = """UPDATE intervals
        SET state=:state
        WHERE id=:interval_id
        AND user_id=:user_id
        """
        await psql_db.execute(
            sql, values={"interval_id": interval_id, "state": state, "user_id": user_id}
        )

    @staticmethod
    async def get_next_irrigation_rule(user_id: uuid.UUID) -> DashboardIrrigationRules:
        sql = """SELECT distinct on (i.id) i.*, c.name
        FROM intervals i
        JOIN rules r ON r.interval_id = i.id
        JOIN device_components c ON i.device_component_id = c.id
        WHERE c.purpose = 'valve'
        AND r.state = :state
        AND r.execution_time > now()
        AND i.user_id = :user_id
        ORDER BY i.id, r.execution_time DESC
        """
        results = await psql_db.fetch_all(sql, values={
            "user_id": user_id,
            "state": RulesPossibleState.NEW
            })

        return DashboardIrrigationRules.parse_obj(results)
