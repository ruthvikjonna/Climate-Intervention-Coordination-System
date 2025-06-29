from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from uuid import UUID
from app.crud.intervention_impact import (
    create_intervention_impact,
    get_intervention_impact_by_id,
    update_intervention_impact,
    delete_intervention_impact,
)

# TODO: Refactor this endpoint for Supabase. All SQLAlchemy code removed.

router = APIRouter()


@router.post("/")
def create(data: dict):
    result = create_intervention_impact(data)
    if not result:
        raise HTTPException(status_code=400, detail="Insert failed")
    return result


@router.get("/{id}")
def read(id: str):
    result = get_intervention_impact_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.put("/{id}")
def update(id: str, data: dict):
    result = update_intervention_impact(id, data)
    if not result:
        raise HTTPException(status_code=400, detail="Update failed")
    return result


@router.delete("/{id}")
def delete(id: str):
    result = delete_intervention_impact(id)
    if not result:
        raise HTTPException(status_code=400, detail="Delete failed")
    return result


@router.get("/", response_model=List[InterventionImpact])
def get_intervention_impact_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    intervention_id: Optional[UUID] = Query(None),
    grid_cell_id: Optional[UUID] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    min_effectiveness: Optional[float] = Query(None, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """Get list of intervention impacts with optional filters"""
    return crud.get_impact_list(
        db=db,
        skip=skip,
        limit=limit,
        intervention_id=intervention_id,
        grid_cell_id=grid_cell_id,
        start_time=start_time,
        end_time=end_time,
        min_effectiveness=min_effectiveness
    )


@router.get("/intervention/{intervention_id}", response_model=List[InterventionImpact])
def get_impacts_by_intervention(
    intervention_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all impacts for a specific intervention"""
    return crud.get_impacts_by_intervention(
        db=db,
        intervention_id=intervention_id,
        skip=skip,
        limit=limit
    )


@router.get("/grid-cell/{grid_cell_id}", response_model=List[InterventionImpact])
def get_impacts_by_grid_cell(
    grid_cell_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get impacts for a specific grid cell"""
    return crud.get_impacts_by_grid_cell(
        db=db,
        grid_cell_id=grid_cell_id,
        skip=skip,
        limit=limit,
        start_time=start_time,
        end_time=end_time
    )


@router.get("/effectiveness-range/", response_model=List[InterventionImpact])
def get_impacts_by_effectiveness_range(
    min_effectiveness: float = Query(..., ge=0, le=1),
    max_effectiveness: float = Query(..., ge=0, le=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get impacts within a specific effectiveness range"""
    if min_effectiveness > max_effectiveness:
        raise HTTPException(status_code=400, detail="min_effectiveness must be less than or equal to max_effectiveness")
    
    return crud.get_impacts_by_effectiveness_range(
        db=db,
        min_effectiveness=min_effectiveness,
        max_effectiveness=max_effectiveness,
        skip=skip,
        limit=limit
    )


@router.get("/best-performing/", response_model=List[InterventionImpact])
def get_best_performing_impacts(
    limit: int = Query(10, ge=1, le=100),
    intervention_id: Optional[UUID] = Query(None),
    grid_cell_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """Get the best performing impacts based on effectiveness score"""
    return crud.get_best_performing_impacts(
        db=db,
        limit=limit,
        intervention_id=intervention_id,
        grid_cell_id=grid_cell_id
    )


@router.get("/statistics/")
def get_impact_statistics(
    intervention_id: Optional[UUID] = Query(None),
    grid_cell_id: Optional[UUID] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get statistics for intervention impacts"""
    return crud.get_impact_statistics(
        db=db,
        intervention_id=intervention_id,
        grid_cell_id=grid_cell_id,
        start_time=start_time,
        end_time=end_time
    ) 