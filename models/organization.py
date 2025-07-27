from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class OrgTypeEnum(enum.Enum):
    winery = "winery"
    vineyard = "vineyard" 
    orchard = "orchard"
    farm = "farm"
    coffee_estate = "coffee_estate"

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String(100), nullable=False, unique=True)
    org_type = Column(Enum(OrgTypeEnum), nullable=False)
    
    # Context-driven UX fields
    agricultural_profile = Column(JSON)
    ui_preferences = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())