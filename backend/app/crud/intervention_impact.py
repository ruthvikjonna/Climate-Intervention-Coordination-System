from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
# TODO: Refactor this CRUD module for Supabase. All SQLAlchemy code removed.

from app.schemas.intervention_impact import InterventionImpact
from app.schemas.intervention_impact import InterventionImpactCreate, InterventionImpactUpdate
from app.core.supabase_client import get_supabase


def create_intervention_impact(data: dict):
    response = get_supabase().table("intervention_impacts").insert(data).execute()
    return response.data


def get_intervention_impact_by_id(id: str):
    response = get_supabase().table("intervention_impacts").select("*").eq("id", id).single().execute()
    return response.data


def update_intervention_impact(id: str, data: dict):
    response = get_supabase().table("intervention_impacts").update(data).eq("id", id).execute()
    return response.data


def delete_intervention_impact(id: str):
    response = get_supabase().table("intervention_impacts").delete().eq("id", id).execute()
    return response.data


def get_impacts_by_intervention(
    intervention_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[InterventionImpact]:
    """Get all impacts for a specific intervention"""
    return get_supabase().table("intervention_impacts").select("*").eq("intervention_id", intervention_id).order_by("timestamp", desc=True).offset(skip).limit(limit).execute().data


def get_impacts_by_grid_cell(
    grid_cell_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[InterventionImpact]:
    """Get impacts for a specific grid cell with optional time filtering"""
    query = get_supabase().table("intervention_impacts").select("*").eq("grid_cell_id", grid_cell_id)
    
    if start_time:
        query = query.filter("timestamp >= ?", start_time)
    if end_time:
        query = query.filter("timestamp <= ?", end_time)
    
    return query.order_by("timestamp", desc=True).offset(skip).limit(limit).execute().data


def get_impacts_by_effectiveness_range(
    min_effectiveness: float,
    max_effectiveness: float,
    skip: int = 0,
    limit: int = 100
) -> List[InterventionImpact]:
    """Get impacts within a specific effectiveness range"""
    return get_supabase().table("intervention_impacts").select("*").filter(
        "effectiveness_score >= ? AND effectiveness_score <= ?",
        min_effectiveness,
        max_effectiveness
    ).order_by("effectiveness_score", desc=True).offset(skip).limit(limit).execute().data


def get_impact_statistics(
    intervention_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """Get statistics for intervention impacts"""
    query = get_supabase().table("intervention_impacts").select("*")
    
    if intervention_id:
        query = query.filter("intervention_id = ?", intervention_id)
    if grid_cell_id:
        query = query.filter("grid_cell_id = ?", grid_cell_id)
    if start_time:
        query = query.filter("timestamp >= ?", start_time)
    if end_time:
        query = query.filter("timestamp <= ?", end_time)
    
    stats = {
        "total_impacts": query.count(),
        "avg_effectiveness": query.with_entities(func.avg("effectiveness_score")).scalar(),
        "avg_confidence": query.with_entities(func.avg("confidence_level")).scalar(),
        "avg_temperature_change": query.with_entities(func.avg("temperature_change")).scalar(),
        "avg_cost_per_degree": query.with_entities(func.avg("cost_per_degree")).scalar(),
        "avg_efficiency_ratio": query.with_entities(func.avg("efficiency_ratio")).scalar(),
        "avg_environmental_impact": query.with_entities(func.avg("environmental_impact_score")).scalar(),
    }
    
    return stats


def get_best_performing_impacts(
    limit: int = 10,
    intervention_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None
) -> List[InterventionImpact]:
    """Get the best performing impacts based on effectiveness score"""
    query = get_supabase().table("intervention_impacts").select("*").filter(
        "effectiveness_score IS NOT NULL"
    )
    
    if intervention_id:
        query = query.filter("intervention_id = ?", intervention_id)
    if grid_cell_id:
        query = query.filter("grid_cell_id = ?", grid_cell_id)
    
    return query.order_by("effectiveness_score", desc=True).limit(limit).execute().data


def get_impact_list(
    skip: int = 0, 
    limit: int = 100,
    intervention_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    min_effectiveness: Optional[float] = None
) -> List[InterventionImpact]:
    """Get list of intervention impacts with optional filters"""
    query = get_supabase().table("intervention_impacts").select("*")
    
    if intervention_id:
        query = query.filter("intervention_id = ?", intervention_id)
    if grid_cell_id:
        query = query.filter("grid_cell_id = ?", grid_cell_id)
    if start_time:
        query = query.filter("timestamp >= ?", start_time)
    if end_time:
        query = query.filter("timestamp <= ?", end_time)
    if min_effectiveness is not None:
        query = query.filter("effectiveness_score >= ?", min_effectiveness)
    
    return query.order_by("timestamp", desc=True).offset(skip).limit(limit).execute().data 