from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class InterventionImpactBase(BaseModel):
    intervention_id: UUID
    grid_cell_id: UUID
    timestamp: datetime
    temperature_change: Optional[float] = None
    humidity_change: Optional[float] = None
    pressure_change: Optional[float] = None
    wind_speed_change: Optional[float] = None
    aerosol_optical_depth_change: Optional[float] = None
    co2_concentration_change: Optional[float] = None
    methane_concentration_change: Optional[float] = None
    solar_irradiance_change: Optional[float] = None
    albedo_change: Optional[float] = None
    effectiveness_score: Optional[float] = None
    confidence_level: Optional[float] = None
    cost_per_degree: Optional[float] = None
    efficiency_ratio: Optional[float] = None
    environmental_impact_score: Optional[float] = None
    side_effects: Optional[Dict[str, Any]] = None
    analysis_method: Optional[str] = None
    baseline_period: Optional[Dict[str, Any]] = None
    comparison_period: Optional[Dict[str, Any]] = None
    uncertainty_estimates: Optional[Dict[str, Any]] = None
    validation_status: Optional[str] = None
    peer_review_status: Optional[str] = None


class InterventionImpactCreate(InterventionImpactBase):
    pass


class InterventionImpactUpdate(BaseModel):
    temperature_change: Optional[float] = None
    humidity_change: Optional[float] = None
    pressure_change: Optional[float] = None
    wind_speed_change: Optional[float] = None
    aerosol_optical_depth_change: Optional[float] = None
    co2_concentration_change: Optional[float] = None
    methane_concentration_change: Optional[float] = None
    solar_irradiance_change: Optional[float] = None
    albedo_change: Optional[float] = None
    effectiveness_score: Optional[float] = None
    confidence_level: Optional[float] = None
    cost_per_degree: Optional[float] = None
    efficiency_ratio: Optional[float] = None
    environmental_impact_score: Optional[float] = None
    side_effects: Optional[Dict[str, Any]] = None
    analysis_method: Optional[str] = None
    baseline_period: Optional[Dict[str, Any]] = None
    comparison_period: Optional[Dict[str, Any]] = None
    uncertainty_estimates: Optional[Dict[str, Any]] = None
    validation_status: Optional[str] = None
    peer_review_status: Optional[str] = None


class InterventionImpactInDB(InterventionImpactBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InterventionImpact(InterventionImpactInDB):
    pass 