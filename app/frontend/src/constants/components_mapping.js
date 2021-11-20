import CesspollMaster from '../components/Group/library/Cesspoll';
import IrrigationMaster from '../components/Group/library/Irrigation';
import IrrigationActuator from '../components/Group/library/Irrigation/IrrigationActuator';

export const components_mapping = {
    'irrigation': {
        'actuator': {
            'v1': IrrigationActuator
        }
    }
};

export const group_view_map = {
    'irrigation': IrrigationMaster,
    'cesspoll': CesspollMaster
}