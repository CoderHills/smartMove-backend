import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5ead1ae258577a4829d2b623d0497f1e14b0dbb260147424' # Consider setting this via an environment variable in production

    
    # Railway uses postgres:// but SQLAlchemy 1.4+ requires postgresql://
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set for Flask application. Set the DATABASE_URL environment variable.")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
