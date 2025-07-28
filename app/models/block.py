# app/models/block.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Block(Base):
    __tablename__ = "blocks"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    block_name = Column(String(100), nullable=False)
    
    # Universal crop support
    crop_type = Column(ENUM('grape', 'apple', 'cherry', 'pear', 'coffee', 'avocado', 'citrus', 'stone_fruit', 'berry', 'nut', 'other', name='crop_type_enum'), nullable=False)
    variety = Column(String(50))  # Crop variety/cultivar
    
    # Enhanced genetics tracking
    primary_variety = Column(String(50))
    primary_clone = Column(String(50))
    primary_rootstock = Column(String(50))
    mixed_genetics = Column(Boolean, default=False)
    
    # Physical layout
    row_count = Column(Integer)
    row_spacing_ft = Column(DECIMAL(5,2))
    vine_spacing_ft = Column(DECIMAL(5,2))
    
    # GPS location using simple lat/lng
    center_latitude = Column(DECIMAL(10,8))
    center_longitude = Column(DECIMAL(11,8))
    boundary_radius_meters = Column(DECIMAL(10,2))  # Radius for circular boundary
    
    # Planting details (keeping existing fields)
    rootstock = Column(String(50))
    clone = Column(String(50))
    planting_year = Column(Integer)
    planting_density = Column(Integer)  # Plants per acre
    
    # Management details
    trellis_system = Column(String(100))
    training_method = Column(String(100))
    harvest_method = Column(ENUM('hand_picked', 'machine_harvested', 'strip_picked', 'selective_pick', name='harvest_method_enum'))
    processing_type = Column(String(100))  # Intended use (fresh, juice, dried, etc.)
    
    # Physical characteristics
    acres = Column(DECIMAL(6,2))
    slope_degree = Column(DECIMAL(4,1))
    aspect = Column(ENUM('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', name='aspect_enum'))
    soil_type = Column(String(100))
    
    # Status flags
    is_organic = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    property = relationship("Property", back_populates="blocks")
    activities = relationship("Activity", back_populates="block")
    rows = relationship("Row", back_populates="block")