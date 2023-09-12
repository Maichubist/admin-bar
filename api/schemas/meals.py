from flask_marshmallow import Marshmallow

from db.meals import MealDBModel
from db.db_config import db

ma = Marshmallow()

class MealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MealDBModel
        load_instance = True
        sqla_session = db.session

    title = ma.String(required=True)
    description = ma.String(required=False)
    ingredients = ma.String(required=False)
    weight = ma.String(required=False)
    price = ma.String(required=True)
    photo = ma.String(required=False)