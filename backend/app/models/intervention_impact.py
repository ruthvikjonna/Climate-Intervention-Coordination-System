from sqlalchemy import Column, Integer, Float, DateTime, String, Text, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class InterventionImpact(Base):
    __tablename__ = "intervention_impacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intervention_id = Column(UUID(as_uuid=True), ForeignKey("interventions.id"), nullable=False)
    grid_cell_id = Column(UUID(as_uuid=True), ForeignKey("climate_grid_cells.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Impact metrics
    temperature_change = Column(Float, nullable=True)      # Temperature change in Celsius
    humidity_change = Column(Float, nullable=True)         # Humidity change percentage
    pressure_change = Column(Float, nullable=True)         # Pressure change in hPa
    wind_speed_change = Column(Float, nullable=True)       # Wind speed change in m/s
    
    # Aerosol and atmospheric impact
    aerosol_optical_depth_change = Column(Float, nullable=True)  # AOD change
    co2_concentration_change = Column(Float, nullable=True)      # CO2 change in ppm
    methane_concentration_change = Column(Float, nullable=True)  # Methane change in ppb
    
    # Solar radiation impact
    solar_irradiance_change = Column(Float, nullable=True)       # Solar irradiance change in W/m²
    albedo_change = Column(Float, nullable=True)                 # Albedo change
    
    # Effectiveness metrics
    effectiveness_score = Column(Float, nullable=True)           # Overall effectiveness (0-1)
    confidence_level = Column(Float, nullable=True)              # Confidence in measurements (0-1)
    
    # Cost and efficiency
    cost_per_degree = Column(Float, nullable=True)               # Cost per degree Celsius change
    efficiency_ratio = Column(Float, nullable=True)              # Efficiency ratio
    
    # Environmental impact
    environmental_impact_score = Column(Float, nullable=True)    # Environmental impact (0-1, lower is better)
    side_effects = Column(JSON, nullable=True)                   # Side effects assessment
    
    # Analysis metadata
    analysis_method = Column(String(100), nullable=True)         # Method used for analysis
    baseline_period = Column(JSON, nullable=True)                # Baseline period definition
    comparison_period = Column(JSON, nullable=True)              # Comparison period definition
    
    # Uncertainty and validation
    uncertainty_estimates = Column(JSON, nullable=True)          # Uncertainty estimates
    validation_status = Column(String(20), nullable=True)        # Validation status
    peer_review_status = Column(String(20), nullable=True)       # Peer review status
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationships
    intervention = relationship("Intervention", back_populates="impacts")
    grid_cell = relationship("ClimateGridCell", back_populates="intervention_impacts")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_intervention_impacts_intervention', 'intervention_id'),
        Index('idx_intervention_impacts_grid_timestamp', 'grid_cell_id', 'timestamp'),
        Index('idx_intervention_impacts_timestamp', 'timestamp'),
        Index('idx_intervention_impacts_effectiveness', 'effectiveness_score'),
    ) 