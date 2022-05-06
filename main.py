from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for
from flask_restful import Api
import data
from data import login, user_app, product_app
from data.db_session import create_session, global_init
from data import products_resource, db_session
from data.users import User
from data.products import Product
from flask_login import login_required, logout_user, current_user, login_user, LoginManager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
import flask
from data.classes import LoginForm, RegisterForm, ProductForm, ProfileForm
global_init('data\\database.db')
create_session()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(data.login.app, name='1')
app.register_blueprint(data.product_app.app, name='2')
app.register_blueprint(data.user_app.app, name='3')
api = Api(app)
api.add_resource(products_resource.ProductResource, '/api/<int:product_id>')
api.add_resource(products_resource.ProductListResource, '/api/')


def reload_user():
    pass


@app.route('/logout')  # Выйти
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def products_foo(session):
    products = session.query(Product).filter(Product.is_private == False).all()
    return render_template('main.html', current_user=current_user, products=products, url_for=url_for)


def about_foo(session):
    return render_template('about.html', current_user=current_user)


def starred_foo(session):
    return render_template('starred.html', current_user=current_user)


def filter_foo(session):
    pass


@app.route('/user/<int:user_id>')  # Вывод профиля пользователя
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if current_user != user:
        products = session.query(Product).filter(Product.is_private == False, Product.user == current_user)
    else:
        products = user.products
    return render_template('user.html', current_user=current_user, user=user, products=products)


@app.route('/product/<int:product_id>')
def get_product(product_id):  # Вывод информации о продукте
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    return render_template('product.html', current_user=current_user, product=product)


@app.route('/', methods=['POST', 'GET'])
@app.route('/<int:action>', methods=['POST', 'GET'])  # Главная страница
def main(action=1):
    session = db_session.create_session()
    a = {1: products_foo(session), 2: about_foo(session), 3: starred_foo(session), 4: filter_foo(session)}
    return a[action]


if __name__ == '__main__':
    app.run()
