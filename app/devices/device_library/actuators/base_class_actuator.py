class Actuator:

    def __init__(self, device, actuator_id) -> None:
        self.actuator_id = actuator_id
        self.device = device

    def set_state(self, state: dict):
        return self.device._set_actuator_state(self.actuator_id, state)

    def get_state(self):
        return self.device._get_actuator_state(self.actuator_id)
