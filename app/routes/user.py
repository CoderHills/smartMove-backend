from flask import Blueprint, request
from app.models.user import User
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/profile', methods=['GET'])
@jwt_required
def get_profile(current_user):
    return success(current_user.to_dict())

@user_bp.route('/profile', methods=['PUT'])
@jwt_required
def update_profile(current_user):
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(current_user, key, value)
        current_user.save()
        return success(current_user.to_dict())
    except Exception as e:
        return error_response(str(e))
