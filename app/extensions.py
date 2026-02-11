from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(supports_credentials=True, resources={r"/api/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
bcrypt = Bcrypt()
