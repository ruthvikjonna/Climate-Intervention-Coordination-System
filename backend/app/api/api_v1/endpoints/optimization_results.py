from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from uuid import UUID
from app.crud.optimization_result import (
    create_optimization_result,
    get_optimization_result_by_id,
    update_optimization_result,
    delete_optimization_result,
)

# TODO: Refactor this endpoint for Supabase. All SQLAlchemy code removed.

router = APIRouter()


@router.post("/")
def create(data: dict):
    result = create_optimization_result(data)
    if not result:
        raise HTTPException(status_code=400, detail="Insert failed")
    return result


@router.get("/{id}")
def read(id: str):
    result = get_optimization_result_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result


@router.put("/{id}")
def update(id: str, data: dict):
    result = update_optimization_result(id, data)
    if not result:
        raise HTTPException(status_code=400, detail="Update failed")
    return result


@router.delete("/{id}")
def delete(id: str):
    result = delete_optimization_result(id)
    if not result:
        raise HTTPException(status_code=400, detail="Delete failed")
    return result


@router.get("/", response_model=List[OptimizationResult])
def get_optimization_result_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    operator_id: Optional[UUID] = Query(None),
    grid_cell_id: Optional[UUID] = Query(None),
    optimization_type: Optional[str] = Query(None),
    algorithm: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of optimization results with optional filters"""
    return crud.get_optimization_result_list(
        db=db,
        skip=skip,
        limit=limit,
        operator_id=operator_id,
        grid_cell_id=grid_cell_id,
        optimization_type=optimization_type,
        algorithm=algorithm,
        status=status
    )


@router.get("/operator/{operator_id}", response_model=List[OptimizationResult])
def get_optimization_results_by_operator(
    operator_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all optimization results for a specific operator"""
    return crud.get_optimization_results_by_operator(
        db=db,
        operator_id=operator_id,
        skip=skip,
        limit=limit
    )


@router.get("/grid-cell/{grid_cell_id}", response_model=List[OptimizationResult])
def get_optimization_results_by_grid_cell(
    grid_cell_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get optimization results for a specific grid cell"""
    return crud.get_optimization_results_by_grid_cell(
        db=db,
        grid_cell_id=grid_cell_id,
        skip=skip,
        limit=limit
    )


@router.get("/type/{optimization_type}", response_model=List[OptimizationResult])
def get_optimization_results_by_type(
    optimization_type: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get optimization results by type"""
    return crud.get_optimization_results_by_type(
        db=db,
        optimization_type=optimization_type,
        skip=skip,
        limit=limit
    )


@router.get("/algorithm/{algorithm}", response_model=List[OptimizationResult])
def get_optimization_results_by_algorithm(
    algorithm: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get optimization results by algorithm"""
    return crud.get_optimization_results_by_algorithm(
        db=db,
        algorithm=algorithm,
        skip=skip,
        limit=limit
    )


@router.get("/status/{status}", response_model=List[OptimizationResult])
def get_optimization_results_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get optimization results by status"""
    return crud.get_optimization_results_by_status(
        db=db,
        status=status,
        skip=skip,
        limit=limit
    )


@router.get("/best-performing/", response_model=List[OptimizationResult])
def get_best_optimization_results(
    limit: int = Query(10, ge=1, le=100),
    optimization_type: Optional[str] = Query(None),
    grid_cell_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """Get the best optimization results based on objective value"""
    return crud.get_best_optimization_results(
        db=db,
        limit=limit,
        optimization_type=optimization_type,
        grid_cell_id=grid_cell_id
    )


@router.get("/statistics/")
def get_optimization_statistics(
    operator_id: Optional[UUID] = Query(None),
    grid_cell_id: Optional[UUID] = Query(None),
    optimization_type: Optional[str] = Query(None),
    algorithm: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get statistics for optimization results"""
    return crud.get_optimization_statistics(
        db=db,
        operator_id=operator_id,
        grid_cell_id=grid_cell_id,
        optimization_type=optimization_type,
        algorithm=algorithm
    ) 