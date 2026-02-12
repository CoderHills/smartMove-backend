from flask import Blueprint, request
from app.services.booking_service import BookingService
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required
from app.utils.validators import validate_request
from app.models.booking import Booking, BookingStatus

booking_bp = Blueprint('booking', __name__, url_prefix='')

@booking_bp.route('', methods=['GET'])
@jwt_required
def get_bookings(current_user):
    """Get all bookings for the current user with optional filters."""
    try:
        filters = {
            'status': request.args.get('status'),
            'page': request.args.get('page', 1, type=int),
            'limit': request.args.get('limit', 10, type=int)
        }
        result = BookingService.get_user_bookings(current_user, filters)
        return success(result)
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('', methods=['POST'])
@jwt_required
@validate_request('pickup_address', 'dropoff_address', 'booking_time', 'mover_id')
def create_booking(current_user):
    """Create a new booking."""
    data = request.get_json()
    try:
        booking = BookingService.create_booking(current_user, data)
        return success(booking.to_dict(), 201)
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required
def get_booking(current_user, booking_id):
    """Get a specific booking by ID."""
    try:
        booking = BookingService.get_booking_by_id(booking_id, current_user)
        return success(booking.to_dict())
    except Exception as e:
        return error_response(str(e), 404)

@booking_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required
def update_booking(current_user, booking_id):
    """Update a booking."""
    try:
        booking = BookingService.get_booking_by_id(booking_id, current_user)
        data = request.get_json()
        
        # Only allow updating certain fields
        if 'booking_time' in data:
            from datetime import datetime
            if isinstance(data['booking_time'], str):
                booking.booking_time = datetime.fromisoformat(data['booking_time'].replace('Z', '+00:00'))
            else:
                booking.booking_time = data['booking_time']
        
        if 'status' in data:
            try:
                booking.status = BookingStatus(data['status'])
            except ValueError:
                return error_response(f"Invalid status. Valid values: {[s.value for s in BookingStatus]}"), 400
        
        booking.save()
        return success(booking.to_dict())
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required
def cancel_booking(current_user, booking_id):
    """Cancel a booking."""
    try:
        booking = BookingService.get_booking_by_id(booking_id, current_user)
        
        # Only allow cancelling pending bookings
        if booking.status != BookingStatus.PENDING:
            return error_response("Can only cancel pending bookings"), 400
        
        booking.status = BookingStatus.CANCELLED
        booking.save()
        return success({"message": "Booking cancelled successfully"})
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('/quote', methods=['POST'])
@jwt_required
@validate_request('pickup_address', 'dropoff_address', 'mover_id')
def get_quote(current_user):
    """Get a quote for a potential booking."""
    data = request.get_json()
    try:
        from app.services.pricing_service import PricingService
        quote = PricingService.calculate_quote(
            pickup_address=data['pickup_address'],
            dropoff_address=data['dropoff_address'],
            mover_id=data['mover_id']
        )
        return success(quote)
    except NotImplementedError:
        # Fallback simple pricing if service not implemented
        return success({
            'estimated_amount': 150.00,
            'distance_km': 10,
            'duration_hours': 2,
            'message': 'Estimated quote (detailed pricing not configured)'
        })
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('/<int:booking_id>/confirm', methods=['POST'])
@jwt_required
def confirm_booking(current_user, booking_id):
    """Confirm a booking."""
    try:
        booking = BookingService.get_booking_by_id(booking_id, current_user)
        
        if booking.status != BookingStatus.PENDING:
            return error_response("Can only confirm pending bookings"), 400
        
        booking.status = BookingStatus.CONFIRMED
        booking.save()
        return success(booking.to_dict())
    except Exception as e:
        return error_response(str(e))

@booking_bp.route('/<int:booking_id>/track', methods=['GET'])
@jwt_required
def track_booking(current_user, booking_id):
    """Track a booking status."""
    try:
        booking = BookingService.get_booking_by_id(booking_id, current_user)
        
        tracking_info = {
            'booking_id': booking.id,
            'status': booking.status.value if hasattr(booking.status, 'value') else booking.status,
            'payment_status': booking.payment_status,
            'booking_time': booking.booking_time.isoformat() if booking.booking_time else None,
            'created_at': booking.created_at.isoformat() if booking.created_at else None
        }
        
        # Add mover info if available
        if booking.mover:
            tracking_info['mover'] = {
                'company_name': booking.mover.company_name,
                'service_area': booking.mover.service_area
            }
        
        return success(tracking_info)
    except Exception as e:
        return error_response(str(e))

