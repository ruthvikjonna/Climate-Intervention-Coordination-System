from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from uuid import UUID

from app.core.supabase_client import get_supabase
from app.crud.data_source import (
    create_data_source,
    get_data_source_by_id,
    update_data_source,
    delete_data_source,
)
from app.schemas.data_source import (
    DataSource, 
    DataSourceCreate, 
    DataSourceUpdate
)

router = APIRouter()


@router.post("/")
def create(data: dict):
    result = create_data_source(data)
    if not result:
        raise HTTPException(status_code=400, detail="Insert failed")
    return result


@router.get("/{id}")
def read(id: str):
    result = get_data_source_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.put("/{id}")
def update(id: str, data: dict):
    result = update_data_source(id, data)
    if not result:
        raise HTTPException(status_code=400, detail="Update failed")
    return result


@router.delete("/{id}")
def delete(id: str):
    result = delete_data_source(id)
    if not result:
        raise HTTPException(status_code=400, detail="Delete failed")
    return result


@router.get("/", response_model=List[DataSource])
def get_data_source_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source_type: Optional[str] = Query(None),
    provider: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    requires_auth: Optional[bool] = Query(None),
):
    """Get list of data sources with optional filters"""
    return crud.get_data_source_list(
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
):
    """Get data sources by type"""
    return crud.get_data_sources_by_type(
        source_type=source_type,
        skip=skip,
        limit=limit
    )


@router.get("/provider/{provider}", response_model=List[DataSource])
def get_data_sources_by_provider(
    provider: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get data sources by provider"""
    return crud.get_data_sources_by_provider(
        provider=provider,
        skip=skip,
        limit=limit
    )


@router.get("/active/", response_model=List[DataSource])
def get_active_data_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get all active data sources"""
    return crud.get_active_data_sources(
        skip=skip,
        limit=limit
    )


@router.get("/auth/{requires_auth}", response_model=List[DataSource])
def get_data_sources_by_authentication(
    requires_auth: bool,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get data sources by authentication requirement"""
    return crud.get_data_sources_by_authentication(
        requires_auth=requires_auth,
        skip=skip,
        limit=limit
    )


@router.get("/frequency/{frequency}", response_model=List[DataSource])
def get_data_sources_by_update_frequency(
    frequency: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get data sources by update frequency"""
    return crud.get_data_sources_by_update_frequency(
        frequency=frequency,
        skip=skip,
        limit=limit
    )


@router.get("/search/{search_term}", response_model=List[DataSource])
def search_data_sources(
    search_term: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Search data sources by name, description, or provider"""
    return crud.search_data_sources(
        search_term=search_term,
        skip=skip,
        limit=limit
    )


@router.get("/statistics/")
def get_data_source_statistics():
    """Get statistics for data sources"""
    return crud.get_data_source_statistics()


@router.put("/{data_source_id}", response_model=DataSource)
def update_data_source(
    data_source_id: UUID,
    data_source_update: DataSourceUpdate,
):
    """Update data source"""
    db_data_source = crud.update_data_source(
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
):
    """Update data source status and error information"""
    db_data_source = crud.update_data_source_status(
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
):
    """Delete data source"""
    success = crud.delete_data_source(data_source_id=data_source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Data source not found")
    return {"message": "Data source deleted successfully"}

# TODO: Refactor this endpoint for Supabase. All SQLAlchemy code removed. 