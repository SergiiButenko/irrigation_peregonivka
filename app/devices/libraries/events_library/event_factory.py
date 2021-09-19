from devices.libraries.device_library.devices.base_class_device import Device
from devices.libraries.events_library.cesspoll_relay_sensor1 import CesspollRelaySensor1
from devices.libraries.events_library.irrigation_relay1 import IrrigationRelay1


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
    def get(cls, device: Device, component_id: int, event: str):
        if cls.EVENTS[device.device_id][component_id] is not None:
            return getattr(cls.EVENTS[device.device_id][component_id], event)

        return getattr(device[component_id], event)
