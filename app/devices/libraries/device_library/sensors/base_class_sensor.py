class Sensor:

    def __init__(self, device, sensor_id) -> None:
        self.sensor_id = sensor_id
        self.device = device

    def set_state(self, state: dict) -> None:
        raise NotImplementedError("It is not possible to set state for sensor")

    def get_state(self):
        return self.device._get_sensor_state(self.sensor_id)
