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


@app.route('/add_product')
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        product = Product(
            name=form.name.data,
            about=form.about.data,
            price=form.price.data,
        )


@app.route('/delete_product')
def delete_product():
    pass
