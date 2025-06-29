from typing import List, Optional, Dict, Any
# TODO: Refactor this CRUD module for Supabase. All SQLAlchemy code removed.

from app.models.intervention_impact import InterventionImpact
from app.schemas.intervention_impact import InterventionImpactCreate, InterventionImpactUpdate


def create_intervention_impact(db: Session, impact: InterventionImpactCreate) -> InterventionImpact:
    """Create a new intervention impact record"""
    db_impact = InterventionImpact(**impact.model_dump())
    db.add(db_impact)
    db.commit()
    db.refresh(db_impact)
    return db_impact


def get_intervention_impact(db: Session, impact_id: UUID) -> Optional[InterventionImpact]:
    """Get intervention impact by ID"""
    return db.query(InterventionImpact).filter(InterventionImpact.id == impact_id).first()


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


def update_intervention_impact(
    db: Session, 
    impact_id: UUID, 
    impact_update: InterventionImpactUpdate
) -> Optional[InterventionImpact]:
    """Update intervention impact"""
    db_impact = get_intervention_impact(db, impact_id)
    if db_impact:
        update_data = impact_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_impact, field, value)
        db.commit()
        db.refresh(db_impact)
    return db_impact


def delete_intervention_impact(db: Session, impact_id: UUID) -> bool:
    """Delete intervention impact"""
    db_impact = get_intervention_impact(db, impact_id)
    if db_impact:
        db.delete(db_impact)
        db.commit()
        return True
    return False


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