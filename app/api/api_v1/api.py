from fastapi import APIRouter
from app.api.api_v1.endpoints import health, models

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(models.router, prefix="/models", tags=["models"])