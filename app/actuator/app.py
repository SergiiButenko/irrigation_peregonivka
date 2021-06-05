import logging
import requests

from fastapi import FastAPI
from actuator.resources.helpers import get_device_IP_by_line_id
from actuator.models.state import State

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO
)

app = FastAPI()


@app.put("/devices/{device_id}/lines/{line_id}", status_code=204)
async def set_state(device_id: str, line_id: str, state: State):
    """Change state of line."""
    line = database.get_line_by_id(line_id)

    relay = line["relay_num"]
    base_url = get_device_IP_by_line_id(line_id)
    status = requests.get(
        url="http://" + base_url + "/state",
        params={"relay": relay, 'state': state.expected_state}
    )
    status.raise_for_status()


@app.get("/devices/{device_id}/sensors/{sensor_id}")
async def air_sensor(device_id: str, sensor_id: str):
    base_url = get_device_IP_by_line_id(sensor_id)

    response_air = requests.get(
        url="http://" + base_url + "/" + sensor_id,
    )
    response_air.raise_for_status()
    
    return response_air.json()


@app.get("/devices/{device_id}/lines/{line_id}")
async def get_state(device_id: str, line_id: str):
    line = database.get_line_by_id(line_id)

    relay = line["relay_num"]
    base_url = get_device_IP_by_line_id(line_id)
    response = requests.get(
        url="http://" + base_url + "/status"
    )
    response.raise_for_status()
    response = response.json()

    return response[relay]

