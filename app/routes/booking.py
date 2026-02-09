from flask import Blueprint, request
from app.services.booking_service import BookingService
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required
from app.utils.validators import validate_request

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.route('', methods=['POST'])
@jwt_required
@validate_request('pickup_address', 'dropoff_address', 'booking_time')
def create_booking(current_user):
    data = request.get_json()
    try:
        booking = BookingService.create_booking(current_user, data)
        return success(booking.to_dict(), 201)
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required
def get_booking(current_user, booking_id):
    try:
        booking = BookingService.get_booking_by_id(booking_id, current_user)
        return success(booking.to_dict())
    except Exception as e:
        return error_response(str(e), 404)
