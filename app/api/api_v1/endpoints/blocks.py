from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.block import Block
from app.models.property import Property

router = APIRouter()

@router.get("/{property_id}/blocks")
def get_blocks(
    property_id: int,
    db: Session = Depends(deps.get_db)
):
    """Get all blocks for a property"""
    blocks = db.query(Block).filter(Block.property_id == property_id).all()
    return blocks

@router.post("/{property_id}/blocks") 
def create_block(
    property_id: int,
    block_data: dict,
    db: Session = Depends(deps.get_db)
):
    """Create new block"""
    # Verify property exists
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    
    db_block = Block(property_id=property_id, **block_data)
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block

@router.get("/{property_id}/blocks/{block_id}/context")
def get_block_context(
    property_id: int,
    block_id: int,
    db: Session = Depends(deps.get_db)
):
    """Get block-specific context and available operations"""
    block = db.query(Block).filter(
        Block.id == block_id,
        Block.property_id == property_id
    ).first()
    
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    
    crop_type = block.crop_type
    
    return {
        "block_id": block_id,
        "block_name": block.block_name,
        "crop_type": crop_type,
        "variety": block.variety,
        "available_operations": _get_crop_operations(crop_type),
        "quality_metrics": _get_quality_metrics(crop_type),
        "activity_templates": _get_activity_templates(crop_type)
    }

def _get_crop_operations(crop_type: str) -> List[str]:
    """Get operations available for this crop type"""
    universal_ops = ["irrigation", "observation", "maintenance"]
    
    crop_specific = {
        "coffee": ["cherry_picking", "moisture_testing", "cupping"],
        "apple": ["maturity_testing", "harvest", "ca_storage_prep"],
        "grape": ["harvest", "crush", "fermentation_monitoring"]
    }
    
    return universal_ops + crop_specific.get(crop_type, [])

def _get_quality_metrics(crop_type: str) -> List[dict]:
    """Get quality metrics for this crop"""
    metrics = {
        "coffee": [
            {"name": "cherry_moisture", "unit": "%", "target_range": "18-22"},
            {"name": "cup_score", "unit": "points", "target_range": "80-100"}
        ],
        "apple": [
            {"name": "firmness", "unit": "lbs", "target_range": "16-18"},
            {"name": "starch_index", "unit": "scale", "target_range": "1-8"}
        ],
        "grape": [
            {"name": "brix", "unit": "°Bx", "target_range": "20-26"},
            {"name": "ph", "unit": "pH", "target_range": "3.0-3.6"}
        ]
    }
    
    return metrics.get(crop_type, [])

def _get_activity_templates(crop_type: str) -> List[dict]:
    """Get common activity templates for this crop"""
    templates = {
        "coffee": [
            {"name": "Cherry Moisture Check", "frequency": "daily"},
            {"name": "Cupping Session", "frequency": "weekly"}
        ],
        "apple": [
            {"name": "Maturity Test", "frequency": "weekly"},
            {"name": "Harvest Planning", "frequency": "seasonal"}
        ],
        "grape": [
            {"name": "Brix Testing", "frequency": "weekly"},
            {"name": "Harvest Assessment", "frequency": "daily_during_harvest"}
        ]
    }
    
    return templates.get(crop_type, [])