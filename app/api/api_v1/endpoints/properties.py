from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.property import Property
from app.models.organization import Organization

router = APIRouter()

@router.get("/{org_id}/properties")
def get_properties(
    org_id: int,
    db: Session = Depends(deps.get_db)
):
    """Get all properties for an organization"""
    properties = db.query(Property).filter(Property.org_id == org_id).all()
    return properties

@router.post("/{org_id}/properties")
def create_property(
    org_id: int,
    property_data: dict,  # We'll create proper schema later
    db: Session = Depends(deps.get_db)
):
    """Create new property"""
    # Verify organization exists
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    db_property = Property(org_id=org_id, **property_data)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router.get("/{org_id}/properties/{property_id}/context")
def get_property_context(
    org_id: int,
    property_id: int,
    db: Session = Depends(deps.get_db)
):
    """Get property-specific context for UX"""
    property_obj = db.query(Property).filter(
        Property.id == property_id,
        Property.org_id == org_id
    ).first()
    
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    primary_crops = property_obj.primary_crops or []
    business_functions = property_obj.business_functions or []
    
    return {
        "property_id": property_id,
        "property_name": property_obj.property_name,
        "primary_crops": primary_crops,
        "business_functions": business_functions,
        "available_modules": _get_property_modules(primary_crops, business_functions),
        "dashboard_widgets": _get_property_widgets(primary_crops)
    }

def _get_property_modules(crops: List[str], functions: List[str]) -> List[str]:
    """Get modules specific to this property"""
    modules = ["blocks", "activities", "weather"]
    
    if "coffee" in crops:
        modules.extend(["cherry_processing", "moisture_tracking"])
    if "apple" in crops:
        modules.extend(["maturity_testing", "ca_storage"])
    if "agritourism" in functions:
        modules.extend(["visitor_management", "events"])
        
    return modules

def _get_property_widgets(crops: List[str]) -> List[dict]:
    """Get widgets specific to this property"""
    widgets = [{"type": "weather_station", "priority": 1}]
    
    if "coffee" in crops:
        widgets.append({"type": "cherry_moisture_alerts", "priority": 2})
    if "apple" in crops:
        widgets.append({"type": "harvest_readiness", "priority": 2})
        
    return widgets