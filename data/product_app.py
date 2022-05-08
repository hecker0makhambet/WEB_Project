import flask
from flask import render_template, redirect, request
from flask_login import current_user

from data import db_session
from data.classes import ProductForm, ProductEditForm
from data.products import Product
from data.user_app import mkdir

app = flask.Blueprint('product_blueprint', __name__, template_folder='templates')


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    form = ProductForm()
    # if request.method == 'POST':
    #     print(0)
    #     print(request.form['AvatarFile'])
    #     print(request.form['Name'])
    #     print(request.form['About'])
    #     print(request.form['Price'])
    #     print(request.form['is_private'])
    #     return render_template('add_product.html', current_user=current_user,
    #                        form=form)
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
        return redirect('/1')
    return render_template('add_product.html', current_user=current_user,
                           form=form)


@app.route('/delete_product/<int:product_id>', methods=['POST', 'GET'])
def delete_product(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if request.method == 'POST':
        session.delete(product)
        session.commit()
        return redirect('/')
    return render_template('delete_product.html', current_user=current_user)


@app.route('/edit_product/<int:product_id>', methods=['POST', 'GET'])
def edit_product(product_id):
    form = ProductEditForm()
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if form.is_submitted():
        if form.name.data:
            product.name = form.name.data
        if form.about.data:
            product.about = form.about.data
        if form.price.data:
            product.price = form.price.data
        if form.is_private.data:
            product.is_private = form.is_private
        session.commit()
        return render_template('edit_product.html', current_user=current_user, product=product, form=form,
                               message='Success')
    return render_template('edit_product.html', current_user=current_user, product=product, form=form)