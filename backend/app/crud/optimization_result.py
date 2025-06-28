from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from uuid import UUID

from app.models.optimization_result import OptimizationResult
from app.schemas.optimization_result import OptimizationResultCreate, OptimizationResultUpdate


def create_optimization_result(db: Session, result: OptimizationResultCreate) -> OptimizationResult:
    """Create a new optimization result record"""
    db_result = OptimizationResult(**result.model_dump())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_optimization_result(db: Session, result_id: UUID) -> Optional[OptimizationResult]:
    """Get optimization result by ID"""
    return db.query(OptimizationResult).filter(OptimizationResult.id == result_id).first()


def get_optimization_results_by_operator(
    db: Session, 
    operator_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[OptimizationResult]:
    """Get all optimization results for a specific operator"""
    return db.query(OptimizationResult).filter(
        OptimizationResult.operator_id == operator_id
    ).order_by(OptimizationResult.timestamp.desc()).offset(skip).limit(limit).all()


def get_optimization_results_by_grid_cell(
    db: Session, 
    grid_cell_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[OptimizationResult]:
    """Get optimization results for a specific grid cell"""
    return db.query(OptimizationResult).filter(
        OptimizationResult.grid_cell_id == grid_cell_id
    ).order_by(OptimizationResult.timestamp.desc()).offset(skip).limit(limit).all()


def get_optimization_results_by_type(
    db: Session, 
    optimization_type: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[OptimizationResult]:
    """Get optimization results by type"""
    return db.query(OptimizationResult).filter(
        OptimizationResult.optimization_type == optimization_type
    ).order_by(OptimizationResult.timestamp.desc()).offset(skip).limit(limit).all()


def get_optimization_results_by_algorithm(
    db: Session, 
    algorithm: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[OptimizationResult]:
    """Get optimization results by algorithm"""
    return db.query(OptimizationResult).filter(
        OptimizationResult.algorithm == algorithm
    ).order_by(OptimizationResult.timestamp.desc()).offset(skip).limit(limit).all()


def get_optimization_results_by_status(
    db: Session, 
    status: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[OptimizationResult]:
    """Get optimization results by status"""
    return db.query(OptimizationResult).filter(
        OptimizationResult.status == status
    ).order_by(OptimizationResult.timestamp.desc()).offset(skip).limit(limit).all()


def get_best_optimization_results(
    db: Session,
    limit: int = 10,
    optimization_type: Optional[str] = None,
    grid_cell_id: Optional[UUID] = None
) -> List[OptimizationResult]:
    """Get the best optimization results based on objective value"""
    query = db.query(OptimizationResult).filter(
        and_(
            OptimizationResult.objective_value.isnot(None),
            OptimizationResult.status == "completed"
        )
    )
    
    if optimization_type:
        query = query.filter(OptimizationResult.optimization_type == optimization_type)
    if grid_cell_id:
        query = query.filter(OptimizationResult.grid_cell_id == grid_cell_id)
    
    return query.order_by(OptimizationResult.objective_value.desc()).limit(limit).all()


def get_optimization_statistics(
    db: Session,
    operator_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None,
    optimization_type: Optional[str] = None,
    algorithm: Optional[str] = None
) -> Dict[str, Any]:
    """Get statistics for optimization results"""
    query = db.query(OptimizationResult)
    
    if operator_id:
        query = query.filter(OptimizationResult.operator_id == operator_id)
    if grid_cell_id:
        query = query.filter(OptimizationResult.grid_cell_id == grid_cell_id)
    if optimization_type:
        query = query.filter(OptimizationResult.optimization_type == optimization_type)
    if algorithm:
        query = query.filter(OptimizationResult.algorithm == algorithm)
    
    stats = {
        "total_results": query.count(),
        "completed_results": query.filter(OptimizationResult.status == "completed").count(),
        "failed_results": query.filter(OptimizationResult.status == "failed").count(),
        "running_results": query.filter(OptimizationResult.status == "running").count(),
        "avg_execution_time": query.with_entities(func.avg(OptimizationResult.execution_time)).scalar(),
        "avg_iterations": query.with_entities(func.avg(OptimizationResult.iterations)).scalar(),
        "avg_validation_score": query.with_entities(func.avg(OptimizationResult.validation_score)).scalar(),
        "best_objective_value": query.with_entities(func.max(OptimizationResult.objective_value)).scalar(),
    }
    
    return stats


def update_optimization_result(
    db: Session, 
    result_id: UUID, 
    result_update: OptimizationResultUpdate
) -> Optional[OptimizationResult]:
    """Update optimization result"""
    db_result = get_optimization_result(db, result_id)
    if db_result:
        update_data = result_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_result, field, value)
        db.commit()
        db.refresh(db_result)
    return db_result


def delete_optimization_result(db: Session, result_id: UUID) -> bool:
    """Delete optimization result"""
    db_result = get_optimization_result(db, result_id)
    if db_result:
        db.delete(db_result)
        db.commit()
        return True
    return False


def get_optimization_result_list(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    operator_id: Optional[UUID] = None,
    grid_cell_id: Optional[UUID] = None,
    optimization_type: Optional[str] = None,
    algorithm: Optional[str] = None,
    status: Optional[str] = None
) -> List[OptimizationResult]:
    """Get list of optimization results with optional filters"""
    query = db.query(OptimizationResult)
    
    if operator_id:
        query = query.filter(OptimizationResult.operator_id == operator_id)
    if grid_cell_id:
        query = query.filter(OptimizationResult.grid_cell_id == grid_cell_id)
    if optimization_type:
        query = query.filter(OptimizationResult.optimization_type == optimization_type)
    if algorithm:
        query = query.filter(OptimizationResult.algorithm == algorithm)
    if status:
        query = query.filter(OptimizationResult.status == status)
    
    return query.order_by(OptimizationResult.timestamp.desc()).offset(skip).limit(limit).all() 