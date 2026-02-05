from flask_cors import CORS

def setup_cors(app):
    CORS(app, resources={r"/*": {"origins": "*"}}) # Allow all origins for development, refine for production
