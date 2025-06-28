"""
AI Model endpoints.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.ai_model import AIModel
from app.schemas.ai_model import (
    AIModelCreate,
    AIModelListResponse,
    AIModelResponse,
    AIModelUpdate,
)
from app.schemas.common import APIResponse, SuccessResponse

router = APIRouter()


@router.get("/", response_model=AIModelListResponse)
async def list_models(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """List all AI models with pagination."""
    offset = (page - 1) * per_page
    
    models = db.query(AIModel).offset(offset).limit(per_page).all()
    total = db.query(AIModel).count()
    
    return AIModelListResponse(
        models=[AIModelResponse.model_validate(model) for model in models],
        total=total,
        page=page,
        per_page=per_page,
        has_next=offset + per_page < total,
    )


@router.post("/", response_model=APIResponse[AIModelResponse])
async def create_model(
    model_data: AIModelCreate,
    db: Session = Depends(get_db),
):
    """Create a new AI model."""
    # Check if model with same name and version exists
    existing = (
        db.query(AIModel)
        .filter(
            AIModel.name == model_data.name,
            AIModel.version == model_data.version,
        )
        .first()
    )
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_data.name}' version '{model_data.version}' already exists",
        )
    
    # Create new model
    new_model = AIModel(**model_data.model_dump())
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    
    return APIResponse(
        success=True,
        message="AI model created successfully",
        data=AIModelResponse.model_validate(new_model),
    )


@router.get("/{model_id}", response_model=APIResponse[AIModelResponse])
async def get_model(
    model_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific AI model by ID."""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return APIResponse(
        success=True,
        message="Model retrieved successfully",
        data=AIModelResponse.model_validate(model),
    )


@router.put("/{model_id}", response_model=APIResponse[AIModelResponse])
async def update_model(
    model_id: UUID,
    model_update: AIModelUpdate,
    db: Session = Depends(get_db),
):
    """Update an AI model."""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Update fields that were provided
    update_data = model_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(model, field, value)
    
    db.commit()
    db.refresh(model)
    
    return APIResponse(
        success=True,
        message="Model updated successfully",
        data=AIModelResponse.model_validate(model),
    )


@router.delete("/{model_id}", response_model=SuccessResponse)
async def delete_model(
    model_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete an AI model."""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    db.delete(model)
    db.commit()
    
    return SuccessResponse(message="Model deleted successfully")