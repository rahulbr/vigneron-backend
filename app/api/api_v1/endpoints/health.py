from fastapi import APIRouter
from sqlalchemy import text
from app.db.base import get_db

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "vigneron-backend"}


@router.get("/db")
async def database_health_check():
    """Health check that includes database connectivity."""
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}