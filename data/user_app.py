import os

import flask
from flask import render_template, url_for
from flask_login import logout_user, current_user, login_user

from data import db_session
from data.classes import ProfileForm, AvatarForm, PasswordChangeForm
from data.users import User

app = flask.Blueprint('user_blueprint', __name__, template_folder='templates')


def mkdir(path, direct):
    a = os.getcwd()
    path = os.path.join(a, path, direct)
    if os.path.isdir(path):
        return
    os.mkdir(path)


@app.route('/profile', methods=['POST', 'GET'])
def profile():  # Профиль текущего пользователя
    form = AvatarForm()
    form2 = ProfileForm()
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if user.avatar_name:  # Если у пользователя ест аватар, показать аватар
        url1 = url_for('static', filename=f'images/users/{user.id}/{user.avatar_name}')
    else:  # Иначе показать изображение по умолчанию
        url1 = url_for('static', filename=f'images/prog/s375.webp')
    if form2.is_submitted():  # Если заполнили форму
        if form.Avatar.data:  # Если выбрали аватар
            mkdir('static\\images\\users', str(user.id))  # Создать директорию для пользователя
            with open(f'static\\images\\users\\{str(user.id)}\\{form.Avatar.data.filename}', 'wb') as r:
                # Создать изображение
                r.write(form.Avatar.data.read())
                r.close()
            url1 = url_for('static', filename=f'images/users/{user.id}/{str(form.Avatar.data.filename)}')
            user.avatar_name = form.Avatar.data.filename  # Установить изображение
        if form2.name.data:  # Если заполнили поле имя
            user.name = form2.name.data  # Изменить имя
        if form2.about.data:  # Если заполнили поле доп. информации
            user.about = form2.about.data  # Изменить доп. информацию
        if form2.email.data:  # Если заполнили поле email
            user.email = form2.email.data  # Изменить email
        session.commit()  # Сохранить изменения
        logout_user()  # Обновить профиль
        login_user(user)
        return render_template('profile.html', current_user=current_user, user=user, url1=url1, form=form, form2=form2)
    if form.is_submitted():
        return render_template('profile.html', current_user=current_user, user=user, url1=url1, form=form, form2=form2)
    return render_template('profile.html', current_user=current_user, user=user, url1=url1, form=form, form2=form2)


@app.route('/change_password', methods=['POST', 'GET'])
def change_password():  # Смена пароля
    form = PasswordChangeForm()
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if form.is_submitted():  # Если заполнили форму
        if not user.check_password(form.old_password.data):  # Если пароль неправильный
            return render_template('password_change.html', current_user=current_user,
                                   form=form, message='Incorrect password')
        if form.confirm_password.data != form.new_password.data:  # Если пароли не совпадают
            return render_template('password_change.html', current_user=current_user,
                                   form=form, message='Пароли не совпадают')
        user.set_password(form.new_password.data)  # Установить новый пароль(хэшированный)
        # user.hashed_password = generate_password_hash(form.new_password)
        session.commit()  # Сохранить изменения
        render_template('password_change.html', current_user=current_user, form=form, message="Пароль успешно изменен")
    return render_template('password_change.html', current_user=current_user, form=form)
