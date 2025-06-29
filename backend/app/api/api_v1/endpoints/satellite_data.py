from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from uuid import UUID

# TODO: Refactor this endpoint for Supabase. All SQLAlchemy code removed.

router = APIRouter()


@router.post("/", response_model=SatelliteData)
def create_satellite_data(
    satellite_data: SatelliteDataCreate,
    db: Session = Depends(get_db)
):
    """Create a new satellite data record"""
    return crud.create_satellite_data(db=db, satellite_data=satellite_data)


@router.get("/{satellite_data_id}", response_model=SatelliteData)
def get_satellite_data(
    satellite_data_id: UUID,
    db: Session = Depends(get_db)
):
    """Get satellite data by ID"""
    db_satellite_data = crud.get_satellite_data(db, satellite_data_id=satellite_data_id)
    if db_satellite_data is None:
        raise HTTPException(status_code=404, detail="Satellite data not found")
    return db_satellite_data


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


@router.put("/{satellite_data_id}", response_model=SatelliteData)
def update_satellite_data(
    satellite_data_id: UUID,
    satellite_data_update: SatelliteDataUpdate,
    db: Session = Depends(get_db)
):
    """Update satellite data"""
    db_satellite_data = crud.update_satellite_data(
        db=db,
        satellite_data_id=satellite_data_id,
        satellite_data_update=satellite_data_update
    )
    if db_satellite_data is None:
        raise HTTPException(status_code=404, detail="Satellite data not found")
    return db_satellite_data


@router.delete("/{satellite_data_id}")
def delete_satellite_data(
    satellite_data_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete satellite data"""
    success = crud.delete_satellite_data(db=db, satellite_data_id=satellite_data_id)
    if not success:
        raise HTTPException(status_code=404, detail="Satellite data not found")
    return {"message": "Satellite data deleted successfully"} 