from flask import request
from flask_restful import Resource

from db.meals import MealDBModel
from db.db_config import db, redis_store
from api.auth import required_auth
from api.schemas.meals import MealSchema

class MealResource(Resource):
    
    def get(Self, meal_id: int):
        try:
            schema = MealSchema()
            meal = MealDBModel.query.filter_by(id=meal_id).first()
            if not meal:
                return {"message": "meal not found"}, 404
            return {"meal": schema.dump(meal)}, 200
        except Exception as e:
            raise e
        
    @required_auth
    def put(self, meal_id: int):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401

            schema = MealSchema(partial=True)
            meal = MealDBModel.query.filter_by(id=meal_id).first()
            if not meal:
                return {"message": "meal not found"}, 404
            meal = schema.load(request.json, instance=meal)

            db.session.commit()
            return {"message": "meal updated"}, 200
        except Exception as e:
            raise e

    @required_auth
    def delete(self, meal_id: int):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))
            if not user_id:
                return {"message": "Unauthorized"}, 401
            meal = MealDBModel.query.filter_by(id=meal_id).first()
            if not meal:
                return {"message": "meal not found"}, 404
            db.session.delete(meal)
            db.session.commit()
            return {"message": "meal deleted"}, 200
        except Exception as e:
            raise e
        

class MealListResource(Resource):

    @required_auth
    def post(self):
        try:
            user_id = redis_store.get(request.headers.get("Authorization"))

            if not user_id:
                return {"message": "Unauthorized"}, 401
            data = request.json
            # data["user_id"] = user_id
            schema = MealSchema()
            meal = schema.load(data)

            db.session.add(meal)
            db.session.commit()
            return {'message': 'Meal created successfully'}, 201
        # except TypeError:
        #     return {"message": "post not found"}, 404
        except Exception as a:
            raise a


    def get(self):
        # user_id = request.args.get('user_id')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int)
        ordering = request.args.get('ordering', default='asc')

        query = MealDBModel.query
        # if user_id:
        #     query = query.filter_by(user_id=user_id)

        if ordering == 'asc':
            query = query.order_by(MealDBModel.created_at)
        elif ordering == 'desc':
            query = query.order_by(MealDBModel.created_at.desc())

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        schema = MealSchema(many=True)
        posts = query.all()

        return {'meals': schema.dump(posts)}, 200
