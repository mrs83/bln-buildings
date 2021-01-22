from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.crud import (
    get_buildings,
    get_total_buildings_by_plz,
    get_total_buildings_by_year,
)
from app.db.schemas import (
    Building,
    BuildingOut,
    BuildingByPlzOut,
    BuildingByYearOut
)
# from app.core.auth import get_current_active_user

buildings_router = r = APIRouter()


@r.get(
    "/buildings",
    response_model=t.List[Building],
    response_model_exclude_none=True,
)
async def buildings_list(
    response: Response,
    db=Depends(get_db),
    # current_user=Depends(get_current_active_user),
):
    """
    Get all buildings
    """
    buildings = get_buildings(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(buildings)}"
    return buildings

@r.get(
    "/buildings/by-plz",
    response_model=t.List[BuildingByPlzOut],
    response_model_exclude_none=True,
)
async def total_buildings_by_plz(
    response: Response,
    db=Depends(get_db),
    # current_user=Depends(get_current_active_user),
    plz: t.Optional[int] = 0,
):
    """
    Get total buildings by plz.
    """
    results = get_total_buildings_by_plz(db, plz)
    return results

@r.get(
    "/buildings/by-year",
    response_model=t.List[BuildingByYearOut],
    response_model_exclude_none=True,
)
async def total_buildings_by_year(
    response: Response,
    db=Depends(get_db),
    # current_user=Depends(get_current_active_user),
    plz: t.Optional[int] = 0,
):
    """
    Get total buildings by year.
    """
    results = get_total_buildings_by_year(db, plz)
    return results
