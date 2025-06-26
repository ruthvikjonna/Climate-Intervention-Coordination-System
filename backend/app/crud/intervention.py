from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

from app.models.intervention import Intervention
from app.schemas.intervention import InterventionCreate, InterventionUpdate


class InterventionCRUD:
    """CRUD operations for Intervention model"""

    def create(self, db: Session, obj_in: InterventionCreate) -> Intervention:
        """Create a new intervention"""
        db_obj = Intervention(
            name=obj_in.name,
            description=obj_in.description,
            intervention_type=obj_in.intervention_type,
            location_lat=obj_in.location_lat,
            location_lon=obj_in.location_lon,
            deployment_date=obj_in.deployment_date,
            capacity_tonnes_co2=obj_in.capacity_tonnes_co2,
            status=obj_in.status,
            operator=obj_in.operator,
            cost_per_tonne=obj_in.cost_per_tonne,
            technology_readiness_level=obj_in.technology_readiness_level,
            verification_method=obj_in.verification_method,
            expected_lifetime_years=obj_in.expected_lifetime_years,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Intervention]:
        """Get intervention by ID"""
        return db.query(Intervention).filter(Intervention.id == id).first()

    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        intervention_type: Optional[str] = None,
        operator: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[Intervention], int]:
        """Get multiple interventions with optional filtering and pagination"""
        query = db.query(Intervention)
        
        # Apply filters
        if intervention_type:
            query = query.filter(Intervention.intervention_type == intervention_type)
        if operator:
            query = query.filter(Intervention.operator == operator)
        if status:
            query = query.filter(Intervention.status == status)
        if search:
            search_filter = or_(
                Intervention.name.ilike(f"%{search}%"),
                Intervention.description.ilike(f"%{search}%"),
                Intervention.operator.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count for pagination
        total = query.count()
        
        # Apply pagination
        interventions = query.offset(skip).limit(limit).all()
        
        return interventions, total

    def update(
        self, 
        db: Session, 
        *, 
        db_obj: Intervention, 
        obj_in: InterventionUpdate
    ) -> Intervention:
        """Update an intervention"""
        update_data = obj_in.dict(exclude_unset=True)
        
        # Update the updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Intervention]:
        """Delete an intervention"""
        obj = db.query(Intervention).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_operator(self, db: Session, operator: str) -> List[Intervention]:
        """Get all interventions by a specific operator"""
        return db.query(Intervention).filter(Intervention.operator == operator).all()

    def get_by_type(self, db: Session, intervention_type: str) -> List[Intervention]:
        """Get all interventions of a specific type"""
        return db.query(Intervention).filter(Intervention.intervention_type == intervention_type).all()

    def get_by_status(self, db: Session, status: str) -> List[Intervention]:
        """Get all interventions with a specific status"""
        return db.query(Intervention).filter(Intervention.status == status).all()

    def get_total_capacity(self, db: Session) -> float:
        """Get total CO2 removal capacity across all interventions"""
        result = db.query(func.sum(Intervention.capacity_tonnes_co2)).scalar()
        return result or 0.0

    def get_capacity_by_type(self, db: Session) -> List[dict]:
        """Get CO2 removal capacity grouped by intervention type"""
        result = db.query(
            Intervention.intervention_type,
            func.sum(Intervention.capacity_tonnes_co2).label('total_capacity'),
            func.count(Intervention.id).label('count')
        ).group_by(Intervention.intervention_type).all()
        
        return [
            {
                "intervention_type": row.intervention_type,
                "total_capacity": row.total_capacity or 0.0,
                "count": row.count
            }
            for row in result
        ]


# Create a singleton instance
intervention = InterventionCRUD() 