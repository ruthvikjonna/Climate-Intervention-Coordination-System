from typing import List, Optional, Tuple
from supabase import Client
from datetime import datetime
from uuid import UUID

from app.schemas.intervention import InterventionCreate, InterventionUpdate, InterventionInDB
from app.core.supabase_client import supabase


class InterventionCRUD:
    """CRUD operations for Intervention model using Supabase"""

    def create(self, supabase: Client, obj_in: InterventionCreate) -> InterventionInDB:
        """Create a new intervention"""
        obj_data = obj_in.model_dump(exclude_none=True)
        
        # Insert into Supabase
        response = supabase.table("interventions").insert(obj_data).execute()
        
        if not response.data:
            raise Exception("Failed to create intervention")
        
        return InterventionInDB(**response.data[0])

    def get(self, supabase: Client, id: UUID) -> Optional[InterventionInDB]:
        """Get intervention by ID"""
        response = supabase.table("interventions").select("*").eq("id", str(id)).single().execute()
        
        if not response.data:
            return None
        
        return InterventionInDB(**response.data)

    def get_multi(
        self, 
        supabase: Client, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        intervention_type: Optional[str] = None,
        operator_id: Optional[UUID] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[InterventionInDB], int]:
        """Get multiple interventions with optional filtering and pagination"""
        query = supabase.table("interventions").select("*", count="exact")
        
        # Apply filters
        if intervention_type:
            query = query.eq("intervention_type", intervention_type)
        if operator_id:
            query = query.eq("operator_id", str(operator_id))
        if status:
            query = query.eq("status", status)
        if search:
            query = query.or_(f"name.ilike.%{search}%,description.ilike.%{search}%")
        
        # Apply pagination
        query = query.range(skip, skip + limit - 1)
        
        response = query.execute()
        
        interventions = [InterventionInDB(**item) for item in response.data]
        total = response.count or 0
        
        return interventions, total

    def update(
        self, 
        supabase: Client, 
        *, 
        id: UUID,
        obj_in: InterventionUpdate
    ) -> Optional[InterventionInDB]:
        """Update an intervention"""
        update_data = obj_in.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_data:
            return self.get(supabase, id)
        
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = supabase.table("interventions").update(update_data).eq("id", str(id)).execute()
        
        if not response.data:
            return None
        
        return InterventionInDB(**response.data[0])

    def delete(self, supabase: Client, *, id: UUID) -> bool:
        """Delete an intervention"""
        response = supabase.table("interventions").delete().eq("id", str(id)).execute()
        return len(response.data) > 0

    def get_by_operator(self, supabase: Client, operator_id: UUID) -> List[InterventionInDB]:
        """Get all interventions by a specific operator"""
        response = supabase.table("interventions").select("*").eq("operator_id", str(operator_id)).execute()
        return [InterventionInDB(**item) for item in response.data]

    def get_by_type(self, supabase: Client, intervention_type: str) -> List[InterventionInDB]:
        """Get all interventions of a specific type"""
        response = supabase.table("interventions").select("*").eq("intervention_type", intervention_type).execute()
        return [InterventionInDB(**item) for item in response.data]

    def get_by_status(self, supabase: Client, status: str) -> List[InterventionInDB]:
        """Get all interventions with a specific status"""
        response = supabase.table("interventions").select("*").eq("status", status).execute()
        return [InterventionInDB(**item) for item in response.data]

    def get_total_capacity(self, supabase: Client) -> float:
        """Get total scale amount across all interventions"""
        response = supabase.table("interventions").select("scale_amount").execute()
        return sum(item.get("scale_amount", 0) for item in response.data)

    def get_capacity_by_type(self, supabase: Client) -> List[dict]:
        """Get scale amount grouped by intervention type"""
        response = supabase.table("interventions").select("intervention_type, scale_amount").execute()
        
        # Group by intervention type
        grouped = {}
        for item in response.data:
            intervention_type = item["intervention_type"]
            scale_amount = item.get("scale_amount", 0)
            
            if intervention_type not in grouped:
                grouped[intervention_type] = {"total_scale": 0, "count": 0}
            
            grouped[intervention_type]["total_scale"] += scale_amount
            grouped[intervention_type]["count"] += 1
        
        return [
            {
                "intervention_type": intervention_type,
                "total_scale": data["total_scale"],
                "count": data["count"]
            }
            for intervention_type, data in grouped.items()
        ]


# Create a singleton instance
intervention = InterventionCRUD()

# --- Supabase CRUD Operations for Interventions ---
def create_intervention(data: dict):
    response = supabase.table("interventions").insert(data).execute()
    return response.data

def get_intervention_by_id(id: str):
    response = supabase.table("interventions").select("*").eq("id", id).single().execute()
    return response.data

def update_intervention(id: str, data: dict):
    response = supabase.table("interventions").update(data).eq("id", id).execute()
    return response.data

def delete_intervention(id: str):
    response = supabase.table("interventions").delete().eq("id", id).execute()
    return response.data