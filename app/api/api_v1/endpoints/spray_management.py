from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.api import deps
from app.models.spray_product import SprayProduct

router = APIRouter()

class SprayProductResponse(BaseModel):
    id: int
    name: str
    manufacturer: str
    active_ingredients: dict
    frac_code: Optional[str]
    restrictions: dict
    cost_per_unit: Optional[float]

    class Config:
        from_attributes = True

@router.get("/products/search")
async def search_spray_products(
    q: str,
    crop_type: Optional[str] = None,
    db: Session = Depends(deps.get_db)
):
    """Search spray products with regulatory information"""
    query = db.query(SprayProduct).filter(SprayProduct.is_active == True)
    
    if q:
        query = query.filter(SprayProduct.product_name.ilike(f"%{q}%"))
    
    products = query.limit(20).all()
    
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.product_name,
            "manufacturer": product.manufacturer,
            "active_ingredients": product.active_ingredients,
            "frac_code": product.frac_code,
            "restrictions": {
                "phi_days": product.default_phi_days,
                "rei_hours": product.default_rei_hours,
            },
            "cost_per_unit": product.cost_per_unit
        })
    
    return result

# Add compliance checking endpoint here...