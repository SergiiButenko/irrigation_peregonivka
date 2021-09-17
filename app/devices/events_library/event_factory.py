from devices.events_library.cesspoll_relay_sensor1 import CesspollRelaySensor1
from devices.events_library.irrigation_relay1 import IrrigationRelay1


class EventFactory:
    EVENTS = {
        "cesspoll_relay_sensor1": {
            1: CesspollRelaySensor1.WaterLevel,
            2: CesspollRelaySensor1.PumpStarter
        },

        "irrigation_relay1": {
            1: IrrigationRelay1.WaterLine,
            2: IrrigationRelay1.WaterLine,
            3: IrrigationRelay1.WaterLine,
            4: IrrigationRelay1.WaterLine,
            5: IrrigationRelay1.WaterLine,
            6: IrrigationRelay1.WaterLine,
            7: IrrigationRelay1.WaterLine,
            8: IrrigationRelay1.WaterLine
        }
    }

    @classmethod
    def get(cls, device_id: str, component_id: int, event: str):
        if cls.EVENTS[device_id][component_id] is None:
            raise LookupError("No matching Event found in codebase") 

        return getattr(cls.EVENTS[device_id][component_id], event)
