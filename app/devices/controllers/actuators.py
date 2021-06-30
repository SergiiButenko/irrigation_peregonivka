from devices.service_providers.httpx_client import HttpxClient
from fastapi import APIRouter, Depends, status, Response
from fastapi.params import Header
from pydantic import Required

from devices.dependencies import ahttp_client, service_logger
from devices.commands.devices import DeviceCMD

router = APIRouter(
    prefix="/devices/{device_id}",
    tags=["actuator"]
)


@router.put("/lines/{line_id}", status_code=204)
async def set_state(device_id: str, line_id: str, state: State):
    """Change state of line."""
    line = database.get_line_by_id(line_id)

    relay = line["relay_num"]
    base_url = get_device_IP_by_line_id(line_id)
    status = requests.post(
        url="http://" + base_url + "/state",
        params={"relay": relay, 'state': state.expected_state}
    )
    status.raise_for_status()


@router.get("/lines/{line_id}")
async def get_state(device_id: str, line_id: str):
    line = database.get_line_by_id(line_id)

    relay = line["relay_num"]
    base_url = get_device_IP_by_line_id(line_id)
    response = requests.get(
        url="http://" + base_url + "/state"
    )
    response.raise_for_status()
    response = response.json()

    return response[relay]

