from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, cors
from app.utils.errors import register_error_handlers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints
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
    from app.routes.payments import payment_bp
    # Inside your create_app() function

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(mover_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(maps_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(payment_bp, url_prefix="/api/payments")

    # Register error handlers
    register_error_handlers(app)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    from flask import (
        jsonify,
    )  # Import jsonify here or at the top if not already present

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"}), 200

    return app