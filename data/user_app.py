import os

import flask
from flask import render_template, url_for
from flask_login import logout_user, current_user, login_user

from data import db_session
from data.classes import ProfileForm, AvatarForm, PasswordChangeForm
from data.users import User

user_app = flask.Blueprint('blueprints', __name__, template_folder='templates')


def mkdir(path, direct):
    a = os.getcwd()
    path = os.path.join(a, path, direct)
    if os.path.isdir(path):
        return
    os.mkdir(path)


@user_app.route('/profile', methods=['POST', 'GET'])
def profile():  # Профиль текущего пользователя
    form = AvatarForm()
    form2 = ProfileForm()
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if user.avatar_name != None:
        url1 = url_for('static', filename=f'images/users/{user.id}/{user.avatar_name}')
    else:
        url1 = "https://avatars.mds.yandex.net/get-pdb/1996600/d1725ec1-41d3-4b2c-ab24-91ec603557bf/s375"
    if form2.is_submitted():
        if form.Avatar.data:
            mkdir('static\\images\\users', str(user.id))
            with open(f'static\\images\\users\\{str(user.id)}\\{form.Avatar.data.filename}', 'wb') as r:
                r.write(form.Avatar.data.read())
                r.close()
            url1 = url_for('static', filename=f'images/users/{user.id}/{str(form.Avatar.data.filename)}')
            user.avatar_name = form.Avatar.data.filename
        if form2.name.data:
            user.name = form2.name.data
        if form2.about.data:
            user.about = form2.about.data
        if form2.email.data:
            user.email = form2.email.data
        session.commit()
        logout_user()
        login_user(user)
        # reload_user()
        return render_template('profile.html', current_user=current_user, user=user, url1=url1, form=form, form2=form2)
    if form.is_submitted():

        return render_template('profile.html', current_user=current_user, user=user, url1=url1, form=form, form2=form2)
    return render_template('profile.html', current_user=current_user, user=user, url1=url1, form=form, form2=form2)


@user_app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    form = PasswordChangeForm()
    session = db_session.create_session()
    user = session.query(User).get(current_user.id)
    if form.is_submitted():
        if not user.check_password(form.old_password.data):
            return render_template('password_change.html', current_user=current_user,
                                   form=form, message='Incorrect password')
        if form.confirm_password.data != form.new_password.data:
            return render_template('password_change.html', current_user=current_user,
                                   form=form, message='Пароли не совпадают')
        user.set_password(form.new_password.data)
        # user.hashed_password = generate_password_hash(form.new_password)
        session.commit()
        render_template('password_change.html', current_user=current_user, form=form, message="Пароль успешно изменен")
    return render_template('password_change.html', current_user=current_user, form=form)
