from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class SatelliteDataBase(BaseModel):
    grid_cell_id: UUID
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    precipitation: Optional[float] = None
    aerosol_optical_depth: Optional[float] = None
    co2_concentration: Optional[float] = None
    methane_concentration: Optional[float] = None
    solar_irradiance: Optional[float] = None
    albedo: Optional[float] = None
    satellite_id: str
    instrument: Optional[str] = None
    data_quality: Optional[float] = None
    processing_level: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None
    quality_flags: Optional[Dict[str, Any]] = None
    uncertainty: Optional[Dict[str, Any]] = None


class SatelliteDataCreate(SatelliteDataBase):
    pass


class SatelliteDataUpdate(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    precipitation: Optional[float] = None
    aerosol_optical_depth: Optional[float] = None
    co2_concentration: Optional[float] = None
    methane_concentration: Optional[float] = None
    solar_irradiance: Optional[float] = None
    albedo: Optional[float] = None
    instrument: Optional[str] = None
    data_quality: Optional[float] = None
    processing_level: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None
    quality_flags: Optional[Dict[str, Any]] = None
    uncertainty: Optional[Dict[str, Any]] = None


class SatelliteDataInDB(SatelliteDataBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SatelliteData(SatelliteDataInDB):
    pass 