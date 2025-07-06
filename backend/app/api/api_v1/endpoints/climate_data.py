from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from typing import Optional
from app.services.nasa_merra2 import get_climate_data
from app.services.nasa_services import nasa_services

router = APIRouter()

@router.get("/")
def climate_data(date: str = Query(None, description="Date in YYYY-MM-DD format, or omit for latest")):
    """Get basic climate data using MERRA-2"""
    try:
        dt = datetime.strptime(date, "%Y-%m-%d") if date else None
        data = get_climate_data(dt)
        return {"success": True, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/co2")
def co2_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get CO2 concentration data for a specific location"""
    try:
        data = nasa_services.get_co2_concentrations(lat, lon, date)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/temperature")
def temperature_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get temperature data for a specific location"""
    try:
        data = nasa_services.get_temperature_data(lat, lon, date)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/biomass")
def biomass_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius_km: float = Query(10, description="Radius in kilometers for analysis")
):
    """Get biomass data for intervention planning"""
    try:
        data = nasa_services.get_biomass_data(lat, lon, radius_km)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/historical")
def historical_climate_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    years_back: int = Query(10, description="Number of years of historical data")
):
    """Get historical climate patterns for algorithm training"""
    try:
        data = nasa_services.get_historical_climate_patterns(lat, lon, years_back)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimization")
def intervention_optimization_data(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get comprehensive data for climate intervention optimization"""
    try:
        data = nasa_services.get_intervention_optimization_data(lat, lon)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/satellite-imagery")
def satellite_imagery(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get satellite imagery for visual analysis"""
    try:
        data = nasa_services.get_satellite_imagery(lat, lon, date)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 