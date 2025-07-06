from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from uuid import UUID

from app.core.supabase_client import get_supabase
from app.crud.intervention import (
    create_intervention,
    get_intervention_by_id,
    update_intervention,
    delete_intervention,
    intervention
)
from app.schemas.intervention import (
    InterventionCreate,
    InterventionUpdate,
    InterventionResponse,
    InterventionListResponse
)

router = APIRouter()


@router.post("/", response_model=InterventionResponse, status_code=status.HTTP_201_CREATED)
def create_intervention_endpoint(
    *,
    supabase=Depends(get_supabase),
    intervention_in: InterventionCreate,
) -> InterventionResponse:
    """
    Create a new intervention.
    """
    result = create_intervention(supabase=supabase, obj_in=intervention_in)
    if not result:
        raise HTTPException(status_code=400, detail="Insert failed")
    return result


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
    result = get_intervention_by_id(supabase=supabase, id=intervention_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intervention not found"
        )
    return result


@router.put("/{intervention_id}", response_model=InterventionResponse)
def update_intervention_endpoint(
    *,
    supabase=Depends(get_supabase),
    intervention_id: UUID,
    intervention_in: InterventionUpdate,
) -> InterventionResponse:
    """
    Update an intervention.
    """
    result = update_intervention(supabase=supabase, id=intervention_id, obj_in=intervention_in)
    if not result:
        raise HTTPException(status_code=400, detail="Update failed")
    return result


@router.delete("/{intervention_id}")
def delete_intervention_endpoint(
    *,
    supabase=Depends(get_supabase),
    intervention_id: UUID,
) -> dict:
    """
    Delete an intervention.
    """
    result = delete_intervention(supabase=supabase, id=intervention_id)
    if not result:
        raise HTTPException(status_code=400, detail="Delete failed")
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