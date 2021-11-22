from devices.enums.rules import DiscreteActuatorsType
from devices.models.devices import ComponentSql, ComponentsSql
from devices.schemas.schema import ComponentExpectedState
from devices.service_providers.sql_db import psql_db
from devices.service_providers.device_logger import logger


class ComponentsQRS:

    @staticmethod
    async def get_component_by_id(
        id: str
    ) -> ComponentSql:
        sql = """
        SELECT *
        FROM device_components
        WHERE id=:id;
        """
        result = await psql_db.fetch_one(
            sql, values={"id": id}
        )
        return ComponentSql.parse_obj(result)


    @staticmethod
    async def get_components_by_device_id(
        device_id: str
    ) -> ComponentSql:
        sql = """
        SELECT * 
        FROM device_components
        WHERE device_id=:device_id;
        """
        results = await psql_db.fetch_all(
            sql,
            values={"device_id": device_id}
        )

        return ComponentsSql.parse_obj(results)


    @staticmethod
    async def get_components_by_group_id(group_id: str, user_id: str):
        sql = """SELECT c.* 
        FROM public.device_components AS c
        JOIN public.components_groups AS cg ON c.id = cg.device_component_id
        JOIN public.groups AS g ON g.id = cg.group_id
        WHERE g.user_id=:user_id and g.id=:group_id"""
        result = await psql_db.fetch_all(
            sql, values={'user_id': user_id, 'group_id': group_id}
        )

        return ComponentsSql.parse_obj(result)

    @staticmethod
    async def get_expected_component_state(component_id: str) -> ComponentExpectedState:
        # Get Last executed rule
        sql = """
        SELECT expected_state
        FROM rules
        WHERE device_component_id=:device_component_id
        AND state='completed'
        AND execution_time < now()
        ORDER BY execution_time DESC
        LIMIT 1
        """
        last_executed_rule = await psql_db.fetch_one(
            sql, values={"device_component_id": component_id}
        )

        # Get Next executed rule
        sql = """
        SELECT expected_state
        FROM rules
        WHERE device_component_id=:device_component_id
        AND state='new'
        AND execution_time >= now()
        ORDER BY execution_time ASC
        LIMIT 1
        """
        next_rule = await psql_db.fetch_one(
            sql, values={"device_component_id": component_id}
        )

        component = await ComponentsQRS.get_component_by_id(component_id)
        if last_executed_rule is not None:
            logger.info(ComponentExpectedState.parse_obj(last_executed_rule))
            return ComponentExpectedState.parse_obj(last_executed_rule)

        # if no last rule but next rule exists and components id discrete
        if next_rule and DiscreteActuatorsType.has_value(component.purpose):
            state = ComponentExpectedState.parse_obj(next_rule)
            state.expected_state = 1 - int(state.expected_state)
            return ComponentExpectedState.parse_obj(state)

        # by default return default state
        return ComponentExpectedState.parse_obj(
            {'expected_state': component.default_state}
        )
