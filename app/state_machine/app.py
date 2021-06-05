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


@app.put("/devices/{device_id}/sensors/{sensor_id}")
async def air_sensor(device_id: str, sensor_id: str):
    base_url = get_device_IP_by_line_id(sensor_id)

    response_air = requests.get(
        url="http://" + base_url + "/" + sensor_id,
    )
    response_air.raise_for_status()
    
    return response_air.json()

