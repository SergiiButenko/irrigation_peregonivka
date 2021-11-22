import CesspollMaster from '../components/Group/library/Cesspoll';
import IrrigationMaster from '../components/Group/library/Irrigation';
import IrrigationActuator from '../components/Group/library/Irrigation/IrrigationActuator';
import Switcher from '../components/Group/shared/Switcher';

export const components_mapping = {
    'irrigation': {
        'actuator': {
            'v1': IrrigationActuator
        }
    },
    'cesspoll' : {
        'actuator': {
            'v1': Switcher
        },
        'sensor': {
            'v1': null
        }
    }
};

export const group_view_map = {
    'irrigation': IrrigationMaster,
    'cesspoll': CesspollMaster
}