from db.db_config import db

# class MealPhotoDBModel(db.Model):
#     __tablename__ = "Meal photo"

#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)
#     filename = db.Column(db.String(255), nullable=False)

class DrinkPhotoDBModel(db.Model):
    __tablename__ = 'drink_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    photo_filename = db.Column(db.String(255))
    
    # Define a foreign key relationship with the Drink model
    product_id = db.Column(db.Integer, db.ForeignKey('drinks.id'))
    product = db.relationship('DrinkDBModel', backref='photos')
    
    # Add other fields as needed

    def __init__(self, photo_filename, product=None):
        self.photo_filename = photo_filename
        self.product = product