# app/services/context_service.py
from typing import Dict, List, Optional
from app.models.organization import Organization
from app.models.property import Property

class ContextService:
    """Service for managing context-driven UX logic"""
    
    @staticmethod
    def get_user_context(org_id: int) -> Dict:
        """Get complete user context for UX customization"""
        # This would query the database for organization and properties
        return {
            "crops": ["coffee", "macadamia"],
            "business_model": ["processing", "direct_sales"],
            "modules": ["processing", "cupping_lab", "certifications"],
            "terminology": "coffee"  # vs "wine" or "apple"
        }
    
    @staticmethod
    def get_available_modules(crops: List[str], business_functions: List[str]) -> List[str]:
        """Determine which modules should be available to user"""
        modules = ["properties", "activities", "weather", "people"]  # Always available
        
        # Crop-specific modules
        if "coffee" in crops:
            modules.extend(["cherry_processing", "cupping_lab", "certifications"])
        if "apple" in crops:
            modules.extend(["ca_storage", "maturity_testing", "packing_house"])
        if "grape" in crops:
            modules.extend(["cellar_operations", "barrel_management", "ttb_compliance"])
            
        # Business function modules
        if "processing" in business_functions:
            modules.extend(["production_batches", "quality_control"])
        if "direct_sales" in business_functions:
            modules.extend(["customers", "orders", "pos"])
        if "agritourism" in business_functions:
            modules.extend(["events", "bookings", "visitor_management"])
            
        return list(set(modules))  # Remove duplicates
    
    @staticmethod
    def get_dashboard_widgets(context: Dict) -> List[Dict]:
        """Get contextual dashboard widgets"""
        widgets = [
            {"type": "weather", "priority": 1},
            {"type": "tasks", "priority": 2}
        ]
        
        if "coffee" in context.get("crops", []):
            widgets.extend([
                {"type": "cherry_moisture", "priority": 3},
                {"type": "processing_throughput", "priority": 4},
                {"type": "cup_scores", "priority": 5}
            ])
            
        if "apple" in context.get("crops", []):
            widgets.extend([
                {"type": "maturity_tracking", "priority": 3},
                {"type": "ca_room_status", "priority": 4},
                {"type": "harvest_schedule", "priority": 5}
            ])
            
        return sorted(widgets, key=lambda x: x["priority"])