from db.db_config import db
from werkzeug.security import generate_password_hash


class UserDBModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name: str, email: str, login: str, password: str) -> None:
        self.name = name
        self.email = email
        self.login = login
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.active
    
    def get_id(self):
        return self.id
    
    def __repr__(self):
        return "<User %s>" % self.username