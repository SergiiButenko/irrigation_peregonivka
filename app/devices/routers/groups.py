from devices.queries.components import ComponentsQRS
from devices.models.users import User
from devices.queries.groups import GroupsQRS
from fastapi import APIRouter, Depends
from devices.dependencies import get_current_active_user, get_logger

router = APIRouter(
    prefix="/groups", tags=["groups"], dependencies=[Depends(get_current_active_user)]
)


@router.get("")
async def get_all_groups(
    current_user: User = Depends(get_current_active_user),
):
    return await GroupsQRS.get_groups(current_user.id)


@router.get("/{group_id}")
async def get_group_by_id(
    group_id: str,
    current_user: User = Depends(get_current_active_user),
):
    return await GroupsQRS.get_group_by_id(group_id, current_user.id)


@router.get("/{group_id}/components")
async def get_rule_by_id(
    group_id: str,
    current_user: User = Depends(get_current_active_user),
    logger=Depends(get_logger),
):
    return await ComponentsQRS.get_components_by_group_id(group_id, current_user.id)
