from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from uuid import UUID
from app.crud.satellite_data import (
    create_satellite_data,
    get_satellite_data_by_id,
    update_satellite_data,
    delete_satellite_data,
)

# TODO: Refactor this endpoint for Supabase. All SQLAlchemy code removed.

router = APIRouter()


@router.post("/")
def create(data: dict):
    result = create_satellite_data(data)
    if not result:
        raise HTTPException(status_code=400, detail="Insert failed")
    return result


@router.get("/{id}")
def read(id: str):
    result = get_satellite_data_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.put("/{id}")
def update(id: str, data: dict):
    result = update_satellite_data(id, data)
    if not result:
        raise HTTPException(status_code=400, detail="Update failed")
    return result


@router.delete("/{id}")
def delete(id: str):
    result = delete_satellite_data(id)
    if not result:
        raise HTTPException(status_code=400, detail="Delete failed")
    return result


@router.get("/", response_model=List[SatelliteData])
def get_satellite_data_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    grid_cell_id: Optional[UUID] = Query(None),
    satellite_id: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of satellite data with optional filters"""
    return crud.get_satellite_data_list(
        db=db,
        skip=skip,
        limit=limit,
        grid_cell_id=grid_cell_id,
        satellite_id=satellite_id,
        start_time=start_time,
        end_time=end_time
    )


@router.get("/grid-cell/{grid_cell_id}", response_model=List[SatelliteData])
def get_satellite_data_by_grid_cell(
    grid_cell_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get satellite data for a specific grid cell"""
    return crud.get_satellite_data_by_grid_cell(
        db=db,
        grid_cell_id=grid_cell_id,
        skip=skip,
        limit=limit,
        start_time=start_time,
        end_time=end_time
    )


@router.get("/satellite/{satellite_id}", response_model=List[SatelliteData])
def get_satellite_data_by_satellite(
    satellite_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get satellite data by satellite ID"""
    return crud.get_satellite_data_by_satellite(
        db=db,
        satellite_id=satellite_id,
        skip=skip,
        limit=limit
    )


@router.get("/time-range/", response_model=List[SatelliteData])
def get_satellite_data_by_time_range(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get satellite data within a time range"""
    return crud.get_satellite_data_by_time_range(
        db=db,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )


@router.get("/grid-cell/{grid_cell_id}/latest", response_model=SatelliteData)
def get_latest_satellite_data_by_grid_cell(
    grid_cell_id: UUID,
    db: Session = Depends(get_db)
):
    """Get the latest satellite data for a grid cell"""
    db_satellite_data = crud.get_latest_satellite_data_by_grid_cell(db, grid_cell_id=grid_cell_id)
    if db_satellite_data is None:
        raise HTTPException(status_code=404, detail="No satellite data found for this grid cell")
    return db_satellite_data


@router.get("/statistics/")
def get_satellite_data_statistics(
    grid_cell_id: Optional[UUID] = Query(None),
    satellite_id: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get statistics for satellite data"""
    return crud.get_satellite_data_statistics(
        db=db,
        grid_cell_id=grid_cell_id,
        satellite_id=satellite_id,
        start_time=start_time,
        end_time=end_time
    ) 