from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class OrganizationBase(BaseModel):
    org_name: str
    org_type: str
    agricultural_profile: Optional[Dict[Any, Any]] = None
    ui_preferences: Optional[Dict[Any, Any]] = None
    subscription_tier: str = "free"
    timezone: str = "America/Los_Angeles"

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    org_name: Optional[str] = None
    org_type: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True