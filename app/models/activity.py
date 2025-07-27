from sqlalchemy import Column, Integer, String, Text, Date, Time, DECIMAL, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ActivityTypeEnum(enum.Enum):
    pruning = "pruning"
    spraying = "spraying"
    fertilizing = "fertilizing"
    cultivation = "cultivation"
    irrigation = "irrigation"
    harvest = "harvest"
    observation = "observation"
    maintenance = "maintenance"
    other = "other"

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    activity_type = Column(String(50), nullable=False)  # We'll use string for flexibility
    activity_date = Column(Date, nullable=False)
    activity_time = Column(Time)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Equipment and materials
    equipment_used = Column(String(255))
    cost = Column(DECIMAL(10,2))
    labor_hours = Column(DECIMAL(5,2))
    
    # Status
    is_completed = Column(Boolean, default=True)
    weather_conditions = Column(String(100))
    
    # Additional data
    notes = Column(Text)
    photos = Column(JSON)  # Array of photo URLs
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    block = relationship("Block", back_populates="activities")
    user = relationship("User")