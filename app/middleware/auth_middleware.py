from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.response import error_response


def check_auth():
    """
    Optional global middleware check.
    Can be used in app.before_request to protect all routes except auth.
    """
    # List of endpoints that don't require authentication
    open_endpoints = ["auth.login", "auth.register", "static"]

    if request.endpoint in open_endpoints:
        return None

    try:
        verify_jwt_in_request()
    except Exception as e:
        return error_response("Missing or invalid authentication token", 401)
