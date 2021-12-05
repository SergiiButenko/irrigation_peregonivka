import CesspollMaster from '../components/Group/library/Cesspoll';
import IrrigationMaster from '../components/Group/library/Irrigation';
import IrrigationActuator from '../devices_library/actuators/IrrigationActuator';
import relayV1 from '../devices_library/actuators/relayV1';
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
    }
};

export const group_view_map = {
    'irrigation': IrrigationMaster,
    'cesspoll': CesspollMaster
};