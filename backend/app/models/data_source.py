from sqlalchemy import Column, Integer, Float, DateTime, String, Text, JSON, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Source information
    source_type = Column(String(50), nullable=False)             # Type (satellite, ground_station, model, etc.)
    provider = Column(String(100), nullable=True)                # Data provider
    url = Column(String(500), nullable=True)                     # Source URL
    api_endpoint = Column(String(500), nullable=True)            # API endpoint if applicable
    
    # Data characteristics
    data_format = Column(String(50), nullable=True)              # Data format (JSON, CSV, NetCDF, etc.)
    update_frequency = Column(String(50), nullable=True)         # Update frequency (hourly, daily, etc.)
    spatial_resolution = Column(Float, nullable=True)            # Spatial resolution in degrees
    temporal_resolution = Column(String(50), nullable=True)      # Temporal resolution
    
    # Coverage
    geographic_coverage = Column(JSON, nullable=True)            # Geographic coverage bounds
    temporal_coverage = Column(JSON, nullable=True)              # Temporal coverage (start/end dates)
    
    # Quality and reliability
    data_quality_score = Column(Float, nullable=True)            # Overall data quality score (0-1)
    reliability_score = Column(Float, nullable=True)             # Reliability score (0-1)
    accuracy_metrics = Column(JSON, nullable=True)               # Accuracy metrics
    
    # Access and authentication
    requires_authentication = Column(Boolean, default=False)     # Whether authentication is required
    authentication_method = Column(String(50), nullable=True)    # Authentication method
    rate_limits = Column(JSON, nullable=True)                    # Rate limits if applicable
    
    # Cost and licensing
    cost_per_request = Column(Float, nullable=True)              # Cost per API request
    cost_per_month = Column(Float, nullable=True)                # Monthly cost
    licensing_terms = Column(Text, nullable=True)                # Licensing terms
    
    # Technical details
    api_version = Column(String(20), nullable=True)              # API version
    supported_parameters = Column(JSON, nullable=True)           # Supported parameters
    data_schema = Column(JSON, nullable=True)                    # Data schema
    
    # Status and monitoring
    is_active = Column(Boolean, default=True)                    # Whether source is active
    last_successful_fetch = Column(DateTime(timezone=True), nullable=True)  # Last successful data fetch
    last_error = Column(Text, nullable=True)                     # Last error message
    error_count = Column(Integer, default=0)                     # Error count
    
    # Configuration
    config = Column(JSON, nullable=True)                         # Configuration parameters
    headers = Column(JSON, nullable=True)                        # HTTP headers for API calls
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_data_sources_type', 'source_type'),
        Index('idx_data_sources_active', 'is_active'),
        Index('idx_data_sources_provider', 'provider'),
    ) 