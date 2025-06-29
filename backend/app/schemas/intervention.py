from datetime import datetime, date
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class InterventionBase(BaseModel):
    """Base schema for intervention data"""
    operator_id: UUID = Field(..., description="ID of the operator")
    grid_cell_id: UUID = Field(..., description="ID of the climate grid cell")
    name: str = Field(..., description="Name of the intervention")
    description: Optional[str] = Field(None, description="Description of the intervention")
    intervention_type: str = Field(..., description="Type of intervention (e.g., biochar, DAC, afforestation, SRM)")
    status: str = Field(..., description="Current status of the intervention")
    latitude: float = Field(..., description="Latitude of intervention location")
    longitude: float = Field(..., description="Longitude of intervention location")
    region_name: Optional[str] = Field(None, description="Name of the region")
    scale_amount: float = Field(..., description="Scale amount (tonnes, hectares, etc.)")
    scale_unit: str = Field(..., description="Unit of scale (tonnes_co2, hectares, kg_aerosol)")
    cost_usd: Optional[float] = Field(None, description="Cost in USD")
    start_date: Optional[date] = Field(None, description="Start date of intervention")
    end_date: Optional[date] = Field(None, description="End date of intervention")
    duration_months: Optional[int] = Field(None, description="Duration in months")
    deployment_data: Optional[Dict[str, Any]] = Field(None, description="Specific intervention details")


class InterventionCreate(InterventionBase):
    """Schema for creating a new intervention"""
    pass


class InterventionUpdate(BaseModel):
    """Schema for updating an intervention - all fields optional"""
    operator_id: Optional[UUID] = Field(None, description="ID of the operator")
    grid_cell_id: Optional[UUID] = Field(None, description="ID of the climate grid cell")
    name: Optional[str] = Field(None, description="Name of the intervention")
    description: Optional[str] = Field(None, description="Description of the intervention")
    intervention_type: Optional[str] = Field(None, description="Type of intervention")
    status: Optional[str] = Field(None, description="Current status of the intervention")
    latitude: Optional[float] = Field(None, description="Latitude of intervention location")
    longitude: Optional[float] = Field(None, description="Longitude of intervention location")
    region_name: Optional[str] = Field(None, description="Name of the region")
    scale_amount: Optional[float] = Field(None, description="Scale amount")
    scale_unit: Optional[str] = Field(None, description="Unit of scale")
    cost_usd: Optional[float] = Field(None, description="Cost in USD")
    start_date: Optional[date] = Field(None, description="Start date of intervention")
    end_date: Optional[date] = Field(None, description="End date of intervention")
    duration_months: Optional[int] = Field(None, description="Duration in months")
    deployment_data: Optional[Dict[str, Any]] = Field(None, description="Specific intervention details")


class InterventionInDB(InterventionBase):
    """Schema for intervention as stored in database"""
    id: UUID = Field(..., description="Unique identifier for the intervention")
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