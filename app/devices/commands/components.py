from devices.queries.components import ComponentsQRS
from devices.queries.intervals import IntervalsQRS


class ComponentsCMD:

    @staticmethod
    async def get_component_state(component_id, current_user):
        state = await ComponentsQRS.get_expected_component_state(component_id)
        component = await ComponentsQRS.get_component_by_id(component_id)
        return {
            'expected_state': state.expected_state,
            'interval': await IntervalsQRS.get_active_interval_by_component_id(component_id, current_user),
            'component': component
        }
