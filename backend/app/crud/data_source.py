from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from uuid import UUID

from app.models.data_source import DataSource
from app.schemas.data_source import DataSourceCreate, DataSourceUpdate


def create_data_source(db: Session, data_source: DataSourceCreate) -> DataSource:
    """Create a new data source record"""
    db_data_source = DataSource(**data_source.model_dump())
    db.add(db_data_source)
    db.commit()
    db.refresh(db_data_source)
    return db_data_source


def get_data_source(db: Session, data_source_id: UUID) -> Optional[DataSource]:
    """Get data source by ID"""
    return db.query(DataSource).filter(DataSource.id == data_source_id).first()


def get_data_source_by_name(db: Session, name: str) -> Optional[DataSource]:
    """Get data source by name"""
    return db.query(DataSource).filter(DataSource.name == name).first()


def get_data_sources_by_type(
    db: Session, 
    source_type: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[DataSource]:
    """Get data sources by type"""
    return db.query(DataSource).filter(
        DataSource.source_type == source_type
    ).order_by(DataSource.name).offset(skip).limit(limit).all()


def get_data_sources_by_provider(
    db: Session, 
    provider: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[DataSource]:
    """Get data sources by provider"""
    return db.query(DataSource).filter(
        DataSource.provider == provider
    ).order_by(DataSource.name).offset(skip).limit(limit).all()


def get_active_data_sources(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[DataSource]:
    """Get all active data sources"""
    return db.query(DataSource).filter(
        DataSource.is_active == True
    ).order_by(DataSource.name).offset(skip).limit(limit).all()


def get_data_sources_by_authentication(
    db: Session, 
    requires_auth: bool, 
    skip: int = 0, 
    limit: int = 100
) -> List[DataSource]:
    """Get data sources by authentication requirement"""
    return db.query(DataSource).filter(
        DataSource.requires_authentication == requires_auth
    ).order_by(DataSource.name).offset(skip).limit(limit).all()


def get_data_sources_by_update_frequency(
    db: Session, 
    frequency: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[DataSource]:
    """Get data sources by update frequency"""
    return db.query(DataSource).filter(
        DataSource.update_frequency == frequency
    ).order_by(DataSource.name).offset(skip).limit(limit).all()


def get_data_source_statistics(db: Session) -> Dict[str, Any]:
    """Get statistics for data sources"""
    total_sources = db.query(DataSource).count()
    active_sources = db.query(DataSource).filter(DataSource.is_active == True).count()
    auth_required = db.query(DataSource).filter(DataSource.requires_authentication == True).count()
    
    # Count by type
    type_counts = db.query(
        DataSource.source_type, 
        func.count(DataSource.id)
    ).group_by(DataSource.source_type).all()
    
    # Count by provider
    provider_counts = db.query(
        DataSource.provider, 
        func.count(DataSource.id)
    ).filter(DataSource.provider.isnot(None)).group_by(DataSource.provider).all()
    
    # Average quality scores
    avg_quality = db.query(func.avg(DataSource.data_quality_score)).scalar()
    avg_reliability = db.query(func.avg(DataSource.reliability_score)).scalar()
    
    stats = {
        "total_sources": total_sources,
        "active_sources": active_sources,
        "inactive_sources": total_sources - active_sources,
        "auth_required": auth_required,
        "no_auth_required": total_sources - auth_required,
        "type_distribution": dict(type_counts),
        "provider_distribution": dict(provider_counts),
        "avg_data_quality": avg_quality,
        "avg_reliability": avg_reliability,
    }
    
    return stats


def update_data_source(
    db: Session, 
    data_source_id: UUID, 
    data_source_update: DataSourceUpdate
) -> Optional[DataSource]:
    """Update data source"""
    db_data_source = get_data_source(db, data_source_id)
    if db_data_source:
        update_data = data_source_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_data_source, field, value)
        db.commit()
        db.refresh(db_data_source)
    return db_data_source


def update_data_source_status(
    db: Session, 
    data_source_id: UUID, 
    is_active: bool,
    last_error: Optional[str] = None
) -> Optional[DataSource]:
    """Update data source status and error information"""
    db_data_source = get_data_source(db, data_source_id)
    if db_data_source:
        db_data_source.is_active = is_active
        if is_active:
            db_data_source.last_successful_fetch = datetime.utcnow()
            db_data_source.last_error = None
        else:
            db_data_source.last_error = last_error
            db_data_source.error_count += 1
        db.commit()
        db.refresh(db_data_source)
    return db_data_source


def delete_data_source(db: Session, data_source_id: UUID) -> bool:
    """Delete data source"""
    db_data_source = get_data_source(db, data_source_id)
    if db_data_source:
        db.delete(db_data_source)
        db.commit()
        return True
    return False


def get_data_source_list(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    source_type: Optional[str] = None,
    provider: Optional[str] = None,
    is_active: Optional[bool] = None,
    requires_auth: Optional[bool] = None
) -> List[DataSource]:
    """Get list of data sources with optional filters"""
    query = db.query(DataSource)
    
    if source_type:
        query = query.filter(DataSource.source_type == source_type)
    if provider:
        query = query.filter(DataSource.provider == provider)
    if is_active is not None:
        query = query.filter(DataSource.is_active == is_active)
    if requires_auth is not None:
        query = query.filter(DataSource.requires_authentication == requires_auth)
    
    return query.order_by(DataSource.name).offset(skip).limit(limit).all()


def search_data_sources(
    db: Session, 
    search_term: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[DataSource]:
    """Search data sources by name or description"""
    return db.query(DataSource).filter(
        or_(
            DataSource.name.ilike(f"%{search_term}%"),
            DataSource.description.ilike(f"%{search_term}%"),
            DataSource.provider.ilike(f"%{search_term}%")
        )
    ).order_by(DataSource.name).offset(skip).limit(limit).all() 