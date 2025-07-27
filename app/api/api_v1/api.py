from fastapi import APIRouter
from app.api.api_v1.endpoints import health, models 
from app.api.api_v1.endpoints import organizations, properties, blocks


api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(
    organizations.router, 
    prefix="/organizations", 
    tags=["organizations"]
)

api_router.include_router(
    properties.router,
    prefix="/properties", 
    tags=["properties"]
)

api_router.include_router(
    blocks.router,
    prefix="/blocks",
    tags=["blocks"]
)