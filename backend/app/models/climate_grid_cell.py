from sqlalchemy import Column, String, Float, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ClimateGridCell(Base):
    __tablename__ = "climate_grid_cells"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    grid_resolution = Column(String, nullable=False)  # "1km", "10km", etc.
    measurement_timestamp = Column(DateTime, nullable=False)
    co2_ppm = Column(Float)
    temperature_celsius = Column(Float)
    biomass_index = Column(Float)
    data_source = Column(String, nullable=False)  # "NASA", "Copernicus", etc.
    source_metadata = Column(JSON)  # API details, satellite info
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    satellite_data = relationship("SatelliteData", back_populates="grid_cell")
    intervention_impacts = relationship("InterventionImpact", back_populates="grid_cell")
    optimization_results = relationship("OptimizationResult", back_populates="grid_cell")
    interventions = relationship("Intervention", back_populates="grid_cell")

    # Indexes for performance
    __table_args__ = (
        Index('idx_climate_grid_geospatial', 'latitude', 'longitude', 'measurement_timestamp'),
        Index('idx_climate_grid_temporal', 'measurement_timestamp'),
        Index('idx_climate_grid_source', 'data_source'),
    ) 