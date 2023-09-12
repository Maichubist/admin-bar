from flask import Flask, Blueprint, render_template
from flask_restful import Api
from flask_admin import Admin, AdminIndexView, BaseView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_uploads import UploadSet, configure_uploads, IMAGES

import os

from api.resources.drinks import DrinkResource, DrinkListResource
from api.resources.meals import MealResource, MealListResource
from api.resources.users import RegistrationResource, LoginResource, LogoutResource, UserResource, RestorePasswordResource
from config import Config
from db.db_config import init_db, db
from db.drinks import DrinkDBModel
from db.meals import MealDBModel
from db.users import UserDBModel
from db.product_photo import DrinkPhotoDBModel
from admin.common import CustomAdminIndexView, configure_login
from admin.admin_model_view import UserAdminModelView, MealsAdminModelView, DrinksAdminModelView



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = "secret_key"
    configure_login(app)
    photos = UploadSet("photos", IMAGES)
    configure_uploads(app, photos)
    
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(RegistrationResource, '/registration')
    api.add_resource(UserResource, '/user/<int:meal_id>')
    api.add_resource(LoginResource, '/login')
    api.add_resource(LogoutResource, '/logout')
    api.add_resource(RestorePasswordResource, '/restore-password')
    api.add_resource(MealListResource, '/meals')
    api.add_resource(MealResource, '/meals/<int:meal_id>')
    api.add_resource(DrinkListResource, '/drinks')
    api.add_resource(DrinkResource, '/drinks/<int:drink_id>')

    app.register_blueprint(api_bp)

    admin = Admin(app, name='Admin Site', template_mode='bootstrap4', endpoint='admin', base_template='master.html', index_view=CustomAdminIndexView())
    admin.add_view(UserAdminModelView(UserDBModel, db.session, name='Користувачі'))
    admin.add_view(MealsAdminModelView(MealDBModel, db.session, name='Страви'))
    admin.add_view(DrinksAdminModelView(DrinkDBModel, db.session, name='Напої'))
    path = os.path.join(os.path.dirname(__file__), 'static')
    admin.add_view(FileAdmin(path, '/static/', name='Файловий Менеджер'))
    

    return app

app = create_app()
db = init_db(app)


if __name__ == '__main__':
    app.run(debug=True)


