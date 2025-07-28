# app/services/google_maps_service.py
from typing import Dict, List, Optional, Tuple
import math

class GoogleMapsService:
    """Helper service for Google Maps integration"""
    
    @staticmethod
    def create_map_url(latitude: float, longitude: float, zoom: int = 15) -> str:
        """Create a Google Maps URL for a location"""
        return f"https://www.google.com/maps/@{latitude},{longitude},{zoom}z"
    
    @staticmethod
    def create_directions_url(start_lat: float, start_lng: float, 
                            end_lat: float, end_lng: float) -> str:
        """Create a Google Maps directions URL"""
        return f"https://www.google.com/maps/dir/{start_lat},{start_lng}/{end_lat},{end_lng}"
    
    @staticmethod
    def bounds_for_locations(locations: List[Tuple[float, float]]) -> Dict:
        """Calculate map bounds for a list of lat/lng coordinates"""
        if not locations:
            return {}
        
        lats = [loc[0] for loc in locations]
        lngs = [loc[1] for loc in locations]
        
        return {
            "northeast": {"lat": max(lats), "lng": max(lngs)},
            "southwest": {"lat": min(lats), "lng": min(lngs)},
            "center": {
                "lat": sum(lats) / len(lats),
                "lng": sum(lngs) / len(lngs)
            }
        }
    
    @staticmethod
    def calculate_zoom_level(bounds: Dict, map_width_px: int = 800, 
                           map_height_px: int = 600) -> int:
        """Calculate appropriate zoom level for given bounds"""
        if not bounds:
            return 15
        
        # Simple zoom calculation based on lat/lng span
        lat_span = abs(bounds["northeast"]["lat"] - bounds["southwest"]["lat"])
        lng_span = abs(bounds["northeast"]["lng"] - bounds["southwest"]["lng"])
        
        # Rough zoom calculation (you can refine this)
        max_span = max(lat_span, lng_span)
        
        if max_span > 10:
            return 5
        elif max_span > 5:
            return 7
        elif max_span > 1:
            return 10
        elif max_span > 0.5:
            return 12
        elif max_span > 0.1:
            return 14
        elif max_span > 0.05:
            return 16
        else:
            return 18
    
    @staticmethod
    def format_for_google_maps_js(properties: list, blocks: list) -> Dict:
        """Format property and block data for Google Maps JavaScript API"""
        markers = []
        
        # Add property markers
        for prop in properties:
            if prop.latitude and prop.longitude:
                markers.append({
                    "id": f"property_{prop.id}",
                    "type": "property",
                    "position": {
                        "lat": float(prop.latitude),
                        "lng": float(prop.longitude)
                    },
                    "title": prop.property_name,
                    "info": {
                        "name": prop.property_name,
                        "type": prop.property_type,
                        "acres": float(prop.total_acres) if prop.total_acres else None,
                        "crops": prop.primary_crops
                    },
                    "icon": {
                        "url": "/static/icons/property-marker.png",  # You'll need to add this
                        "scaledSize": {"width": 32, "height": 32}
                    }
                })
        
        # Add block markers
        for block in blocks:
            if block.center_latitude and block.center_longitude:
                markers.append({
                    "id": f"block_{block.id}",
                    "type": "block", 
                    "position": {
                        "lat": float(block.center_latitude),
                        "lng": float(block.center_longitude)
                    },
                    "title": f"{block.block_name} ({block.variety or block.crop_type})",
                    "info": {
                        "name": block.block_name,
                        "variety": block.variety,
                        "crop_type": block.crop_type,
                        "acres": float(block.acres) if block.acres else None,
                        "planting_year": block.planting_year
                    },
                    "icon": {
                        "url": "/static/icons/block-marker.png",  # You'll need to add this
                        "scaledSize": {"width": 24, "height": 24}
                    }
                })
                
                # Add circular boundary if defined
                if block.boundary_radius_meters:
                    markers.append({
                        "id": f"block_boundary_{block.id}",
                        "type": "boundary",
                        "circle": {
                            "center": {
                                "lat": float(block.center_latitude),
                                "lng": float(block.center_longitude)
                            },
                            "radius": float(block.boundary_radius_meters),
                            "fillColor": "#4CAF50",
                            "fillOpacity": 0.1,
                            "strokeColor": "#4CAF50",
                            "strokeOpacity": 0.8,
                            "strokeWeight": 2
                        }
                    })
        
        # Calculate bounds for all markers
        positions = [marker["position"] for marker in markers if "position" in marker]
        bounds = GoogleMapsService.bounds_for_locations(
            [(pos["lat"], pos["lng"]) for pos in positions]
        )
        
        return {
            "markers": markers,
            "bounds": bounds,
            "center": bounds.get("center", {"lat": 37.4419, "lng": -122.1430}),
            "zoom": GoogleMapsService.calculate_zoom_level(bounds)
        }