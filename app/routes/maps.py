from flask import Blueprint, request
from app.utils.response import success, error_response
from app.services.google_maps_service import GoogleMapsService
from app.utils.validators import validate_request

maps_bp = Blueprint('maps', __name__, url_prefix='/maps')

@maps_bp.route('/calculate-distance', methods=['POST'])
@validate_request('origin', 'destination')
def calculate_distance():
    """
    Calculates the distance between two points using Google Maps API.
    """
    data = request.get_json()
    origin = data['origin']
    destination = data['destination']
    
    try:
        distance_info = GoogleMapsService.get_distance_matrix(origin, destination)
        return success(distance_info)
    except Exception as e:
        return error_response(str(e), 500)
