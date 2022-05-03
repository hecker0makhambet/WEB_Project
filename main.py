from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_restful import Api
from data.blueprints import blueprint
from data.db_session import create_session, global_init
from data import products_resource, db_session
from data.users import User
from data.products import Product
from flask_login import login_required, logout_user, current_user, login_user, LoginManager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
import flask
global_init('data\\database.db')
create_session()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(blueprint)
api = Api(app)
api.add_resource(products_resource.ProductResource, '/api/<int:product_id>')
api.add_resource(products_resource.ProductListResource, '/api/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("LOGIN")


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField("SIGN UP")


@app.route('/', methods=['POST', 'GET'])
def main():
    return make_response(render_template('main.html', current_user=current_user))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        e_mail = db_sess.query(User).filter(User.email == form.email.data).first()
        if e_mail:
            return render_template('register.html',
                                   message="Email уже зарегистрирован",
                                   form=form)
        if form.password.data != form.confirm_password.data:
            return render_template('register.html',
                                   message="Пароли не совпадают",
                                   form=form)
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
