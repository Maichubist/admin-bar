import os

class Config:
    DEBUG = os.environ.get('DEBUG', False)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    REDIS_URL = 'redis://localhost:6379/0'
    UPLOADED_PHOTOS_DEST = 'static'