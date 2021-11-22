from devices.schemas.schema import ComponentExpectedState
from devices.models.devices import DeviceSql
from devices.service_providers.device_logger import logger


class IrrigationRelay1:

    class WaterLine:

        @staticmethod
        def set_state(device: DeviceSql, component_id: int, in_state: ComponentExpectedState, *args, **kwargs):
            state = int(in_state.expected_state)

            if state == 1:
                logger.info("TURN ON PUMP; SLEEP; TURN ON VALVE")
                pass

            if state == 0:
                logger.info("TURN OFF PUMP; SLEEP; TURN OFF VALVE")
                pass
