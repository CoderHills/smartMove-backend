from functools import wraps
from flask import request
from app.utils.response import error

def validate_request(*expected_args):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return error("Request must be JSON", 400)
            
            data = request.get_json()
            for arg in expected_args:
                if arg not in data:
                    return error(f"Missing argument: {arg}", 400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
