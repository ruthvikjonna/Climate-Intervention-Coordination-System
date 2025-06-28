from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class OptimizationResultBase(BaseModel):
    operator_id: UUID
    grid_cell_id: UUID
    timestamp: datetime
    optimization_type: str
    algorithm: str
    objective_function: Optional[str] = None
    input_constraints: Optional[Dict[str, Any]] = None
    input_data: Optional[Dict[str, Any]] = None
    parameter_bounds: Optional[Dict[str, Any]] = None
    optimal_parameters: Dict[str, Any]
    objective_value: Optional[float] = None
    convergence_status: Optional[str] = None
    execution_time: Optional[float] = None
    iterations: Optional[int] = None
    convergence_iteration: Optional[int] = None
    confidence_interval: Optional[Dict[str, Any]] = None
    uncertainty_analysis: Optional[Dict[str, Any]] = None
    sensitivity_analysis: Optional[Dict[str, Any]] = None
    validation_score: Optional[float] = None
    cross_validation_score: Optional[float] = None
    test_set_performance: Optional[Dict[str, Any]] = None
    recommended_interventions: Optional[Dict[str, Any]] = None
    deployment_strategy: Optional[Dict[str, Any]] = None
    risk_assessment: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    feature_importance: Optional[Dict[str, Any]] = None
    status: str = "completed"
    error_message: Optional[str] = None


class OptimizationResultCreate(OptimizationResultBase):
    pass


class OptimizationResultUpdate(BaseModel):
    objective_function: Optional[str] = None
    input_constraints: Optional[Dict[str, Any]] = None
    input_data: Optional[Dict[str, Any]] = None
    parameter_bounds: Optional[Dict[str, Any]] = None
    optimal_parameters: Optional[Dict[str, Any]] = None
    objective_value: Optional[float] = None
    convergence_status: Optional[str] = None
    execution_time: Optional[float] = None
    iterations: Optional[int] = None
    convergence_iteration: Optional[int] = None
    confidence_interval: Optional[Dict[str, Any]] = None
    uncertainty_analysis: Optional[Dict[str, Any]] = None
    sensitivity_analysis: Optional[Dict[str, Any]] = None
    validation_score: Optional[float] = None
    cross_validation_score: Optional[float] = None
    test_set_performance: Optional[Dict[str, Any]] = None
    recommended_interventions: Optional[Dict[str, Any]] = None
    deployment_strategy: Optional[Dict[str, Any]] = None
    risk_assessment: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    feature_importance: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


class OptimizationResultInDB(OptimizationResultBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OptimizationResult(OptimizationResultInDB):
    pass 