from devices.commands.intervals import IntervalsCMD
from devices.enums.intervals import IntervalPossibleState
from devices.models.users import User
from devices.schemas.schema import IntervalState
from devices.queries.intervals import IntervalsQRS
from fastapi import APIRouter, Depends
from devices.dependencies import get_current_active_user

router = APIRouter(
    prefix="/intervals",
    tags=["intervals"],
    dependencies=[Depends(get_current_active_user)]
)


@router.get("/{interval_id}")
async def get_interval_by_id(
    interval_id: str,
    IntervalsQRS=Depends(IntervalsQRS),
    current_user: User = Depends(get_current_active_user),
):
    return await IntervalsQRS.get_interval(interval_id, current_user)


@router.put("/{interval_id}/state")
async def change_interval_state(
    interval_id: str,
    interval_state: IntervalState,
    current_user: User = Depends(get_current_active_user),
):
    return await IntervalsQRS.set_interval_state(
        interval_id,
        interval_state.expected_state,
        current_user
    )


@router.delete("/{interval_id}")
async def remove_interval(
    interval_id: str,
    current_user: User = Depends(get_current_active_user),
):
    return await IntervalsCMD.cancel_interval(
        interval_id,
        IntervalPossibleState.CANCELED,
        current_user
    )
