from devices.models.users import User
from devices.service_providers.sql_db import psql_db


class UsersQRS:
    @staticmethod
    async def get_user(username: str):
        sql = "SELECT * FROM users WHERE username=:username"
        result = await psql_db.fetch_one(sql, values={"username": username})

        return User.parse_obj(result)
