from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from app.api import deps
from app.models.property import Property
from app.models.block import Block
from app.models.row import Row

router = APIRouter()

class GPSLocationRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy_meters: float
    altitude_ft: Optional[float] = None

class MobileCheckinRequest(BaseModel):
    gps_location: GPSLocationRequest
    timestamp: datetime
    device_id: str
    app_version: str

@router.post("/detect-location")
async def detect_location(
    gps_data: GPSLocationRequest,
    db: Session = Depends(deps.get_db)
):
    """Auto-detect property, block, row based on GPS coordinates"""
    user_point = (gps_data.latitude, gps_data.longitude)
    
    # Find closest property
    properties = db.query(Property).all()
    closest_property = None
    min_distance = float('inf')
    
    for prop in properties:
        if prop.latitude and prop.longitude:
            prop_point = (float(prop.latitude), float(prop.longitude))
            distance = geodesic(user_point, prop_point).meters
            if distance < min_distance:
                min_distance = distance
                closest_property = prop
    
    if not closest_property or min_distance > 1000:  # 1km radius
        raise HTTPException(status_code=404, detail="No property found within range")
    
    # Find closest block
    blocks = db.query(Block).filter(Block.property_id == closest_property.id).all()
    closest_block = None
    min_block_distance = float('inf')
    
    # For now, use property center; later implement proper polygon checking
    for block in blocks:
        if closest_property.latitude and closest_property.longitude:
            block_point = (float(closest_property.latitude), float(closest_property.longitude))
            distance = geodesic(user_point, block_point).meters
            if distance < min_block_distance:
                min_block_distance = distance
                closest_block = block
    
    # Calculate confidence scores
    property_confidence = max(0, 1 - (min_distance / 1000))
    block_confidence = max(0, 1 - (min_block_distance / 500)) if closest_block else 0
    
    return {
        "detected_property": {
            "id": closest_property.id,
            "name": closest_property.property_name,
            "confidence": round(property_confidence, 2)
        },
        "detected_block": {
            "id": closest_block.id if closest_block else None,
            "name": closest_block.block_name if closest_block else None,
            "confidence": round(block_confidence, 2)
        } if closest_block else None,
        "gps_accuracy": gps_data.accuracy_meters
    }

@router.post("/checkin")
async def mobile_checkin(
    checkin_data: MobileCheckinRequest,
    db: Session = Depends(deps.get_db)
):
    """Record mobile check-in with auto-detected location"""
    location_detection = await detect_location(checkin_data.gps_location, db)
    
    # For now, just return the detection - you can add ActivityLocation model later
    return {
        "checkin_id": f"temp_{checkin_data.timestamp.isoformat()}",
        "location_detection": location_detection,
        "timestamp": checkin_data.timestamp
    }