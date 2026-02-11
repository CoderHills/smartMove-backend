from flask import Flask, jsonify, request
from app.config import Config
from app.extensions import db, migrate, cors, bcrypt
from app.utils.errors import register_error_handlers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints with /api prefix
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.booking import booking_bp
    from app.routes.mover import mover_bp
    from app.routes.review import review_bp
    from app.routes.admin import admin_bp
    from app.routes.chat import chat_bp
    from app.routes.inventory import inventory_bp
    from app.routes.maps import maps_bp
    from app.routes.notification import notification_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(booking_bp, url_prefix='/api/booking')
    app.register_blueprint(mover_bp, url_prefix='/api/mover')
    app.register_blueprint(review_bp, url_prefix='/api/review')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(maps_bp, url_prefix='/api/maps')
    app.register_blueprint(notification_bp, url_prefix='/api/notification')

    # Register error handlers
    register_error_handlers(app)

    # Add CORS headers to all responses
    @app.after_request
    def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Handle OPTIONS requests globally
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            return '', 200

    # Health check endpoint for Render/load balancers
    @app.route('/health', methods=['GET', 'HEAD', 'OPTIONS'])
    def health_check():
        """Basic health check - returns 200 if app is running."""
        return jsonify({"status": "ok"}), 200

    @app.route('/health/ready', methods=['GET', 'HEAD', 'OPTIONS'])
    def readiness_check():
        """Readiness check - verifies database connectivity."""
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({"status": "ready", "database": "connected"}), 200
        except Exception as e:
            return jsonify({"status": "not ready", "database": "disconnected", "error": str(e)}), 503

    return app
