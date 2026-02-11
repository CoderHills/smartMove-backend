from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
bcrypt = Bcrypt()
