from flask import jsonify


def success(data=None, message="Success", status_code=200):
    return jsonify({"status": "success", "message": message, "data": data}), status_code


def error(message="Error", status_code=400, errors=None):
    return jsonify(
        {"status": "error", "message": message, "errors": errors}
    ), status_code
