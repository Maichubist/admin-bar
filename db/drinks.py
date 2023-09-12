from db.db_config import db

class DrinkDBModel(db.Model):
    __tablename__ = "drinks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    ingredients = db.Column(db.String, nullable=True)
    weight = db.Column(db.String, nullable=True)
    price = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    photo_1 = db.Column(db.String, nullable=True)
    photo_2 = db.Column(db.String, nullable=True)
    photo_3 = db.Column(db.String, nullable=True)

    def __init__(self, title: str, description: str, ingredients: str, weight: str, price: str, photo1: str, photo3: str, photo2: str ) -> None:
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.weight = weight
        self.price = price
        self.photo_1 = photo1
        self.photo_2 = photo2
        self.photo_3 = photo3