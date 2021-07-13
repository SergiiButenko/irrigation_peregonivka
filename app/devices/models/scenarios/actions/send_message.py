from devices.models.scenarios.actions.base_action import BaseACtion


class ActionSendMessage(BaseACtion):

    def __init__(self, channel_id, message) -> None:
        super().__init__()
        self.channel_id = channel_id
        self.message = message

    def execute(self):
        pass

