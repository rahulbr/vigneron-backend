# app/api/api_v1/endpoints/mobile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import math

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

def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two GPS points in meters"""
    return geodesic((lat1, lng1), (lat2, lng2)).meters

def is_point_in_circle(point_lat: float, point_lng: float, 
                      center_lat: float, center_lng: float, radius_meters: float) -> bool:
    """Check if a point is within a circular boundary"""
    distance = calculate_distance(point_lat, point_lng, center_lat, center_lng)
    return distance <= radius_meters

@router.post("/detect-location")
async def detect_location(
    gps_data: GPSLocationRequest,
    db: Session = Depends(deps.get_db)
):
    """Auto-detect property, block, row based on GPS coordinates"""
    user_lat = gps_data.latitude
    user_lng = gps_data.longitude
    
    # Find closest property
    properties = db.query(Property).all()
    detected_property = None
    min_distance = float('inf')
    
    for prop in properties:
        if prop.latitude and prop.longitude:
            # Check if user is within property boundary (if defined)
            if (prop.boundary_center_lat and prop.boundary_center_lng and 
                prop.boundary_radius_meters):
                if is_point_in_circle(user_lat, user_lng, 
                                    float(prop.boundary_center_lat), 
                                    float(prop.boundary_center_lng),
                                    float(prop.boundary_radius_meters)):
                    detected_property = prop
                    min_distance = calculate_distance(user_lat, user_lng, 
                                                    float(prop.latitude), float(prop.longitude))
                    break
            else:
                # Fallback to closest property by center point
                distance = calculate_distance(user_lat, user_lng, 
                                            float(prop.latitude), float(prop.longitude))
                if distance < min_distance and distance < 1000:  # Within 1km
                    min_distance = distance
                    detected_property = prop
    
    if not detected_property:
        raise HTTPException(status_code=404, detail="No property found within range")
    
    # Find closest block within property
    blocks = db.query(Block).filter(Block.property_id == detected_property.id).all()
    detected_block = None
    min_block_distance = float('inf')
    
    for block in blocks:
        if block.center_latitude and block.center_longitude:
            # Check if user is within block boundary (if defined)
            if block.boundary_radius_meters:
                if is_point_in_circle(user_lat, user_lng,
                                    float(block.center_latitude),
                                    float(block.center_longitude),
                                    float(block.boundary_radius_meters)):
                    detected_block = block
                    min_block_distance = calculate_distance(user_lat, user_lng,
                                                           float(block.center_latitude),
                                                           float(block.center_longitude))
                    break
            else:
                # Fallback to closest block
                distance = calculate_distance(user_lat, user_lng,
                                            float(block.center_latitude),
                                            float(block.center_longitude))
                if distance < min_block_distance and distance < 500:  # Within 500m
                    min_block_distance = distance
                    detected_block = block
    
    # Calculate confidence scores
    property_confidence = max(0, 1 - (min_distance / 1000))
    block_confidence = max(0, 1 - (min_block_distance / 500)) if detected_block else 0
    
    return {
        "detected_property": {
            "id": detected_property.id,
            "name": detected_property.property_name,
            "confidence": round(property_confidence, 2),
            "distance_meters": round(min_distance, 1)
        },
        "detected_block": {
            "id": detected_block.id if detected_block else None,
            "name": detected_block.block_name if detected_block else None,
            "confidence": round(block_confidence, 2),
            "distance_meters": round(min_block_distance, 1) if detected_block else None
        } if detected_block else None,
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
        "checkin_id": f"checkin_{checkin_data.timestamp.isoformat()}",
        "location_detection": location_detection,
        "timestamp": checkin_data.timestamp,
        "device_id": checkin_data.device_id
    }

@router.get("/nearby-locations")
async def get_nearby_locations(
    latitude: float,
    longitude: float,
    radius_meters: float = 1000,
    db: Session = Depends(deps.get_db)
):
    """Get all properties and blocks within radius of user location"""
    nearby_properties = []
    nearby_blocks = []
    
    # Find nearby properties
    properties = db.query(Property).all()
    for prop in properties:
        if prop.latitude and prop.longitude:
            distance = calculate_distance(latitude, longitude, 
                                        float(prop.latitude), float(prop.longitude))
            if distance <= radius_meters:
                nearby_properties.append({
                    "id": prop.id,
                    "name": prop.property_name,
                    "distance_meters": round(distance, 1),
                    "latitude": float(prop.latitude),
                    "longitude": float(prop.longitude)
                })
    
    # Find nearby blocks
    blocks = db.query(Block).all()
    for block in blocks:
        if block.center_latitude and block.center_longitude:
            distance = calculate_distance(latitude, longitude,
                                        float(block.center_latitude),
                                        float(block.center_longitude))
            if distance <= radius_meters:
                nearby_blocks.append({
                    "id": block.id,
                    "name": block.block_name,
                    "property_id": block.property_id,
                    "distance_meters": round(distance, 1),
                    "latitude": float(block.center_latitude),
                    "longitude": float(block.center_longitude)
                })
    
    return {
        "user_location": {"latitude": latitude, "longitude": longitude},
        "search_radius_meters": radius_meters,
        "nearby_properties": sorted(nearby_properties, key=lambda x: x["distance_meters"]),
        "nearby_blocks": sorted(nearby_blocks, key=lambda x: x["distance_meters"])
    }