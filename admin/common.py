from wtforms import form, fields, validators

from flask import redirect, url_for, request, current_app
import flask_login as login
from flask_admin import AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView
from passlib.context import CryptContext
from werkzeug.security import check_password_hash

from db.db_config import db
from db.users import UserDBModel


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class AdminModelView(ModelView):
    
    create_modal = True
    edit_modal = True
    

    def is_accessible(self):
        return login.current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


def configure_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(UserDBModel).get(user_id)
    

# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(label="Логін", validators=[validators.InputRequired()])
    password = fields.PasswordField(label="Пароль", validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Невірний логін')

        # we're comparing hashes
        salt = current_app.config.get("SECRET_KEY").encode("utf-8")
        if not check_password_hash(user.password, self.password.data):
            print(check_password_hash(user.password, self.password.data), user.password, self.password.data)
            raise validators.ValidationError('Невірний пароль')
        
        # if not user.admin:
        #     raise validators.ValidationError('Користувач не адміністратор')

    def get_user(self):
        return db.session.query(UserDBModel).filter_by(login=self.login.data).first()


class CustomAdminIndexView(AdminIndexView):
    
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(CustomAdminIndexView, self).index()
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(CustomAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))