import flask
from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for
from flask_restful import Api
from data.db_session import create_session, global_init
from data import products_resource
from data import db_session
from data.users import User
from data.products import Product
from flask_login import login_required, logout_user, current_user, login_user, LoginManager
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
from data.classes import LoginForm, RegisterForm, ProductForm, ProfileForm
from data.user_app import mkdir

app = flask.Blueprint('blueprints', __name__, template_folder='templates')


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    form = ProductForm()
    if form.is_submitted():
        session = db_session.create_session()
        product = Product(
            name=form.name.data,
            about=form.about.data,
            price=form.price.data,
            user_id=current_user.id,
            is_private=form.is_private.data
        )
        session.add(product)
        product = session.query(Product).all()[-1]
        if form.Avatar.data:
            mkdir('static\\images\\products', str(product.id))
            with open(f'static\\images\\products\\{product.id}\\{form.Avatar.data.filename}', 'wb') as r:
                r.write(form.Avatar.data.read())
                r.close()
            product.avatar_name = form.Avatar.data.filename
        session.commit()
        return render_template('add_product.html', current_user=current_user,
                               form=form, product=product)
    return render_template('add_product.html', current_user=current_user,
                           form=form)


@app.route('/delete_product')
def delete_product():
    pass


@app.route('/edit_product')
def edit_product():
    pass