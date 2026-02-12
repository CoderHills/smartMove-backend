from datetime import datetime
from app.extensions import db
from app.models.booking import Booking, BookingStatus
from app.models.address import Address
from app.models.mover import Mover

class BookingService:
    @staticmethod
    def create_booking(current_user, data):
        """
        Create a new booking for the current user.
        
        Args:
            current_user: The authenticated user
            data: Booking data containing:
                - mover_id: ID of the mover
                - pickup_address: {street, city, state, zip_code}
                - dropoff_address: {street, city, state, zip_code}
                - booking_time: ISO datetime string
                - amount: Booking amount
        
        Returns:
            Created Booking object
        """
        # Validate mover exists
        mover = Mover.query.get(data.get('mover_id'))
        if not mover:
            raise ValueError("Mover not found")
        
        # Create pickup address
        pickup_address = Address(
            street=data['pickup_address']['street'],
            city=data['pickup_address']['city'],
            state=data['pickup_address']['state'],
            zip_code=data['pickup_address']['zip_code'],
            user_id=current_user.id
        )
        pickup_address.save()
        
        # Create dropoff address
        dropoff_address = Address(
            street=data['dropoff_address']['street'],
            city=data['dropoff_address']['city'],
            state=data['dropoff_address']['state'],
            zip_code=data['dropoff_address']['zip_code'],
            user_id=current_user.id
        )
        dropoff_address.save()
        
        # Parse booking time
        if isinstance(data['booking_time'], str):
            booking_time = datetime.fromisoformat(data['booking_time'].replace('Z', '+00:00'))
        else:
            booking_time = data['booking_time']
        
        # Create booking
        booking = Booking(
            user_id=current_user.id,
            mover_id=data['mover_id'],
            pickup_address_id=pickup_address.id,
            dropoff_address_id=dropoff_address.id,
            booking_time=booking_time,
            status=BookingStatus.PENDING,
            amount=data.get('amount', 0.00),
            payment_status='PENDING'
        )
        booking.save()
        
        return booking

    @staticmethod
    def get_booking_by_id(booking_id, current_user):
        """
        Get a booking by ID, ensuring the user has access.
        
        Args:
            booking_id: ID of the booking
            current_user: The authenticated user
        
        Returns:
            Booking object if found and user has access
        
        Raises:
            ValueError: If booking not found or user doesn't have access
        """
        booking = Booking.query.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        
        # Check if user owns the booking or is the mover
        if booking.user_id != current_user.id:
            mover = current_user.mover
            if not mover or booking.mover_id != mover.id:
                raise ValueError("Access denied")
        
        return booking

    @staticmethod
    def get_user_bookings(current_user, filters=None):
        """
        Get all bookings for the current user.
        
        Args:
            current_user: The authenticated user
            filters: Optional dict with status, page, limit
        
        Returns:
            Dict with bookings list and pagination info
        """
        query = Booking.query.filter_by(user_id=current_user.id)
        
        if filters and filters.get('status'):
            query = query.filter_by(status=filters['status'])
        
        page = filters.get('page', 1) if filters else 1
        limit = filters.get('limit', 10) if filters else 10
        
        pagination = query.order_by(Booking.created_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        return {
            'bookings': [b.to_dict() for b in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }

