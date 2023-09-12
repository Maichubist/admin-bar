from flask_admin.form.upload import FileUploadField
from wtforms.fields import MultipleFileField
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from datetime import datetime


from admin.common import AdminModelView
from db.db_config import db
from db.product_photo import DrinkPhotoDBModel

class UserAdminModelView(AdminModelView):
    
    column_list = ["login", "email", "active", "password"]
    column_exclude_list = ("password")
    column_labels = {
        "login": "Логін",
        "password": "Пароль",
        "active": "Aктивований",
        "email": "Пошта",
    }
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = generate_password_hash(form.password.data)
        else:
            old_password = form.password.object_data
            if not old_password == model.password:
                model.password = generate_password_hash(form.password.data)



class DrinksAdminModelView(AdminModelView):

    column_list = ["title", "description", "ingredients", "weight", "price", "created_at", "photo_1", "photo_2", "photo_3"]
    form_extra_fields = {
        'photo_1': FileUploadField('Product Photo 1', base_path='static/drinks'),
        'photo_2': FileUploadField('Product Photo 2', base_path='static/drinks'), 
        'photo_3': FileUploadField('Product Photo 3', base_path='static/drinks')
    }
    column_labels = {
        "title": "Заголовок",
        "description": "Опис",
        "ingredients": "Інгредієнти",
        "weight": "Вага/Об'єм",
        "price": "Ціна", 
        "created_at":"Створено", 
        "photo_1": "Зображення 1",
        "photo_2": "Зображення 2",
        "photo_3": "Зображення 3",
    }

    def on_model_change(self, form,  model, is_created):
        now = datetime.now()
        if is_created:
            model.needs_creation_date = now
        else:
            model.needs_modidfication_date = now

    def create_model(self, form):
        model = super(DrinksAdminModelView, self).create_model(form)
        self.save_photos(model, form)
        return model

    def update_model(self, form, model):
        model = super(DrinksAdminModelView, self).update_model(form, model)
        self.save_photos(model, form)
        return model

    def save_photos(self, model, form):
        if 'photo' in form:
            photos = form.photo.data
            for photo in photos:
                if photo:
                    filename = secure_filename(photo.filename)
                    file_path = f"static/drinks/{filename}"
                    photo.save(file_path)
                    product_photo = DrinkPhotoDBModel(product=model, photo_filename=filename)
                    db.session.add(product_photo)
            db.session.commit()


class MealsAdminModelView(AdminModelView):

    column_list = ["title", "description", "ingredients", "weight", "price", "created_at", "photo_1", "photo_2", "photo_3"]
    form_extra_fields = {
        'photo_1': FileUploadField('Product Photo 1', base_path='static/meals'),
        'photo_2': FileUploadField('Product Photo 2', base_path='static/meals'), 
        'photo_3': FileUploadField('Product Photo 3', base_path='static/meals')
    }
    
    column_labels = {
        "title": "Заголовок",
        "description": "Опис",
        "ingredients": "Інгредієнти",
        "weight": "Вага/Об'єм",
        "price": "Ціна", 
        "created_at":"Створено", 
        "photo_1": "Зображення 1",
        "photo_2": "Зображення 2",
        "photo_3": "Зображення 3",
        
    }

    def on_model_change(self, form,  model, is_created):
        now = datetime.now()
        if is_created:
            model.needs_creation_date = now
        else:
            model.needs_modidfication_date = now

    def create_model(self, form):
        model = super(MealsAdminModelView, self).create_model(form)
        self.save_photos(model, form)
        return model

    def update_model(self, form, model):
        model = super(MealsAdminModelView, self).update_model(form, model)
        self.save_photos(model, form)
        return model
    
    def save_photos(self, model, form):
        if 'photo' in form:
            photos = form.photo.data
            for photo in photos:
                if photo:
                    filename = secure_filename(photo.filename)
                    file_path = f"static/drinks/{filename}"
                    photo.save(file_path)
                    product_photo = DrinkPhotoDBModel(product=model, photo_filename=filename)
                    db.session.add(product_photo)
            db.session.commit()