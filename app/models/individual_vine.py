from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.db.base import Base

class IndividualVine(Base):
    __tablename__ = "individual_vines"
    
    id = Column(Integer, primary_key=True, index=True)
    row_id = Column(Integer, ForeignKey("rows.id"), nullable=False)
    vine_number = Column(Integer, nullable=False)
    variety = Column(String(50))
    clone = Column(String(50))
    rootstock = Column(String(50))
    planting_date = Column(Date)
    
    # Vine details
    graft_union_height = Column(DECIMAL(4,2))
    vine_status = Column(String(20), default='healthy')
    trunk_diameter_mm = Column(DECIMAL(6,2))
    
    # Trellis/training (if different from row)
    trellis_system = Column(String(100))
    training_method = Column(String(100))
    pruning_method = Column(String(100))
    spur_count = Column(Integer)
    cane_count = Column(Integer)
    
    # Performance
    canopy_vigor = Column(String(20))
    fruit_quality_rating = Column(String(20))
    historical_yield_kg = Column(DECIMAL(6,2))
    
    # GPS
    gps_coordinates = Column(Geometry('POINT'))
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    row = relationship("Row", back_populates="vines")