"""
Navigation and transportation tools for the API Conference AI Agent.
Handles maps, directions, bus routes, and venue access information.
"""

import asyncio
from typing import Dict, Any, Optional, List
import googlemaps
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from google.adk.tools import FunctionTool
from googlemaps.exceptions import ApiError

from app.config.settings import settings
from app.config.logger import Logger

logger = Logger.get_logger(__name__)

# Initialize Google Maps client
gmaps = googlemaps.Client(key=settings.google_maps_api_key)
geolocator = Nominatim(user_agent=settings.user_agent)

def get_directions_to_venue(origin: str, mode: str = "transit", **kwargs) -> Optional[Dict[str, Any]]:
    """
    Get directions from user's location to the conference venue.
    
    Args:
        origin: User's starting location (address or coordinates)
        mode: Transportation mode (transit, driving, walking, bicycling)
        
    Returns:
        Dictionary with route information, estimated time, and instructions
    """
    try:
        venue_coords = settings.conference_venue_coordinates.split(",")
        venue_lat, venue_lng = float(venue_coords[0]), float(venue_coords[1])
        
        # Get directions
        directions = gmaps.directions(
            origin,
            (venue_lat, venue_lng),
            mode=mode,
            transit_mode=["bus", "train"] if mode == "transit" else None,
            alternatives=True
        )
        
        if not directions:
            return {
                "error": True,
                "message": f"Could not find route from {origin} to the venue",
                "suggestion": "Try providing a more specific address or contact support",
                "support_contact": settings.support_phone
            }
        
        # Process the best route
        route = directions[0]
        legs = route['legs'][0]
        
        # Extract step-by-step instructions
        steps = []
        for step in legs['steps']:
            steps.append({
                "instruction": step['html_instructions'],
                "distance": step['distance']['text'],
                "duration": step['duration']['text']
            })
        
        # Get fare information if available
        fare_info = "Contact transport provider"
        if 'fare' in route:
            fare_info = route['fare'].get('text', fare_info)
        
        return {
            "success": True,
            "origin": origin,
            "destination": settings.conference_venue_name,
            "total_distance": legs['distance']['text'],
            "total_duration": legs['duration']['text'],
            "transportation_mode": mode,
            "steps": steps,
            "fare_estimate": fare_info,
            "alternative_routes": len(directions) > 1,
            "venue_address": settings.conference_venue_address,
            "support_contact": settings.support_phone
        }
        
    except ApiError as e:
        logger.error(f"Error getting directions (ApiError): {e}")
        if "REQUEST_DENIED" in str(e):
            return {
                "error": True,
                "message": "I am unable to provide directions at this time due to a server configuration issue. The Google Maps API key may be invalid or require a billing account to be enabled. Please contact support.",
                "support_contact": settings.support_phone
            }
        return {
            "error": True,
            "message": f"Unable to get directions at this time due to a Google Maps API error: {e}",
            "support_contact": settings.support_phone
        }
    except Exception as e:
        logger.error(f"Error getting directions: {e}")
        return {
            "error": True,
            "message": "Unable to get directions at this time",
            "fallback": f"Please contact {settings.support_phone} for assistance",
            "support_contact": settings.support_phone
        }

def find_nearby_transportation(location: str, radius: int = 1000, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Find nearby bus stops, train stations, and other transportation options.
    
    Args:
        location: User's location (address or coordinates)
        radius: Search radius in meters
        
    Returns:
        Dictionary with nearby transportation options
    """
    try:
        # Geocode the location if it's an address
        if not location.replace('.', '').replace(',', '').replace(' ', '').isdigit():
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                location = f"{geocode_result[0]['geometry']['location']['lat']},{geocode_result[0]['geometry']['location']['lng']}"
        
        # Search for transit stations
        transit_stations = gmaps.places_nearby(
            location=location,
            radius=radius,
            type='transit_station'
        )
        
        # Search for bus stops
        bus_stops = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword='bus stop'
        )
        
        # Combine and format results
        transport_options = []
        
        for place in transit_stations.get('results', []):
            transport_options.append({
                "name": place['name'],
                "type": "transit_station",
                "address": place.get('vicinity', 'Address not available'),
                "rating": place.get('rating', 'No rating'),
                "distance": place.get('distance', 'Unknown')
            })
        
        for place in bus_stops.get('results', []):
            transport_options.append({
                "name": place['name'],
                "type": "bus_stop",
                "address": place.get('vicinity', 'Address not available'),
                "rating": place.get('rating', 'No rating'),
                "distance": place.get('distance', 'Unknown')
            })
        
        return {
            "success": True,
            "location": location,
            "transport_options": transport_options[:10],  # Limit to top 10
            "total_found": len(transport_options),
            "search_radius_km": radius / 1000,
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error finding transportation: {e}")
        return {
            "error": True,
            "message": "Unable to find transportation options",
            "fallback": f"Please contact {settings.support_phone} for assistance",
            "support_contact": settings.support_phone
        }

def get_venue_access_info(**kwargs) -> Dict[str, Any]:
    """
    Get information about accessing the conference venue.
    
    Returns:
        Dictionary with venue access information
    """
    return {
        "venue_name": settings.conference_venue_name,
        "address": settings.conference_venue_address,
        "coordinates": settings.conference_venue_coordinates,
        "access_notes": [
            "Main entrance on Gbagada - Oworonshoki Expressway",
            "Security checkpoint at entrance",
            "Conference registration desk in lobby",
            "Elevator access to conference rooms",
            "Wheelchair accessible"
        ],
        "parking_info": [
            "Free parking available on-site",
            "Street parking available nearby",
            "Secure parking area within the industrial scheme"
        ],
        "transportation_tips": [
            "Buses run frequently on Gbagada - Oworonshoki Expressway",
            "Uber and Bolt are available in the area",
            "Walking distance from Gbagada bus terminal",
            "Consider traffic during peak hours (7-9 AM and 5-7 PM)",
            "The venue is easily accessible from Ikeja, Victoria Island, and mainland Lagos"
        ],
        "contact": {
            "phone": settings.support_phone,
            "email": settings.support_email
        }
    }

def get_real_time_transport_info(location: str, **kwargs) -> Optional[Dict[str, Any]]:
    """
    Get real-time transportation information for a location.
    
    Args:
        location: User's location (address or coordinates)
        
    Returns:
        Dictionary with real-time transport information
    """
    try:
        # This would integrate with local transport APIs
        # For now, return general information
        return {
            "success": True,
            "location": location,
            "transport_info": {
                "buses": "Buses run every 15-30 minutes",
                "traffic": "Check Google Maps for real-time traffic",
                "peak_hours": "7-9 AM and 5-7 PM",
                "tips": [
                    "Plan extra time during peak hours",
                    "Consider ride-sharing apps",
                    "Check weather conditions"
                ]
            },
            "support_contact": settings.support_phone
        }
        
    except Exception as e:
        logger.error(f"Error getting transport info: {e}")
        return {
            "error": True,
            "message": "Unable to get transport information",
            "support_contact": settings.support_phone
        }

def get_navigation_tools() -> List[FunctionTool]:
    """Get all navigation-related tools."""
    
    return [
        FunctionTool(get_directions_to_venue),
        FunctionTool(find_nearby_transportation),
        FunctionTool(get_venue_access_info),
        FunctionTool(get_real_time_transport_info)
    ] 