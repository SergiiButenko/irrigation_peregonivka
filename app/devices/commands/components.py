from devices.schemas.schema import SensorData
from devices.commands.events import EventsCMD
from devices.queries.sensors import SensorQRS
from devices.queries.components import ComponentsQRS
from devices.queries.intervals import IntervalsQRS


class ComponentsCMD:
    @staticmethod
    async def get_component_state(component_id, current_user):
        state = await ComponentsQRS.get_expected_component_state(component_id)
        component = await ComponentsQRS.get_component_by_id(component_id)
        return {
            "expected_state": state.expected_state,
            "interval": await IntervalsQRS.get_active_interval_by_component_id(
                component_id, current_user
            ),
            "component": component,
        }

    @staticmethod
    async def get_component_data(component_id, limit):
        component = await ComponentsQRS.get_component_by_id(component_id)
        data = await SensorQRS.get_sensor_values_by_id(
            component_id,
            limit=limit,
        )

        return SensorData.parse_obj({
            'component': component,
            'data': data
        })


    @staticmethod
    async def register_component_data(component_id, sensor_value, events_cmds, notification_service):
        await SensorQRS.register_sensor_value_by_id(component_id, sensor_value.data)
        await events_cmds.try_execute(component_id, "analyse")
        
        component_data = await ComponentsCMD.get_component_data(component_id, limit=1)
        await notification_service.send_ws_message(
            "sensor_update",
            component_data
        )
        return component_data
