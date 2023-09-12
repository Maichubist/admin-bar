from flask_marshmallow import Marshmallow

from werkzeug.security import generate_password_hash
from db.users import UserDBModel
from db.db_config import db

ma = Marshmallow()
#
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDBModel
        sqla_session = db.session
        load_instance = True

    name = ma.String(required=True)      
    email = ma.String(required=True)      
    login = ma.String(required=True)        
    password = ma.String(load_only=True, required=True)      

    def load_password(self, value):
        return generate_password_hash(value)