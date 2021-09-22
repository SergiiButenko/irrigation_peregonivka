from devices.dependencies import get_sql_db, get_logger
from devices.models.rules import Rule
import uuid
from fastapi import Depends


class RulesQRS:
    def __init__(
        self,
        service_logger=Depends(get_logger),
        psql_db=Depends(get_sql_db),
    ):
        self.service_logger = service_logger
        self.psql_db = psql_db

    async def create_rule(self, rule: Rule) -> None:
        sql = """
        INSERT INTO rules (type, next_rule, device_id, actuator_id, expected_state,
        execution_time, state) VALUES (
            :type, :next_rule, :device_id, :actuator_id, :expected_state, :execution_time, :state
        ) RETURNING id, type, next_rule, device_id, actuator_id, expected_state, execution_time, state
        )
        """
        self.service_logger.info(f"Executing {sql}")
        result = await self.psql_db.execute(
            sql, values=rule.to_dict()
        )

        return Rule.parse_obj(result) 

    async def get_rule(self, rule_id: uuid.UUID) -> Rule:
        sql = """SELECT id, type, next_rule, device_id, actuator_id, 
        expected_state, execution_time, state
        FROM rules WHERE id=:rule_id
        """
        result = await self.psql_db.execute(
            sql, values={'rule_id': rule_id}
        )
        return Rule.parse_obj(result)

    async def get_last_irrigation_rule(self) -> Rule:
        sql = """SELECT id, type, next_rule, device_id, actuator_id, 
        expected_state, execution_time, state
        FROM rules
        WHERE type = 'irrigation' and state = 'new'
        ORDER BY execution_time DESC LIMIT 1
        """
        result = await self.psql_db.fetch_one(sql)
        return Rule.parse_obj(result)
