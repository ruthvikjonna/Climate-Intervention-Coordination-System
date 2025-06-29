from typing import List, Optional, Dict, Any
# TODO: Refactor this CRUD module for Supabase. All SQLAlchemy code removed.

from app.models.intervention_impact import InterventionImpact
from app.schemas.intervention_impact import InterventionImpactCreate, InterventionImpactUpdate
from app.core.supabase_client import supabase


def create_intervention_impact(data: dict):
    response = supabase.table("intervention_impacts").insert(data).execute()
    return response.data


def get_intervention_impact_by_id(id: str):
    response = supabase.table("intervention_impacts").select("*").eq("id", id).single().execute()
    return response.data


def update_intervention_impact(id: str, data: dict):
    response = supabase.table("intervention_impacts").update(data).eq("id", id).execute()
    return response.data


def delete_intervention_impact(id: str):
    response = supabase.table("intervention_impacts").delete().eq("id", id).execute()
    return response.data


def get_impacts_by_intervention(
    db: Session, 
    intervention_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[InterventionImpact]:
    """Get all impacts for a specific intervention"""
    return db.query(InterventionImpact).filter(
        InterventionImpact.intervention_id == intervention_id
    ).order_by(InterventionImpact.timestamp.desc()).offset(skip).limit(limit).all()


def get_impacts_by_grid_cell(
    db: Session, 
    grid_cell_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[InterventionImpact]:
    """Get impacts for a specific grid cell with optional time filtering"""
    query = db.query(InterventionImpact).filter(InterventionImpact.grid_cell_id == grid_cell_id)
    
    if start_time:
        query = query.filter(InterventionImpact.timestamp >= start_time)
    if end_time:
        query = query.filter(InterventionImpact.timestamp <= end_time)
    
    return query.order_by(InterventionImpact.timestamp.desc()).offset(skip).limit(limit).all()


def get_impacts_by_effectiveness_range(
    db: Session,
    min_effectiveness: float,
    max_effectiveness: float,
    skip: int = 0,
    limit: int = 100
) -> List[InterventionImpact]:
    """Get impacts within a specific effectiveness range"""
    return db.query(InterventionImpact).filter(
        and_(
            InterventionImpact.effectiveness_score >= min_effectiveness,
            InterventionImpact.effectiveness_score <= max_effectiveness
        )
    ).order_by(InterventionImpact.effectiveness_score.desc()).offset(skip).limit(limit).all()


def get_impact_statistics(
    db: Session,
    intervention_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """Get statistics for intervention impacts"""
    query = db.query(InterventionImpact)
    
    if intervention_id:
        query = query.filter(InterventionImpact.intervention_id == intervention_id)
    if grid_cell_id:
        query = query.filter(InterventionImpact.grid_cell_id == grid_cell_id)
    if start_time:
        query = query.filter(InterventionImpact.timestamp >= start_time)
    if end_time:
        query = query.filter(InterventionImpact.timestamp <= end_time)
    
    stats = {
        "total_impacts": query.count(),
        "avg_effectiveness": query.with_entities(func.avg(InterventionImpact.effectiveness_score)).scalar(),
        "avg_confidence": query.with_entities(func.avg(InterventionImpact.confidence_level)).scalar(),
        "avg_temperature_change": query.with_entities(func.avg(InterventionImpact.temperature_change)).scalar(),
        "avg_cost_per_degree": query.with_entities(func.avg(InterventionImpact.cost_per_degree)).scalar(),
        "avg_efficiency_ratio": query.with_entities(func.avg(InterventionImpact.efficiency_ratio)).scalar(),
        "avg_environmental_impact": query.with_entities(func.avg(InterventionImpact.environmental_impact_score)).scalar(),
    }
    
    return stats


def get_best_performing_impacts(
    db: Session,
    limit: int = 10,
    intervention_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None
) -> List[InterventionImpact]:
    """Get the best performing impacts based on effectiveness score"""
    query = db.query(InterventionImpact).filter(
        InterventionImpact.effectiveness_score.isnot(None)
    )
    
    if intervention_id:
        query = query.filter(InterventionImpact.intervention_id == intervention_id)
    if grid_cell_id:
        query = query.filter(InterventionImpact.grid_cell_id == grid_cell_id)
    
    return query.order_by(InterventionImpact.effectiveness_score.desc()).limit(limit).all()


def get_impact_list(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    intervention_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    min_effectiveness: Optional[float] = None
) -> List[InterventionImpact]:
    """Get list of intervention impacts with optional filters"""
    query = db.query(InterventionImpact)
    
    if intervention_id:
        query = query.filter(InterventionImpact.intervention_id == intervention_id)
    if grid_cell_id:
        query = query.filter(InterventionImpact.grid_cell_id == grid_cell_id)
    if start_time:
        query = query.filter(InterventionImpact.timestamp >= start_time)
    if end_time:
        query = query.filter(InterventionImpact.timestamp <= end_time)
    if min_effectiveness is not None:
        query = query.filter(InterventionImpact.effectiveness_score >= min_effectiveness)
    
    return query.order_by(InterventionImpact.timestamp.desc()).offset(skip).limit(limit).all() 