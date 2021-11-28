from devices.service_providers.sql_db import psql_db
from devices.models.rules import Rule, Rules
import uuid


class RulesQRS:
    @staticmethod
    async def create_rule(rule: Rule):
        sql = """
        INSERT INTO rules (
            id, interval_id, device_component_id, expected_state, execution_time, state
        ) VALUES (
            :id, :interval_id, :device_component_id, :expected_state, :execution_time, :state
        ) RETURNING id, interval_id, device_component_id, expected_state, execution_time, state
        """
        result = await psql_db.fetch_one(sql, values=rule.dict(exclude_none=True))
        return Rule.parse_obj(result)

    @staticmethod
    async def get_rule(rule_id: uuid.UUID) -> Rule:
        sql = """SELECT *
        FROM rules
        WHERE id=:rule_id"""

        result = await psql_db.fetch_one(sql, values={"rule_id": rule_id})

        return Rule.parse_obj(result)

    @staticmethod
    async def get_rules_by_interval_id(
        interval_id: uuid.UUID, only_active=False
    ) -> Rule:
        sql = """SELECT *
        FROM rules
        WHERE interval_id=:interval_id
        """

        if only_active:
            sql += " AND execution_time >= now()"

        result = await psql_db.fetch_all(sql, values={"interval_id": interval_id})

        if result is None:
            return None

        return Rules.parse_obj(result)

    @staticmethod
    async def set_rule_state(rule_id, state) -> None:
        sql = """UPDATE rules
        SET state=:state
        WHERE id=:rule_id
        RETURNING id, interval_id, device_component_id, expected_state, execution_time, state
        """
        result = await psql_db.fetch_one(
            sql, values={"rule_id": rule_id, "state": state}
        )
        return Rule.parse_obj(result)
