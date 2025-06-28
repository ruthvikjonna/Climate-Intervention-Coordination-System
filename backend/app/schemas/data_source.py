from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class DataSourceBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_type: str
    provider: Optional[str] = None
    url: Optional[str] = None
    api_endpoint: Optional[str] = None
    data_format: Optional[str] = None
    update_frequency: Optional[str] = None
    spatial_resolution: Optional[float] = None
    temporal_resolution: Optional[str] = None
    geographic_coverage: Optional[Dict[str, Any]] = None
    temporal_coverage: Optional[Dict[str, Any]] = None
    data_quality_score: Optional[float] = None
    reliability_score: Optional[float] = None
    accuracy_metrics: Optional[Dict[str, Any]] = None
    requires_authentication: bool = False
    authentication_method: Optional[str] = None
    rate_limits: Optional[Dict[str, Any]] = None
    cost_per_request: Optional[float] = None
    cost_per_month: Optional[float] = None
    licensing_terms: Optional[str] = None
    api_version: Optional[str] = None
    supported_parameters: Optional[Dict[str, Any]] = None
    data_schema: Optional[Dict[str, Any]] = None
    is_active: bool = True
    config: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, Any]] = None


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(BaseModel):
    description: Optional[str] = None
    provider: Optional[str] = None
    url: Optional[str] = None
    api_endpoint: Optional[str] = None
    data_format: Optional[str] = None
    update_frequency: Optional[str] = None
    spatial_resolution: Optional[float] = None
    temporal_resolution: Optional[str] = None
    geographic_coverage: Optional[Dict[str, Any]] = None
    temporal_coverage: Optional[Dict[str, Any]] = None
    data_quality_score: Optional[float] = None
    reliability_score: Optional[float] = None
    accuracy_metrics: Optional[Dict[str, Any]] = None
    requires_authentication: Optional[bool] = None
    authentication_method: Optional[str] = None
    rate_limits: Optional[Dict[str, Any]] = None
    cost_per_request: Optional[float] = None
    cost_per_month: Optional[float] = None
    licensing_terms: Optional[str] = None
    api_version: Optional[str] = None
    supported_parameters: Optional[Dict[str, Any]] = None
    data_schema: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, Any]] = None


class DataSourceInDB(DataSourceBase):
    id: UUID
    last_successful_fetch: Optional[datetime] = None
    last_error: Optional[str] = None
    error_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DataSource(DataSourceInDB):
    pass 