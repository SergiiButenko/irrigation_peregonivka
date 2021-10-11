from devices.models.users import User
from devices.service_providers.sql_db import psql_db


class UsersQRS:
    @staticmethod
    async def get_user(email: str):
        sql = "SELECT * FROM users WHERE email=:email"
        result = await psql_db.fetch_one(
            sql, values={'email': email}
        )
        
        return User.parse_obj(result)
