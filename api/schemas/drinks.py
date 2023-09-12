from flask_marshmallow import Marshmallow

from db.drinks import DrinkDBModel
from db.db_config import db

ma = Marshmallow()

class DrinkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DrinkDBModel
        load_instance = True
        sqla_session = db.session

    title = ma.String(required=True)
    description = ma.String(required=False)
    ingredients = ma.String(required=False)
    weight = ma.String(required=False)
    price = ma.String(required=True)
    photo = ma.String(required=False)