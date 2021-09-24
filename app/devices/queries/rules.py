from devices.service_providers.sql_db import psql_db
from devices.service_providers.device_logger import logger
from devices.models.rules import Rule
import uuid


class RulesQRS:
    @staticmethod
    async def create_rule(rule: Rule):
        sql = """
        INSERT INTO rules (
            id, interval_uuid, device_id, actuator_id, expected_state, execution_time, state
        ) VALUES (
            :id, :interval_uuid, :device_id, :actuator_id, :expected_state, :execution_time, :state
        ) RETURNING id, interval_uuid, device_id, actuator_id, expected_state, execution_time, state
        """
        result = await psql_db.fetch_one(
            sql, values=rule.dict()
        )
        
        return Rule.parse_obj(result)

    @staticmethod
    async def get_rule(rule_id: uuid.UUID) -> Rule:
        sql = """SELECT id, interval_uuid, device_id, actuator_id, 
        expected_state, execution_time, state
        FROM rules WHERE id=:rule_id
        """
        result = await psql_db.fetch_one(
            sql, values={'rule_id': rule_id}
        )
        
        return Rule.parse_obj(result)

    @staticmethod
    async def get_last_irrigation_rule() -> Rule:
        sql = """SELECT id, next_rule, device_id, actuator_id, 
        expected_state, execution_time, state
        FROM rules
        WHERE type = 'irrigation' and state = 'new'
        ORDER BY execution_time DESC LIMIT 1
        """
        result = await psql_db.fetch_one(sql)
        return Rule.parse_obj(result)

    @staticmethod
    async def set_rule_state(rule_id, state) -> None:
        sql = """UPDATE rules SET state=:state WHERE id=:rule_id"""
        await psql_db.execute(
            sql, values={'rule_id': rule_id, 'state': state}
        )
