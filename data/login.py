import flask
from flask import render_template, redirect, request
from flask_login import login_user

from data import db_session
from data.users import User

app = flask.Blueprint('login_blueprint', __name__, template_folder='templates')


@app.route('/login', methods=['POST', 'GET'])  # Вход
def login():  # Логин пользователя
    session = db_session.create_session()
    if request.method == 'POST':
        user = session.query(User).filter(User.email == request.form['email']).first()
        if user and user.check_password(request.form['password']):  # Проверка пароля
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль")
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():  # Регистрация
    session = db_session.create_session()
    if request.method == 'POST':
        if request.form['password'] != request.form['confirmpassword']:
            return render_template('register.html', message="Пароли не совпадают")
        user = User(
            name=request.form['name'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])  # Хеширование пароля
        session.add(user)  # Добавление в БД
        session.commit()  # Сохранение БД
        login_user(user)  # Логин пользователя
        return redirect('/')
    return render_template('register.html')
