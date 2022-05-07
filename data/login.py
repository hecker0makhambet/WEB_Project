import flask
from flask import render_template, redirect
from flask_login import login_user

from data import db_session
from data.classes import LoginForm, RegisterForm
from data.users import User

login_app = flask.Blueprint('blueprints', __name__, template_folder='templates')


@login_app.route('/login', methods=['POST', 'GET'])  # Вход
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


@login_app.route('/register', methods=['POST', 'GET'])
def register():  # Регистрация
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
