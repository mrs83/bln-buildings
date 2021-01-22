from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.crud import (
    get_buildings,
)
from app.db.schemas import Building, BuildingOut
from app.core.auth import get_current_active_user, get_current_active_superuser

buildings_router = r = APIRouter()


@r.get(
    "/buildings",
    response_model=t.List[Building],
    response_model_exclude_none=True,
)
async def buildings_list(
    response: Response,
    db=Depends(get_db),
    # current_user=Depends(get_current_active_superuser),
):
    """
    Get all buildings
    """
    buildings = get_buildings(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(buildings)}"
    return buildings
