from flask import request
from flask_restful import Resource

from db.drinks import DrinkDBModel
from db.db_config import db, redis_store
from api.auth import required_auth
from api.schemas.drinks import DrinkSchema

class DrinkResource(Resource):
    
    def get(Self, drink_id: int):
        try:
            schema = DrinkSchema()
            drink = DrinkDBModel.query.filter_by(id=drink_id).first()
            if not drink:
                return {"message": "drink not found"}, 404
            return {"drink": schema.dump(drink)}, 200
        except Exception as e:
            raise e
        
    @required_auth
    def put(self, drink_id: int):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401

            schema = DrinkSchema(partial=True)
            drink = DrinkDBModel.query.filter_by(id=drink_id).first()
            if not drink:
                return {"message": "drink not found"}, 404
            drink = schema.load(request.json, instance=drink)

            db.session.commit()
            return {"message": "drink updated"}, 200
        except Exception as e:
            raise e

    @required_auth
    def delete(self, drink_id: int):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401
            drink = DrinkDBModel.query.filter_by(id=drink_id).first()
            if not drink:
                return {"message": "post not found"}, 404
            db.session.delete(drink)
            db.session.commit()
            return {"message": "post deleted"}, 200
        except Exception as e:
            raise e
        

class DrinkListResource(Resource):

    @required_auth
    def post(self):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))

            if not user_id:
                return {"message": "Unauthorized"}, 401
            data = request.json
            # data["user_id"] = user_id
            schema = DrinkSchema()
            drink = schema.load(data)

            db.session.add(drink)
            db.session.commit()
            return {'message': 'Drink created successfully'}, 201
        except Exception as a:
            raise a


    def get(self):
        # user_id = request.args.get('user_id')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        ordering = request.args.get('ordering', default='asc')

        query = DrinkDBModel.query
        # if user_id:
        #     query = query.filter_by(user_id=user_id)

        if ordering == 'asc':
            query = query.order_by(DrinkDBModel.created_at)
        elif ordering == 'desc':
            query = query.order_by(DrinkDBModel.created_at.desc())

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        schema = DrinkSchema(many=True)
        posts = query.all()

        return {'drinks': schema.dump(posts)}, 200
