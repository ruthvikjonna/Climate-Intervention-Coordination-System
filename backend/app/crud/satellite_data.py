# TODO: Refactor this CRUD module for Supabase. All SQLAlchemy code removed.

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from uuid import UUID

from app.schemas.satellite_data import SatelliteData
from app.schemas.satellite_data import SatelliteDataCreate, SatelliteDataUpdate
from app.core.supabase_client import get_supabase


def create_satellite_data(data: dict):
    response = get_supabase().table("satellite_data").insert(data).execute()
    return response.data


def get_satellite_data_by_id(id: str):
    response = get_supabase().table("satellite_data").select("*").eq("id", id).single().execute()
    return response.data


def update_satellite_data(id: str, data: dict):
    response = get_supabase().table("satellite_data").update(data).eq("id", id).execute()
    return response.data


def delete_satellite_data(id: str):
    response = get_supabase().table("satellite_data").delete().eq("id", id).execute()
    return response.data


def get_satellite_data(db: Session, satellite_data_id: UUID) -> Optional[SatelliteData]:
    """Get satellite data by ID"""
    return db.query(SatelliteData).filter(SatelliteData.id == satellite_data_id).first()


def get_satellite_data_by_grid_cell(
    db: Session, 
    grid_cell_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[SatelliteData]:
    """Get satellite data for a specific grid cell with optional time filtering"""
    query = db.query(SatelliteData).filter(SatelliteData.grid_cell_id == grid_cell_id)
    
    if start_time:
        query = query.filter(SatelliteData.timestamp >= start_time)
    if end_time:
        query = query.filter(SatelliteData.timestamp <= end_time)
    
    return query.order_by(SatelliteData.timestamp.desc()).offset(skip).limit(limit).all()


def get_satellite_data_by_satellite(
    db: Session, 
    satellite_id: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[SatelliteData]:
    """Get satellite data by satellite ID"""
    return db.query(SatelliteData).filter(
        SatelliteData.satellite_id == satellite_id
    ).order_by(SatelliteData.timestamp.desc()).offset(skip).limit(limit).all()


def get_satellite_data_by_time_range(
    db: Session,
    start_time: datetime,
    end_time: datetime,
    skip: int = 0,
    limit: int = 100
) -> List[SatelliteData]:
    """Get satellite data within a time range"""
    return db.query(SatelliteData).filter(
        and_(
            SatelliteData.timestamp >= start_time,
            SatelliteData.timestamp <= end_time
        )
    ).order_by(SatelliteData.timestamp.desc()).offset(skip).limit(limit).all()


def get_latest_satellite_data_by_grid_cell(
    db: Session, 
    grid_cell_id: UUID
) -> Optional[SatelliteData]:
    """Get the latest satellite data for a grid cell"""
    return db.query(SatelliteData).filter(
        SatelliteData.grid_cell_id == grid_cell_id
    ).order_by(SatelliteData.timestamp.desc()).first()


def get_satellite_data_statistics(
    db: Session,
    grid_cell_id: Optional[UUID] = None,
    satellite_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """Get statistics for satellite data"""
    query = db.query(SatelliteData)
    
    if grid_cell_id:
        query = query.filter(SatelliteData.grid_cell_id == grid_cell_id)
    if satellite_id:
        query = query.filter(SatelliteData.satellite_id == satellite_id)
    if start_time:
        query = query.filter(SatelliteData.timestamp >= start_time)
    if end_time:
        query = query.filter(SatelliteData.timestamp <= end_time)
    
    stats = {
        "total_records": query.count(),
        "avg_temperature": query.with_entities(func.avg(SatelliteData.temperature)).scalar(),
        "avg_humidity": query.with_entities(func.avg(SatelliteData.humidity)).scalar(),
        "avg_pressure": query.with_entities(func.avg(SatelliteData.pressure)).scalar(),
        "avg_co2": query.with_entities(func.avg(SatelliteData.co2_concentration)).scalar(),
        "avg_aod": query.with_entities(func.avg(SatelliteData.aerosol_optical_depth)).scalar(),
        "data_quality_avg": query.with_entities(func.avg(SatelliteData.data_quality)).scalar(),
    }
    
    return stats


def get_satellite_data_list(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    grid_cell_id: Optional[UUID] = None,
    satellite_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[SatelliteData]:
    """Get list of satellite data with optional filters"""
    query = db.query(SatelliteData)
    
    if grid_cell_id:
        query = query.filter(SatelliteData.grid_cell_id == grid_cell_id)
    if satellite_id:
        query = query.filter(SatelliteData.satellite_id == satellite_id)
    if start_time:
        query = query.filter(SatelliteData.timestamp >= start_time)
    if end_time:
        query = query.filter(SatelliteData.timestamp <= end_time)
    
    return query.order_by(SatelliteData.timestamp.desc()).offset(skip).limit(limit).all() 