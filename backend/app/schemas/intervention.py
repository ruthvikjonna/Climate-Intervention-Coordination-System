from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class InterventionBase(BaseModel):
    """Base schema for intervention data"""
    name: str = Field(..., description="Name of the intervention")
    description: Optional[str] = Field(None, description="Description of the intervention")
    intervention_type: str = Field(..., description="Type of intervention (e.g., biochar, DAC, reforestation)")
    location_lat: float = Field(..., description="Latitude of intervention location")
    location_lon: float = Field(..., description="Longitude of intervention location")
    deployment_date: datetime = Field(..., description="Date when intervention was deployed")
    capacity_tonnes_co2: float = Field(..., description="CO2 removal capacity in tonnes")
    status: str = Field(..., description="Current status of the intervention")
    operator: str = Field(..., description="Organization or entity operating the intervention")
    cost_per_tonne: Optional[float] = Field(None, description="Cost per tonne of CO2 removed")
    technology_readiness_level: Optional[int] = Field(None, ge=1, le=9, description="Technology readiness level (1-9)")
    verification_method: Optional[str] = Field(None, description="Method used to verify CO2 removal")
    expected_lifetime_years: Optional[int] = Field(None, description="Expected operational lifetime in years")


class InterventionCreate(InterventionBase):
    """Schema for creating a new intervention"""
    pass


class InterventionUpdate(BaseModel):
    """Schema for updating an intervention - all fields optional"""
    name: Optional[str] = Field(None, description="Name of the intervention")
    description: Optional[str] = Field(None, description="Description of the intervention")
    intervention_type: Optional[str] = Field(None, description="Type of intervention")
    location_lat: Optional[float] = Field(None, description="Latitude of intervention location")
    location_lon: Optional[float] = Field(None, description="Longitude of intervention location")
    deployment_date: Optional[datetime] = Field(None, description="Date when intervention was deployed")
    capacity_tonnes_co2: Optional[float] = Field(None, description="CO2 removal capacity in tonnes")
    status: Optional[str] = Field(None, description="Current status of the intervention")
    operator: Optional[str] = Field(None, description="Organization or entity operating the intervention")
    cost_per_tonne: Optional[float] = Field(None, description="Cost per tonne of CO2 removed")
    technology_readiness_level: Optional[int] = Field(None, ge=1, le=9, description="Technology readiness level (1-9)")
    verification_method: Optional[str] = Field(None, description="Method used to verify CO2 removal")
    expected_lifetime_years: Optional[int] = Field(None, description="Expected operational lifetime in years")


class InterventionInDB(InterventionBase):
    """Schema for intervention as stored in database"""
    id: int = Field(..., description="Unique identifier for the intervention")
    created_at: datetime = Field(..., description="Timestamp when record was created")
    updated_at: datetime = Field(..., description="Timestamp when record was last updated")

    class Config:
        from_attributes = True


class InterventionResponse(InterventionInDB):
    """Schema for intervention API responses"""
    pass


class InterventionListResponse(BaseModel):
    """Schema for paginated list of interventions"""
    interventions: list[InterventionResponse] = Field(..., description="List of interventions")
    total: int = Field(..., description="Total number of interventions")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages") 