from flask import jsonify


def success_response(data=None, message="Operation successful", status_code=200):
    """Standardized success response format."""
    return jsonify({"status": "success", "message": message, "data": data}), status_code


def error_response(message="An error occurred", status_code=400, errors=None):
    """Standardized error response format."""
    payload = {"status": "error", "message": message}
    if errors:
        payload["errors"] = errors
    return jsonify(payload), status_code
