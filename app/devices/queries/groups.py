from devices.models.groups import Group, Groups
from devices.service_providers.sql_db import psql_db


class GroupsQRS:
    @staticmethod
    async def get_groups(user_id: str):
        sql = "SELECT * FROM public.groups WHERE user_id=:user_id"
        result = await psql_db.fetch_all(sql, values={"user_id": user_id})

        return Groups.parse_obj(result)

    @staticmethod
    async def get_group_by_id(group_id: str, user_id: str):
        sql = "SELECT * FROM public.groups WHERE user_id=:user_id and id=:group_id"
        result = await psql_db.fetch_one(
            sql, values={"user_id": user_id, "group_id": group_id}
        )

        return Group.parse_obj(result)
