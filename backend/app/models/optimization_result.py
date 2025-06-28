from sqlalchemy import Column, Integer, Float, DateTime, String, Text, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class OptimizationResult(Base):
    __tablename__ = "optimization_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_id = Column(UUID(as_uuid=True), ForeignKey("operators.id"), nullable=False)
    grid_cell_id = Column(UUID(as_uuid=True), ForeignKey("climate_grid_cells.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    
    # Optimization parameters
    optimization_type = Column(String(50), nullable=False)       # Type of optimization (temperature, cost, efficiency)
    algorithm = Column(String(100), nullable=False)              # Algorithm used (genetic, gradient descent, etc.)
    objective_function = Column(Text, nullable=True)             # Objective function definition
    
    # Input parameters
    input_constraints = Column(JSON, nullable=True)              # Input constraints
    input_data = Column(JSON, nullable=True)                     # Input data used
    parameter_bounds = Column(JSON, nullable=True)               # Parameter bounds
    
    # Results
    optimal_parameters = Column(JSON, nullable=False)            # Optimal parameters found
    objective_value = Column(Float, nullable=True)               # Objective function value
    convergence_status = Column(String(20), nullable=True)       # Convergence status
    
    # Performance metrics
    execution_time = Column(Float, nullable=True)                # Execution time in seconds
    iterations = Column(Integer, nullable=True)                  # Number of iterations
    convergence_iteration = Column(Integer, nullable=True)       # Iteration at convergence
    
    # Quality metrics
    confidence_interval = Column(JSON, nullable=True)            # Confidence intervals
    uncertainty_analysis = Column(JSON, nullable=True)           # Uncertainty analysis
    sensitivity_analysis = Column(JSON, nullable=True)           # Sensitivity analysis
    
    # Validation
    validation_score = Column(Float, nullable=True)              # Validation score (0-1)
    cross_validation_score = Column(Float, nullable=True)        # Cross-validation score
    test_set_performance = Column(JSON, nullable=True)           # Test set performance
    
    # Recommendations
    recommended_interventions = Column(JSON, nullable=True)      # Recommended interventions
    deployment_strategy = Column(JSON, nullable=True)            # Deployment strategy
    risk_assessment = Column(JSON, nullable=True)                # Risk assessment
    
    # Metadata
    model_version = Column(String(50), nullable=True)            # Model version
    hyperparameters = Column(JSON, nullable=True)                # Hyperparameters used
    feature_importance = Column(JSON, nullable=True)             # Feature importance scores
    
    # Status
    status = Column(String(20), nullable=False, default="completed")  # Status (running, completed, failed)
    error_message = Column(Text, nullable=True)                 # Error message if failed
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Relationships
    operator = relationship("Operator", back_populates="optimization_results")
    grid_cell = relationship("ClimateGridCell", back_populates="optimization_results")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_optimization_results_operator', 'operator_id'),
        Index('idx_optimization_results_grid_timestamp', 'grid_cell_id', 'timestamp'),
        Index('idx_optimization_results_type', 'optimization_type'),
        Index('idx_optimization_results_status', 'status'),
        Index('idx_optimization_results_algorithm', 'algorithm'),
    ) 