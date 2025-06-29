from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from uuid import UUID

from app.core.database import get_supabase
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
    supabase=Depends(get_supabase),
    intervention_in: InterventionCreate,
) -> InterventionResponse:
    """
    Create a new intervention.
    """
    intervention_obj = intervention.create(supabase=supabase, obj_in=intervention_in)
    return intervention_obj


@router.get("/", response_model=InterventionListResponse)
def read_interventions(
    supabase=Depends(get_supabase),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    intervention_type: Optional[str] = Query(None, description="Filter by intervention type"),
    operator_id: Optional[UUID] = Query(None, description="Filter by operator ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search in name, description, or operator"),
) -> InterventionListResponse:
    """
    Retrieve interventions with optional filtering and pagination.
    """
    interventions, total = intervention.get_multi(
        supabase=supabase,
        skip=skip,
        limit=limit,
        intervention_type=intervention_type,
        operator_id=operator_id,
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
    supabase=Depends(get_supabase),
    intervention_id: UUID,
) -> InterventionResponse:
    """
    Get intervention by ID.
    """
    intervention_obj = intervention.get(supabase=supabase, id=intervention_id)
    if not intervention_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    return intervention_obj


@router.put("/{intervention_id}", response_model=InterventionResponse)
def update_intervention(
    *,
    supabase=Depends(get_supabase),
    intervention_id: UUID,
    intervention_in: InterventionUpdate,
) -> InterventionResponse:
    """
    Update an intervention.
    """
    intervention_obj = intervention.update(supabase=supabase, id=intervention_id, obj_in=intervention_in)
    if not intervention_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    return intervention_obj


@router.delete("/{intervention_id}")
def delete_intervention(
    *,
    supabase=Depends(get_supabase),
    intervention_id: UUID,
) -> dict:
    """
    Delete an intervention.
    """
    success = intervention.delete(supabase=supabase, id=intervention_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    return {"message": "Intervention deleted successfully"}


@router.get("/operator/{operator_id}", response_model=List[InterventionResponse])
def read_interventions_by_operator(
    *,
    supabase=Depends(get_supabase),
    operator_id: UUID,
) -> List[InterventionResponse]:
    """
    Get all interventions by a specific operator.
    """
    interventions = intervention.get_by_operator(supabase=supabase, operator_id=operator_id)
    return interventions


@router.get("/type/{intervention_type}", response_model=List[InterventionResponse])
def read_interventions_by_type(
    *,
    supabase=Depends(get_supabase),
    intervention_type: str,
) -> List[InterventionResponse]:
    """
    Get all interventions of a specific type.
    """
    interventions = intervention.get_by_type(supabase=supabase, intervention_type=intervention_type)
    return interventions


@router.get("/status/{status}", response_model=List[InterventionResponse])
def read_interventions_by_status(
    *,
    supabase=Depends(get_supabase),
    status: str,
) -> List[InterventionResponse]:
    """
    Get all interventions with a specific status.
    """
    interventions = intervention.get_by_status(supabase=supabase, status=status)
    return interventions


@router.get("/stats/total-scale")
def get_total_scale(
    supabase=Depends(get_supabase),
) -> dict:
    """
    Get total scale amount across all interventions.
    """
    total_scale = intervention.get_total_capacity(supabase=supabase)
    return {"total_scale_amount": total_scale}


@router.get("/stats/scale-by-type")
def get_scale_by_type(
    supabase=Depends(get_supabase),
) -> List[dict]:
    """
    Get scale amount grouped by intervention type.
    """
    scale_by_type = intervention.get_capacity_by_type(supabase=supabase)
    return scale_by_type 