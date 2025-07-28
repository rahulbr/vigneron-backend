from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # 'expense', 'income'
    description = Column(String(200), nullable=False)
    amount = Column(DECIMAL(12,2), nullable=False)
    
    # Cost allocation
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=True)
    spray_application_id = Column(Integer, nullable=True)  # Will add FK later
    
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    organization = relationship("Organization")
    block = relationship("Block")
    created_by = relationship("User")