# app/models/organization.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String(100), nullable=False, unique=True)
    org_type = Column(ENUM('winery', 'vineyard', 'orchard', 'farm', 'coffee_estate', 'processing_facility', name='org_type_enum'), nullable=False)
    
    # Context-driven UX fields
    agricultural_profile = Column(JSON)  # Crops grown, processing types, business model
    ui_preferences = Column(JSON)  # Enabled modules, dashboard layout, terminology
    
    subscription_tier = Column(ENUM('free', 'basic', 'premium', 'enterprise', name='subscription_tier_enum'), default='free')
    timezone = Column(String(50), default='America/Los_Angeles')
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="organization")
    properties = relationship("Property", back_populates="organization")