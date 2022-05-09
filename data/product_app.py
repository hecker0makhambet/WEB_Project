import flask
from flask import render_template, redirect, request
from flask_login import current_user

from data import db_session
from data.classes import ProductForm, ProductEditForm
from data.products import Product
from data.user_app import mkdir

app = flask.Blueprint('product_blueprint', __name__, template_folder='templates')


@app.route('/add_product', methods=['POST', 'GET'])
def add_product():  # Добавление товара
    form = ProductForm()
    if form.is_submitted():  # Если форму заполнили
        session = db_session.create_session()
        product = Product(
            name=form.name.data,
            about=form.about.data,
            price=form.price.data,
            user_id=current_user.id,
            is_private=form.is_private.data
        )
        session.add(product)  # Добавление продуктов
        product = session.query(Product).all()[-1]
        if form.Avatar.data:  # Если пользователь выбрал изображение
            mkdir('static\\images\\products', str(product.id))  # Создание директории для продукта
            with open(f'static\\images\\products\\{product.id}\\{form.Avatar.data.filename}', 'wb') as r:
                # Создание изображения
                r.write(form.Avatar.data.read())
                r.close()
            product.avatar_name = form.Avatar.data.filename  # Установка изображения
        session.commit()  # Сохранение изменений
        return redirect('/1')
    return render_template('add_product.html', current_user=current_user,
                           form=form)


@app.route('/delete_product/<int:product_id>', methods=['POST', 'GET'])
def delete_product(product_id):  # Удаление продукта
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if request.method == 'POST':  # Если нажали submit
        session.delete(product)  # Удалить продукт
        session.commit()  # Сохранить изменения
        return redirect('/')
    return render_template('delete_product.html', current_user=current_user)


@app.route('/edit_product/<int:product_id>', methods=['POST', 'GET'])
def edit_product(product_id):  # Изменение продукта
    form = ProductEditForm()
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if form.is_submitted():  # Если заполнили форму
        if form.name.data:  # Если заполнили поле имя
            product.name = form.name.data  # Изменить имя
        if form.about.data:  # Если заполнили поле доп. информации
            product.about = form.about.data  # Изменить доп. информацию
        if form.price.data:  # Если заполнили поле цены
            product.price = form.price.data  # Изменить цену
        if form.is_private.data:  # Если заполнили поле приватности
            product.is_private = form.is_private  # Изменить приватность
        session.commit()  # Сохранить изменения
        return render_template('edit_product.html', current_user=current_user, product=product, form=form,
                               message='Success')
    return render_template('edit_product.html', current_user=current_user, product=product, form=form)