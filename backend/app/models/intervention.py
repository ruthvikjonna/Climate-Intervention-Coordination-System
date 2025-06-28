from sqlalchemy import Column, String, Float, DateTime, Date, Integer, JSON, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_id = Column(UUID(as_uuid=True), ForeignKey("operators.id"), nullable=False)
    grid_cell_id = Column(UUID(as_uuid=True), ForeignKey("climate_grid_cells.id"), nullable=False)
    
    # Basic info
    name = Column(String, nullable=False)
    description = Column(String)
    intervention_type = Column(String, nullable=False)  # "biochar", "DAC", "afforestation", "SRM", etc.
    status = Column(String, nullable=False)  # "planned", "active", "completed", "failed"
    
    # Location data
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region_name = Column(String)
    
    # Scale and impact
    scale_amount = Column(Float, nullable=False)  # tonnes, hectares, etc.
    scale_unit = Column(String, nullable=False)  # "tonnes_co2", "hectares", "kg_aerosol"
    cost_usd = Column(Float)
    
    # Timeline
    start_date = Column(Date)
    end_date = Column(Date)
    duration_months = Column(Integer)
    
    # Tracking
    deployment_data = Column(JSON)  # specific intervention details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    operator = relationship("Operator", back_populates="interventions")
    grid_cell = relationship("ClimateGridCell", back_populates="interventions")
    impacts = relationship("InterventionImpact", back_populates="intervention")

    # Indexes for performance
    __table_args__ = (
        Index('idx_interventions_geospatial', 'latitude', 'longitude'),
        Index('idx_interventions_operator', 'operator_id'),
        Index('idx_interventions_grid_cell', 'grid_cell_id'),
        Index('idx_interventions_type', 'intervention_type'),
        Index('idx_interventions_status', 'status'),
        Index('idx_interventions_timeline', 'start_date', 'end_date'),
    )