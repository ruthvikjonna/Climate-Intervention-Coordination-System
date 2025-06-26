from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.intervention import intervention
from app.schemas.intervention import (
    InterventionCreate,
    InterventionUpdate,
    InterventionResponse,
    InterventionListResponse
)

router = APIRouter()


@router.post("/", response_model=InterventionResponse, status_code=status.HTTP_201_CREATED)
def create_intervention(
    *,
    db: Session = Depends(get_db),
    intervention_in: InterventionCreate,
) -> InterventionResponse:
    """
    Create a new intervention.
    """
    intervention_obj = intervention.create(db=db, obj_in=intervention_in)
    return intervention_obj


@router.get("/", response_model=InterventionListResponse)
def read_interventions(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    intervention_type: Optional[str] = Query(None, description="Filter by intervention type"),
    operator: Optional[str] = Query(None, description="Filter by operator"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in name, description, or operator"),
) -> InterventionListResponse:
    """
    Retrieve interventions with optional filtering and pagination.
    """
    interventions, total = intervention.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        intervention_type=intervention_type,
        operator=operator,
        status=status,
        search=search
    )
    
    pages = (total + limit - 1) // limit if total > 0 else 0
    page = (skip // limit) + 1 if total > 0 else 0
    
    return InterventionListResponse(
        interventions=interventions,
        total=total,
        page=page,
        size=limit,
        pages=pages
    )


@router.get("/{intervention_id}", response_model=InterventionResponse)
def read_intervention(
    *,
    db: Session = Depends(get_db),
    intervention_id: int,
) -> InterventionResponse:
    """
    Get intervention by ID.
    """
    intervention_obj = intervention.get(db=db, id=intervention_id)
    if not intervention_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    return intervention_obj


@router.put("/{intervention_id}", response_model=InterventionResponse)
def update_intervention(
    *,
    db: Session = Depends(get_db),
    intervention_id: int,
    intervention_in: InterventionUpdate,
) -> InterventionResponse:
    """
    Update an intervention.
    """
    intervention_obj = intervention.get(db=db, id=intervention_id)
    if not intervention_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    intervention_obj = intervention.update(db=db, db_obj=intervention_obj, obj_in=intervention_in)
    return intervention_obj


@router.delete("/{intervention_id}", response_model=InterventionResponse)
def delete_intervention(
    *,
    db: Session = Depends(get_db),
    intervention_id: int,
) -> InterventionResponse:
    """
    Delete an intervention.
    """
    intervention_obj = intervention.delete(db=db, id=intervention_id)
    if not intervention_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    return intervention_obj


@router.get("/operator/{operator}", response_model=List[InterventionResponse])
def read_interventions_by_operator(
    *,
    db: Session = Depends(get_db),
    operator: str,
) -> List[InterventionResponse]:
    """
    Get all interventions by a specific operator.
    """
    interventions = intervention.get_by_operator(db=db, operator=operator)
    return interventions


@router.get("/type/{intervention_type}", response_model=List[InterventionResponse])
def read_interventions_by_type(
    *,
    db: Session = Depends(get_db),
    intervention_type: str,
) -> List[InterventionResponse]:
    """
    Get all interventions of a specific type.
    """
    interventions = intervention.get_by_type(db=db, intervention_type=intervention_type)
    return interventions


@router.get("/status/{status}", response_model=List[InterventionResponse])
def read_interventions_by_status(
    *,
    db: Session = Depends(get_db),
    status: str,
) -> List[InterventionResponse]:
    """
    Get all interventions with a specific status.
    """
    interventions = intervention.get_by_status(db=db, status=status)
    return interventions


@router.get("/stats/total-capacity")
def get_total_capacity(
    db: Session = Depends(get_db),
) -> dict:
    """
    Get total CO2 removal capacity across all interventions.
    """
    total_capacity = intervention.get_total_capacity(db=db)
    return {"total_capacity_tonnes_co2": total_capacity}


@router.get("/stats/capacity-by-type")
def get_capacity_by_type(
    db: Session = Depends(get_db),
) -> List[dict]:
    """
    Get CO2 removal capacity grouped by intervention type.
    """
    capacity_by_type = intervention.get_capacity_by_type(db=db)
    return capacity_by_type 