from flask import Blueprint, request
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required, admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required
@admin_required
def get_dashboard_data(current_user):
    """
    An example route for an admin dashboard.
    """
    try:
        # In a real application, you'd fetch and return actual dashboard data.
        # For example, number of users, recent bookings, system stats, etc.
        dashboard_data = {
            "message": "Welcome to the admin dashboard!",
            "user_count": 150,
            "recent_bookings": 5,
            "system_health": "OK"
        }
        return success(dashboard_data)
    except Exception as e:
        return error_response(str(e), 500)

