from devices.libraries.events_library.cesspoll_relay_sensor1 import CesspollRelaySensor1
from devices.libraries.events_library.irrigation_relay1 import IrrigationRelay1


class EventFactory:
    EVENTS = {
        "cesspoll_relay_sensor1": {
            '59551dc9-fa3f-4362-8a18-7678fd98c67b': CesspollRelaySensor1.WaterLevel,
            '53dd36aa-fe23-4d48-ac0e-08948f122e09': CesspollRelaySensor1.PumpStarter
        },
        "irrigation_relay1": {
            'b98d7199-cea3-43a8-a615-940b3a59ffa4': IrrigationRelay1.WaterLine,
            'a6157199-cea3-43a8-a615-940b3a59ffa4': IrrigationRelay1.WaterLine,
            'cea37199-cea3-43a8-a615-940b3a59ffa4': IrrigationRelay1.WaterLine,
        }
    }

    @classmethod
    def get(cls, device_id: str, component_id: str, event: str):
        try:
            return getattr(cls.EVENTS[device_id][component_id], event)
        except KeyError:
            return None
