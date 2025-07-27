from typing import Generator
from app.db.base import SessionLocal

def get_db() -> Generator:
    """Get database session"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()