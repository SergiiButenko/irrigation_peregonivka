from devices.service_providers.sql_db import psql_db
from devices.service_providers.device_logger import logger
from devices.models.rules import Rule
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
        result = await psql_db.fetch_one(
            sql, values=rule.dict(exclude_none=True)
        )
        rule = Rule.parse_obj(result)

        return await RulesQRS.get_rule(rule.id)

    @staticmethod
    async def get_rule(rule_id: uuid.UUID) -> Rule:
        sql = """SELECT r.*, c.device_id, c.component_id
        FROM rules r
        JOIN device_components c ON r.device_component_id = c.id
        WHERE r.id=:rule_id"""

        result = await psql_db.fetch_one(
            sql, values={'rule_id': rule_id}
        )

        return Rule.parse_obj(result)

    @staticmethod
    async def set_rule_state(rule_id, state) -> None:
        sql = """UPDATE rules SET state=:state WHERE id=:rule_id"""
        await psql_db.execute(
            sql, values={'rule_id': rule_id, 'state': state}
        )
