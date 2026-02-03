from functools import wraps
from flask import request
from app.utils.response import error

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Placeholder for JWT token verification
        # For migration purposes, we are bypassing the actual JWT check.
        # This will need to be properly implemented once Auth is set up.
        return f(*args, **kwargs) # Call the function directly
    return decorated_function

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Placeholder for role checking
            # For migration purposes, we are bypassing the actual role check.
            # This will need to be properly implemented.
            return f(*args, **kwargs) # Call the function directly
        return decorated_function
    return decorator