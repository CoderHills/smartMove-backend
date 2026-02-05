from flask import request


def init_cors(app):
    @app.after_request
    def add_cors_headers(response):
        # In production, replace '*' with your specific frontend URL
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
