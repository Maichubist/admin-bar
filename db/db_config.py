from flask_sqlalchemy import SQLAlchemy
import redis

from config import Config

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        return db


redis_store = redis.from_url(Config.REDIS_URL)