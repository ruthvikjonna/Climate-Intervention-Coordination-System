from sqlalchemy import Column, Integer, Float, DateTime, String, Text, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class SatelliteData(Base):
    __tablename__ = "satellite_data"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grid_cell_id = Column(UUID(as_uuid=True), ForeignKey("climate_grid_cells.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Climate metrics
    temperature = Column(Float, nullable=True)  # Temperature in Celsius
    humidity = Column(Float, nullable=True)     # Relative humidity percentage
    pressure = Column(Float, nullable=True)     # Atmospheric pressure in hPa
    wind_speed = Column(Float, nullable=True)   # Wind speed in m/s
    wind_direction = Column(Float, nullable=True)  # Wind direction in degrees
    precipitation = Column(Float, nullable=True)   # Precipitation in mm
    
    # Aerosol and atmospheric composition
    aerosol_optical_depth = Column(Float, nullable=True)  # AOD at 550nm
    co2_concentration = Column(Float, nullable=True)      # CO2 concentration in ppm
    methane_concentration = Column(Float, nullable=True)  # Methane concentration in ppb
    
    # Solar radiation
    solar_irradiance = Column(Float, nullable=True)       # Solar irradiance in W/m²
    albedo = Column(Float, nullable=True)                 # Surface albedo
    
    # Metadata
    satellite_id = Column(String(50), nullable=False)     # Satellite identifier
    instrument = Column(String(50), nullable=True)        # Instrument used
    data_quality = Column(Float, nullable=True)           # Data quality score (0-1)
    processing_level = Column(String(20), nullable=True)  # Processing level (L1, L2, etc.)
    
    # Raw data and flags
    raw_data = Column(JSON, nullable=True)                # Raw satellite data
    quality_flags = Column(JSON, nullable=True)           # Quality flags
    uncertainty = Column(JSON, nullable=True)             # Uncertainty estimates
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationships
    grid_cell = relationship("ClimateGridCell", back_populates="satellite_data")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_satellite_data_grid_timestamp', 'grid_cell_id', 'timestamp'),
        Index('idx_satellite_data_timestamp', 'timestamp'),
        Index('idx_satellite_data_satellite', 'satellite_id'),
    ) 