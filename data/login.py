import flask
from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for
from flask_restful import Api
from .db_session import create_session, global_init
from . import products_resource
from . import db_session
from .users import User
from .products import Product
from flask_login import login_required, logout_user, current_user, login_user, LoginManager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
from .classes import LoginForm, RegisterForm, ProductForm, ProfileForm


app = flask.Blueprint('blueprints', __name__, template_folder='templates')


@app.route('/login', methods=['POST', 'GET'])  # Вход
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
