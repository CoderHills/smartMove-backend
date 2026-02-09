from functools import wraps
from flask import request
from app.utils.response import error_response
import time

# Simple in-memory storage for rate limiting
# WARNING: This in-memory rate limiter is NOT suitable for production environments
# with multiple worker processes or instances, as state is not shared.
# For production, consider using a dedicated rate-limiting library like Flask-Limiter
# with a distributed backend (e.g., Redis).
_request_counts = {}
_last_request_time = {}

def rate_limit(limit, per):
    """
    A simple rate limiting decorator.
    :param limit: Maximum number of requests.
    :param per: Time window in seconds.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()

            if client_ip not in _request_counts:
                _request_counts[client_ip] = 0
                _last_request_time[client_ip] = current_time

            # Reset count if time window has passed
            if current_time - _last_request_time[client_ip] > per:
                _request_counts[client_ip] = 0
                _last_request_time[client_ip] = current_time

            _request_counts[client_ip] += 1

            if _request_counts[client_ip] > limit:
                return error_response(f"Too Many Requests: Rate limit exceeded. Try again in {per} seconds.", 429)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
