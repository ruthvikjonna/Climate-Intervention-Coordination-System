from typing import List, Optional, Tuple
from supabase import Client
from datetime import datetime
from uuid import UUID

from app.schemas.intervention import InterventionCreate, InterventionUpdate, InterventionInDB


class InterventionCRUD:
    """CRUD operations for Intervention model using Supabase"""

    def create(self, supabase: Client, obj_in: InterventionCreate) -> InterventionInDB:
        """Create a new intervention"""
        obj_data = obj_in.model_dump(exclude_none=True)
        
        # Insert into Supabase
        result = supabase.table("interventions").insert(obj_data).execute()
        
        if not result.data:
            raise Exception("Failed to create intervention")
        
        return InterventionInDB(**result.data[0])

    def get(self, supabase: Client, id: UUID) -> Optional[InterventionInDB]:
        """Get intervention by ID"""
        result = supabase.table("interventions").select("*").eq("id", str(id)).execute()
        
        if not result.data:
            return None
        
        return InterventionInDB(**result.data[0])

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
        
        result = query.execute()
        
        interventions = [InterventionInDB(**item) for item in result.data]
        total = result.count or 0
        
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
        
        result = supabase.table("interventions").update(update_data).eq("id", str(id)).execute()
        
        if not result.data:
            return None
        
        return InterventionInDB(**result.data[0])

    def delete(self, supabase: Client, *, id: UUID) -> bool:
        """Delete an intervention"""
        result = supabase.table("interventions").delete().eq("id", str(id)).execute()
        return len(result.data) > 0

    def get_by_operator(self, supabase: Client, operator_id: UUID) -> List[InterventionInDB]:
        """Get all interventions by a specific operator"""
        result = supabase.table("interventions").select("*").eq("operator_id", str(operator_id)).execute()
        return [InterventionInDB(**item) for item in result.data]

    def get_by_type(self, supabase: Client, intervention_type: str) -> List[InterventionInDB]:
        """Get all interventions of a specific type"""
        result = supabase.table("interventions").select("*").eq("intervention_type", intervention_type).execute()
        return [InterventionInDB(**item) for item in result.data]

    def get_by_status(self, supabase: Client, status: str) -> List[InterventionInDB]:
        """Get all interventions with a specific status"""
        result = supabase.table("interventions").select("*").eq("status", status).execute()
        return [InterventionInDB(**item) for item in result.data]

    def get_total_capacity(self, supabase: Client) -> float:
        """Get total scale amount across all interventions"""
        result = supabase.table("interventions").select("scale_amount").execute()
        return sum(item.get("scale_amount", 0) for item in result.data)

    def get_capacity_by_type(self, supabase: Client) -> List[dict]:
        """Get scale amount grouped by intervention type"""
        result = supabase.table("interventions").select("intervention_type, scale_amount").execute()
        
        # Group by intervention type
        grouped = {}
        for item in result.data:
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