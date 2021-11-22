from devices.models.users import User
from devices.queries.intervals import IntervalsQRS
from devices.config.config import Config
from fastapi import APIRouter, Depends

from devices.dependencies import ahttp_client, get_current_active_user, get_logger

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/weather/forecast", name="Get weather forecast")
async def get_weather_forecast(
    logger=Depends(get_logger),
    client=Depends(ahttp_client),
):
    """Get latest updates on weather"""
    logger.info("Getting info from openweather.")
    data = (await client.get(
        url=f"http://api.openweathermap.org/data/2.5/onecall?lat=50.11&lon=30.6227&appid={Config.OPENAPI_KEY}&lang=ua&units=metric&exclude=minutely,alerts"
        )).json()

    return data


@router.get("/rules/irrigation/forecast", name="Get planned irrigation rules")
async def get_rules_forecast(
    IntervalsQRS=Depends(IntervalsQRS),
    current_user: User = Depends(get_current_active_user),
):
    """Get latest updates on weather"""
    return await IntervalsQRS.get_next_irrigation_rule(current_user.id)
