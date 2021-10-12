from devices.models.devices import ComponentSql
from devices.models.rules import Rule
from devices.service_providers.httpx_client import HttpxClient
from devices.config.config import Config


class DevicesClient:
    def __init__(self) -> None:
        self.headers = None

    async def login(self, username, password):
        res = await HttpxClient.post_with_raise(
            data={"username": username, "password": password}
        )

        token = res.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {token}"}

    async def get_rule(self, rule_id):
        _rule = await HttpxClient.get_with_raise(
            url=Config.DEVICES_URL + "/rules/" + rule_id, headers=self.headers
        )

        return Rule.parse_obj(_rule.json())

    async def update_rule_state(self, rule_id, state):
        _rule = await HttpxClient.put_with_raise(
            url=f"{Config.DEVICES_URL}/rules/{rule_id}/state",
            json={"expected_state": state},
            headers=self.headers,
        )

        return Rule.parse_obj(_rule.json())

    async def update_actuator_state(self, device_id, actuator_id, state):
        return await HttpxClient.put_with_raise(
            url=f"{Config.DEVICES_URL}/devices/{device_id}/actuators/{actuator_id}/state",
            json={"expected_state": state},
            headers=self.headers,
        )

    async def get_actuator(self, device_id, actuator_id):
        _actuator = await HttpxClient.get_with_raise(
            url=f"{Config.DEVICES_URL}/devices/{device_id}/actuators/{actuator_id}",
            headers=self.headers,
        )
        return ComponentSql.parse_obj(_actuator.json())

    async def send_message(self, message, user=Config.TELEGRAM_CHAT_ID_COTTAGE):
        return await HttpxClient.post_with_raise(
            url=f"{Config.DEVICES_URL}/telegram/{user}/message",
            json={"message": message},
            headers=self.headers,
        )
