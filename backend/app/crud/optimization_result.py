from typing import List, Optional, Dict, Any
from uuid import UUID
# TODO: Refactor this CRUD module for Supabase. All SQLAlchemy code removed.

from app.schemas.optimization_result import OptimizationResult
from app.schemas.optimization_result import OptimizationResultCreate, OptimizationResultUpdate
from app.core.supabase_client import get_supabase


def create_optimization_result(data: dict):
    response = get_supabase().table("optimization_results").insert(data).execute()
    return response.data


def get_optimization_result_by_id(id: str):
    response = get_supabase().table("optimization_results").select("*").eq("id", id).single().execute()
    return response.data


def update_optimization_result(id: str, data: dict):
    response = get_supabase().table("optimization_results").update(data).eq("id", id).execute()
    return response.data


def delete_optimization_result(id: str):
    response = get_supabase().table("optimization_results").delete().eq("id", id).execute()
    return response.data


def get_optimization_results_by_operator(operator_id: UUID, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    response = get_supabase().table("optimization_results").select("*").eq("operator_id", str(operator_id)).order_by("timestamp", desc=True).range(skip, skip+limit-1).execute()
    return response.data


def get_optimization_results_by_grid_cell(grid_cell_id: UUID, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    response = get_supabase().table("optimization_results").select("*").eq("grid_cell_id", str(grid_cell_id)).order_by("timestamp", desc=True).range(skip, skip+limit-1).execute()
    return response.data


def get_optimization_results_by_type(optimization_type: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    response = get_supabase().table("optimization_results").select("*").eq("optimization_type", optimization_type).order_by("timestamp", desc=True).range(skip, skip+limit-1).execute()
    return response.data


def get_optimization_results_by_algorithm(algorithm: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    response = get_supabase().table("optimization_results").select("*").eq("algorithm", algorithm).order_by("timestamp", desc=True).range(skip, skip+limit-1).execute()
    return response.data


def get_optimization_results_by_status(status: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    response = get_supabase().table("optimization_results").select("*").eq("status", status).order_by("timestamp", desc=True).range(skip, skip+limit-1).execute()
    return response.data


def get_best_optimization_results(limit: int = 10, optimization_type: Optional[str] = None, grid_cell_id: Optional[UUID] = None) -> List[Dict[str, Any]]:
    query = get_supabase().table("optimization_results").select("*").neq("objective_value", None).eq("status", "completed")
    if optimization_type:
        query = query.eq("optimization_type", optimization_type)
    if grid_cell_id:
        query = query.eq("grid_cell_id", str(grid_cell_id))
    response = query.order_by("objective_value", desc=True).limit(limit).execute()
    return response.data


def get_optimization_statistics(operator_id: Optional[UUID] = None, grid_cell_id: Optional[UUID] = None, optimization_type: Optional[str] = None, algorithm: Optional[str] = None) -> Dict[str, Any]:
    query = get_supabase().table("optimization_results").select("*")
    if operator_id:
        query = query.eq("operator_id", str(operator_id))
    if grid_cell_id:
        query = query.eq("grid_cell_id", str(grid_cell_id))
    if optimization_type:
        query = query.eq("optimization_type", optimization_type)
    if algorithm:
        query = query.eq("algorithm", algorithm)
    response = query.execute()
    data = response.data or []
    stats = {
        "total_results": len(data),
        "completed_results": len([r for r in data if r.get("status") == "completed"]),
        "failed_results": len([r for r in data if r.get("status") == "failed"]),
        "running_results": len([r for r in data if r.get("status") == "running"]),
        "avg_execution_time": sum(r.get("execution_time", 0) for r in data if r.get("execution_time") is not None) / len(data) if data else 0,
        "avg_iterations": sum(r.get("iterations", 0) for r in data if r.get("iterations") is not None) / len(data) if data else 0,
        "avg_validation_score": sum(r.get("validation_score", 0) for r in data if r.get("validation_score") is not None) / len(data) if data else 0,
        "best_objective_value": max((r.get("objective_value", float('-inf')) for r in data if r.get("objective_value") is not None), default=None),
    }
    return stats


def get_optimization_result_list(skip: int = 0, limit: int = 100, operator_id: Optional[UUID] = None, grid_cell_id: Optional[UUID] = None, optimization_type: Optional[str] = None, algorithm: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    query = get_supabase().table("optimization_results").select("*")
    if operator_id:
        query = query.eq("operator_id", str(operator_id))
    if grid_cell_id:
        query = query.eq("grid_cell_id", str(grid_cell_id))
    if optimization_type:
        query = query.eq("optimization_type", optimization_type)
    if algorithm:
        query = query.eq("algorithm", algorithm)
    if status:
        query = query.eq("status", status)
    response = query.order_by("timestamp", desc=True).range(skip, skip+limit-1).execute()
    return response.data 