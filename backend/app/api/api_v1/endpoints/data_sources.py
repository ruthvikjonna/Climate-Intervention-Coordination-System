from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from app.core.database import get_db
from app.crud import data_source as crud
from app.schemas.data_source import (
    DataSource, 
    DataSourceCreate, 
    DataSourceUpdate
)

router = APIRouter()


@router.post("/", response_model=DataSource)
def create_data_source(
    data_source: DataSourceCreate,
    db: Session = Depends(get_db)
):
    """Create a new data source record"""
    # Check if data source with same name already exists
    existing = crud.get_data_source_by_name(db, name=data_source.name)
    if existing:
        raise HTTPException(status_code=400, detail="Data source with this name already exists")
    
    return crud.create_data_source(db=db, data_source=data_source)


@router.get("/{data_source_id}", response_model=DataSource)
def get_data_source(
    data_source_id: UUID,
    db: Session = Depends(get_db)
):
    """Get data source by ID"""
    db_data_source = crud.get_data_source(db, data_source_id=data_source_id)
    if db_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return db_data_source


@router.get("/name/{name}", response_model=DataSource)
def get_data_source_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    """Get data source by name"""
    db_data_source = crud.get_data_source_by_name(db, name=name)
    if db_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return db_data_source


@router.get("/", response_model=List[DataSource])
def get_data_source_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source_type: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    requires_auth: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of data sources with optional filters"""
    return crud.get_data_source_list(
        db=db,
        skip=skip,
        limit=limit,
        source_type=source_type,
        provider=provider,
        is_active=is_active,
        requires_auth=requires_auth
    )


@router.get("/type/{source_type}", response_model=List[DataSource])
def get_data_sources_by_type(
    source_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get data sources by type"""
    return crud.get_data_sources_by_type(
        db=db,
        source_type=source_type,
        skip=skip,
        limit=limit
    )


@router.get("/provider/{provider}", response_model=List[DataSource])
def get_data_sources_by_provider(
    provider: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get data sources by provider"""
    return crud.get_data_sources_by_provider(
        db=db,
        provider=provider,
        skip=skip,
        limit=limit
    )


@router.get("/active/", response_model=List[DataSource])
def get_active_data_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all active data sources"""
    return crud.get_active_data_sources(
        db=db,
        skip=skip,
        limit=limit
    )


@router.get("/auth/{requires_auth}", response_model=List[DataSource])
def get_data_sources_by_authentication(
    requires_auth: bool,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get data sources by authentication requirement"""
    return crud.get_data_sources_by_authentication(
        db=db,
        requires_auth=requires_auth,
        skip=skip,
        limit=limit
    )


@router.get("/frequency/{frequency}", response_model=List[DataSource])
def get_data_sources_by_update_frequency(
    frequency: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get data sources by update frequency"""
    return crud.get_data_sources_by_update_frequency(
        db=db,
        frequency=frequency,
        skip=skip,
        limit=limit
    )


@router.get("/search/{search_term}", response_model=List[DataSource])
def search_data_sources(
    search_term: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Search data sources by name, description, or provider"""
    return crud.search_data_sources(
        db=db,
        search_term=search_term,
        skip=skip,
        limit=limit
    )


@router.get("/statistics/")
def get_data_source_statistics(db: Session = Depends(get_db)):
    """Get statistics for data sources"""
    return crud.get_data_source_statistics(db=db)


@router.put("/{data_source_id}", response_model=DataSource)
def update_data_source(
    data_source_id: UUID,
    data_source_update: DataSourceUpdate,
    db: Session = Depends(get_db)
):
    """Update data source"""
    db_data_source = crud.update_data_source(
        db=db,
        data_source_id=data_source_id,
        data_source_update=data_source_update
    )
    if db_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return db_data_source


@router.put("/{data_source_id}/status")
def update_data_source_status(
    data_source_id: UUID,
    is_active: bool,
    last_error: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update data source status and error information"""
    db_data_source = crud.update_data_source_status(
        db=db,
        data_source_id=data_source_id,
        is_active=is_active,
        last_error=last_error
    )
    if db_data_source is None:
        raise HTTPException(status_code=404, detail="Data source not found")
    return {"message": f"Data source status updated to {'active' if is_active else 'inactive'}"}


@router.delete("/{data_source_id}")
def delete_data_source(
    data_source_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete data source"""
    success = crud.delete_data_source(db=db, data_source_id=data_source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data source not found")
    return {"message": "Data source deleted successfully"} 