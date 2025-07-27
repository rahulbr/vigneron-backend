from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationResponse

router = APIRouter()

@router.get("/", response_model=List[OrganizationResponse])
def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
):
    """Get all organizations"""
    organizations = db.query(Organization).offset(skip).limit(limit).all()
    return organizations

@router.post("/", response_model=OrganizationResponse)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(deps.get_db)
):
    """Create new organization"""
    db_org = Organization(**organization.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@router.get("/{org_id}/context")
def get_organization_context(
    org_id: int,
    db: Session = Depends(deps.get_db)
):
    """Get organization context for UX customization"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Return context-driven UX data
    agricultural_profile = org.agricultural_profile or {}
    
    return {
        "org_id": org_id,
        "org_name": org.org_name,
        "org_type": org.org_type,
        "agricultural_profile": agricultural_profile,
        "available_modules": _get_available_modules(agricultural_profile),
        "dashboard_widgets": _get_dashboard_widgets(agricultural_profile)
    }

def _get_available_modules(profile: dict) -> List[str]:
    """Determine available modules based on agricultural profile"""
    modules = ["properties", "activities", "weather", "people"]
    
    crops = profile.get("crops", [])
    if "coffee" in crops:
        modules.extend(["cherry_processing", "cupping_lab", "certifications"])
    if "apple" in crops:
        modules.extend(["ca_storage", "maturity_testing", "packing_house"])
    if "grape" in crops:
        modules.extend(["cellar_operations", "barrel_management"])
        
    return modules

def _get_dashboard_widgets(profile: dict) -> List[dict]:
    """Get contextual dashboard widgets"""
    widgets = [
        {"type": "weather", "priority": 1},
        {"type": "recent_activities", "priority": 2}
    ]
    
    crops = profile.get("crops", [])
    if "coffee" in crops:
        widgets.append({"type": "cherry_moisture", "priority": 3})
    if "apple" in crops:
        widgets.append({"type": "maturity_tracking", "priority": 3})
        
    return widgets