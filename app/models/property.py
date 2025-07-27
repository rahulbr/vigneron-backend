# app/models/property.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    property_name = Column(String(100), nullable=False)
    property_type = Column(ENUM('vineyard', 'orchard', 'ranch', 'farm', 'coffee_estate', name='property_type_enum'), nullable=False)
    
    # Context-aware fields
    primary_crops = Column(JSON)  # ['coffee', 'macadamia'] for this specific property
    business_functions = Column(JSON)  # ['processing', 'direct_sales', 'agritourism']
    
    # Location data
    street_address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(20))
    country_code = Column(String(2), default='US')
    latitude = Column(DECIMAL(10,8))
    longitude = Column(DECIMAL(11,8))
    elevation_ft = Column(Integer)
    
    # Operational data
    total_acres = Column(DECIMAL(8,2))
    planted_acres = Column(DECIMAL(8,2))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="properties")
    blocks = relationship("Block", back_populates="property")