from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required, logout_user, current_user, LoginManager, login_user
from flask_restful import Api

import data
from data import login, user_app, product_app
from data import products_resource, db_session
from data.db_session import create_session, global_init
from data.products import Product
from data.users import User

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
    b = []
    if current_user.is_authenticated:
        user = session.query(User).get(current_user.id)
        products = session.query(Product).all()
        for i in products:
            if str(i.id) in user.starred.split():
                b.append(i)
    return render_template('starred.html', current_user=current_user, products=b)


def filter_foo(session):
    pass


@app.route('/user/<int:user_id>')  # Вывод профиля пользователя
def get_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    params = {
        'current_user': current_user,
        'user': user
    }
    if current_user != user:
        user_products = session.query(Product).filter(Product.is_private == False, Product.user == user)
        params['products'] = user_products
    else:
        user_products = user.products
        params['products'] = user_products
    return render_template('user.html', **params)


@app.route('/like/<int:product_id>', methods=['POST', 'GET', 'PUT'])
def like(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    user = session.query(User).get(current_user.id)
    user_starred = set(user.starred.split())
    product_starred = set(product.starred.split())
    if str(product_id) in user_starred and str(user.id) in product_starred:
        user_starred.remove(str(product_id))
        product_starred.remove(str(user.id))
    else:
        user_starred.add(str(product_id))
        product_starred.add(str(user.id))
    user.starred = ' '.join(list(user_starred))
    product.starred = ' '.join(list(product_starred))
    product.likes = len(product_starred)
    session.commit()
    logout_user()
    login_user(user)
    return redirect(f'/product/{product_id}')


@app.route('/product/<int:product_id>', methods=['POST', 'GET'])
def get_product(product_id):  # Вывод информации о продукте
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    return render_template('product.html', current_user=current_user, product=product)


@app.route('/<int:action>', methods=['POST', 'GET'])  # Главная страница
def main(action=1):
    session = db_session.create_session()
    a = {1: products_foo(session), 2: about_foo(session), 3: starred_foo(session), 4: filter_foo(session)}
    return a[action]


@app.route('/', methods=['POST', 'GET'])
def welcome():
    return render_template('welcome_page.html')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.2')
