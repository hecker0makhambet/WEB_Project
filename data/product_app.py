import flask
from flask import render_template
from flask_login import current_user

from data import db_session
from data.classes import ProductForm
from data.products import Product
from data.user_app import mkdir

product_app = flask.Blueprint('blueprints', __name__, template_folder='templates')


@product_app.route('/add_product', methods=['POST', 'GET'])
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


@product_app.route('/delete_product')
def delete_product():
    pass


@product_app.route('/edit_product')
def edit_product():
    pass