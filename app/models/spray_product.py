from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class SprayProduct(Base):
    __tablename__ = "spray_products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    epa_registration_number = Column(String(50))
    active_ingredients = Column(JSON, nullable=False)
    product_type = Column(String(50), nullable=False)  # 'fungicide', 'insecticide', etc.
    
    # Mode of action
    frac_code = Column(String(10))
    irac_code = Column(String(10))
    hrac_code = Column(String(10))
    resistance_risk = Column(String(10))
    
    # Regulatory
    restricted_use_pesticide = Column(Boolean, default=False)
    organic_approved = Column(Boolean, default=False)
    signal_word = Column(String(10))
    
    # Rates and safety
    min_rate_per_acre = Column(DECIMAL(10,3))
    max_rate_per_acre = Column(DECIMAL(10,3))
    rate_units = Column(String(20))
    default_rei_hours = Column(Integer)
    default_phi_days = Column(Integer)
    
    # Cost
    cost_per_unit = Column(DECIMAL(10,3))
    unit_size = Column(DECIMAL(8,2))
    unit_type = Column(String(20))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    restrictions = relationship("CropSpecificRestriction", back_populates="spray_product")
    applications = relationship("SprayApplication", back_populates="spray_product")