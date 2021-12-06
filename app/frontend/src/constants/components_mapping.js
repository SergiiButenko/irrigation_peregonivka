import CesspollMaster from '../components/Group/library/Cesspoll';
import GreenHouseMaster from '../components/Group/library/GreenHouse';
import IrrigationMaster from '../components/Group/library/Irrigation';
import IrrigationActuator from '../devices_library/actuators/IrrigationActuator';
import relayV1 from '../devices_library/actuators/relayV1';
import DHT11V1 from '../devices_library/sensors/DHT11V1';
import PowerCurrentV1 from '../devices_library/sensors/PowerCurrentV1';

export const components_mapping = {
    'irrigation': {
        'actuator': {
            'relay': {
                'v1': IrrigationActuator
            }
        }
    },
    'cesspoll': {
        'actuator': {
            'relay': {
                'v1': relayV1
            }
        },
        'sensor': {
            'POWER_CURRENT': {
                'v1': PowerCurrentV1
            }
        }
    },
    'greenhouse': {
        'actuator': {
            'relay': {
                'v1': relayV1
            }
        },
        'sensor': {
            'dht11': {
                'v1': DHT11V1
            }
        }
    }
};

export const group_view_map = {
    'irrigation': IrrigationMaster,
    'cesspoll': CesspollMaster,
    'greenhouse': GreenHouseMaster,
};