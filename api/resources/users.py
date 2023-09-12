from datetime import datetime, timedelta

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from werkzeug.security import check_password_hash
import jwt

from db.users import UserDBModel
from db.db_config import db, redis_store
from api.schemas.users import UserSchema
from config import Config
from api.auth import required_auth


class RegistrationResource(Resource):
    def post(self):
        try:
            schema = UserSchema()
            user = schema.load(request.json)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {'message': 'User already exists'}, 409
        except Exception as e:
            raise e
        return {'message': 'User registered successfully'}, 201
    

class UserResource(Resource):

    @required_auth
    def delete(self, user_id):
        try:
            user = redis_store.get(request.headers.get("Authorization"))
            if not user:
                return {"message": "Unauthorized"}, 401
            if not int(user.decode('utf-8')) ==  user_id or not int(user.decode('utf-8')) == 1:
                return {"message": "You are not allowed to do this action"}, 401
        
            user_to_delete = UserDBModel.query.filter_by(id=user_id).first()
            db.session.delete(user_to_delete)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 201
        except Exception as e:
            raise e

    @required_auth 
    def put(self, user_id):
        try:
            user = redis_store.get(request.headers.get("Authorization"))
            if not user:
                return {"message": "Unauthorized"}, 401
            if not int(user.decode('utf-8')) ==  user_id or not int(user.decode('utf-8')) == 1:
                return {"message": "You are not allowed to do this action"}, 401

            schema = UserSchema(partial=True)
            user_to_update = UserDBModel.query.filter_by(id=user_id).first()
            if not user_to_update:
                return {"message": "user not found"}, 404
            user_to_update = schema.load(request.json, instance=user_to_update)

            db.session.commit()
            return {"message": "user updated"}, 200
        except Exception as e:
            raise e


class LoginResource(Resource):
    def post(self):
        try:
            auth = request.json
            user = UserDBModel.query.filter_by(login=auth.get("login")).first()
            if user:
                if check_password_hash(user.password, auth.get("password")):
                    token = jwt.encode(
                        {
                            "user_id": user.id,
                            "exp": datetime.utcnow() + timedelta(days=1)
                        },
                        Config.JWT_SECRET_KEY,
                        algorithm="HS256")
                    redis_store.set(token, user.id, ex=86400)
                    return {"token": token}, 200
            return {"message": "Invalid credentials"}, 401
        except Exception as e:
            print("Error:", e)  # Add this line for debugging
            raise e



class LogoutResource(Resource):
    @required_auth
    def post(self):
        try:
            token = request.headers.get("Authorization")
            if redis_store.exists(token):
                redis_store.delete(token)
                return {"message": "Logout successful"}, 200
            else:
                return {"message": "Token not found"}, 404
        except Exception as e:
            raise e
        
class RestorePasswordResource(Resource):

    ...