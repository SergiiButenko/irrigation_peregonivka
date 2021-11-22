from devices.models.devices import ComponentSql, ComponentsSql
from devices.schemas.schema import ComponentExpectedState
from devices.service_providers.sql_db import psql_db


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
        sql = """
        SELECT expected state
        FROM rules
        WHERE device_component_id=:component_id
        AND state='completed'
        ORDER BY execution_time DESC
        LIMIT 1
        """
        result = await psql_db.fetch_one(
            sql, values={"actuator_id": actuator_id, "device_id": device_id}
        )
        return ComponentExpectedState.parse_obj(result)
