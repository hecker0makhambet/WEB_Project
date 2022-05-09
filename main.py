from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, logout_user, current_user, LoginManager, login_user
from flask_restful import Api

import data
from data import login, user_app, product_app
from data import products_resource, db_session, users_resource
from data.db_session import global_init
from data.products import Product
from data.users import User

global_init('data\\database.db')  # Инициализация БД
app = Flask(__name__)  # Создание Flask-переменной
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()  # Менеджер логинов
login_manager.init_app(app)
app.register_blueprint(data.login.app, name='1')  # Регистрация сторонних модулей
app.register_blueprint(data.product_app.app, name='2')
app.register_blueprint(data.user_app.app, name='3')
api = Api(app)  # API ресурсов
api.add_resource(products_resource.ProductResource, '/api/products/<int:product_id>')  # Добавление ресурсов
api.add_resource(products_resource.ProductListResource, '/api/products/')
api.add_resource(users_resource.UserResource, '/api/users/<int:user_id>')
api.add_resource(users_resource.UserListResource, '/api/users/')


def reload_user():
    pass


@app.route('/logout')
@login_required
def logout():  # Выход из аккаунта
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):  # Загрузка пользователя
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def products_foo(session):  # Страница со списком продуктов
    products = session.query(Product).filter(Product.is_private == False).all()  # Получение всех неприватных продуктов
    products.reverse()  # Сортировка по убыванию даты
    return render_template('main.html', current_user=current_user, products=products, url_for=url_for)


def about_foo(session):  # Страница с информацией о сайте
    return render_template('about.html', current_user=current_user)


def starred_foo(session):  # Страница с избранными товарами
    b = []
    if current_user.is_authenticated:  # Если пользователь авторизовался
        user = session.query(User).get(current_user.id)
        products = session.query(Product).all()
        for i in products:
            if str(i.id) in user.starred.split():  # Если продукт в списке избранных пользователя
                b.append(i)  # Добавить в список
    b.reverse()  # Сортировка по убыванию
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
    if current_user != user:  # Если чужой просматривает страницу этого пользователя
        user_products = session.query(Product).filter(Product.is_private == False, Product.user == user)
        # Получить все его товары, кроме приватных
        params['products'] = user_products
    else:  # Иначе получить все его товары
        user_products = user.products
        params['products'] = user_products
    return render_template('user.html', **params)


@app.route('/like/<int:product_id>', methods=['POST', 'GET', 'PUT'])
def like(product_id):  # Лайк товара
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    user = session.query(User).get(current_user.id)
    user_starred = set(user.starred.split())
    product_starred = set(product.starred.split())
    if str(product_id) in user_starred and str(user.id) in product_starred:  # Если этот товар уже лайкан пользователем
        # Удалить из избранных
        user_starred.remove(str(product_id))
        product_starred.remove(str(user.id))
    else:  # Иначе добавить в избранные
        user_starred.add(str(product_id))
        product_starred.add(str(user.id))
    user.starred = ' '.join(list(user_starred))
    product.starred = ' '.join(list(product_starred))
    product.likes = len(product_starred)
    session.commit()
    logout_user()  # Обновить профиль
    login_user(user)
    return redirect(f'/product/{product_id}')


@app.route('/product/<int:product_id>', methods=['POST', 'GET'])
def get_product(product_id):  # Вывод информации о продукте
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    return render_template('product.html', current_user=current_user, product=product)


@app.route('/<int:action>', methods=['POST', 'GET'])
def main(action=1):  # Главная страница
    session = db_session.create_session()
    a = {1: products_foo(session), 2: about_foo(session), 3: starred_foo(session), 4: filter_foo(session)}
    return a[action]


@app.route('/', methods=['POST', 'GET'])
def welcome():  # Начальная страница
    return render_template('welcome_page.html')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.2')
