from fastapi import APIRouter, Query
from datetime import datetime
from app.services.nasa_merra2 import get_climate_data

router = APIRouter()

@router.get("/")
def climate_data(date: str = Query(None, description="Date in YYYY-MM-DD format, or omit for latest")):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d") if date else None
        data = get_climate_data(dt)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)} 