from flask import Flask
from app.config import Config
from app.extensions import db, migrate, cors

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
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(mover_bp)
    app.register_blueprint(review_bp)

    return app
