from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class DataTypeEnum(enum.Enum):
    quality_metric = "quality_metric"
    processing_parameter = "processing_parameter"
    storage_condition = "storage_condition"
    maturity_indicator = "maturity_indicator"
    defect_assessment = "defect_assessment"
    yield_component = "yield_component"

class CropSpecificData(Base):
    __tablename__ = "crop_specific_data"
    
    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    data_type = Column(String(50), nullable=False)
    measurement_name = Column(String(100), nullable=False)
    measurement_value = Column(DECIMAL(10,4))
    measurement_text = Column(String(200))
    measurement_units = Column(String(50))
    measurement_date = Column(Date, nullable=False)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    block = relationship("Block")
    user = relationship("User")