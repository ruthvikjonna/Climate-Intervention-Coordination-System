from fastapi import APIRouter

from app.api.api_v1.endpoints import interventions

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    interventions.router,
    prefix="/interventions",
    tags=["interventions"]
) 