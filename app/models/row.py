from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from app.db.base import Base

class Row(Base):
    __tablename__ = "rows"
    
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    variety = Column(String(50))
    clone = Column(String(50))
    rootstock = Column(String(50))
    planting_date = Column(DateTime(timezone=True))
    vine_count = Column(Integer)
    row_length_ft = Column(DECIMAL(8,2))
    vine_spacing_ft = Column(DECIMAL(5,2))
    
    # Trellis details
    trellis_system = Column(String(100))
    training_method = Column(String(100))
    wire_count = Column(Integer)
    post_spacing_ft = Column(DECIMAL(5,2))
    
    # GPS
    gps_start_point = Column(Geometry('POINT'))
    gps_end_point = Column(Geometry('POINT'))
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    block = relationship("Block", back_populates="rows")
    vines = relationship("IndividualVine", back_populates="row")