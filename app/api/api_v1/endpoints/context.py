# app/api/api_v1/endpoints/context.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from app.api import deps
from app.services.context_service import ContextService

router = APIRouter()

@router.get("/user-context/{org_id}")
def get_user_context(
    org_id: int,
    db: Session = Depends(deps.get_db)
) -> Dict:
    """Get user's contextual configuration for UX customization"""
    context = ContextService.get_user_context(org_id)
    return {
        "context": context,
        "available_modules": ContextService.get_available_modules(
            context.get("crops", []), 
            context.get("business_model", [])
        ),
        "dashboard_widgets": ContextService.get_dashboard_widgets(context)
    }

@router.post("/configure-organization/{org_id}")
def configure_organization(
    org_id: int,
    config: Dict,  # This would be a proper Pydantic model
    db: Session = Depends(deps.get_db)
) -> Dict:
    """Update organization's agricultural profile and UI preferences"""
    # Update organization with new configuration
    # This drives the entire UX experience
    return {"status": "updated", "config": config}