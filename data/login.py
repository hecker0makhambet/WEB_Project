import flask
from flask import render_template, redirect, request
from flask_login import login_user

from data import db_session
from data.classes import LoginForm, RegisterForm
from data.users import User

app = flask.Blueprint('login_blueprint', __name__, template_folder='templates')


@app.route('/login', methods=['POST', 'GET'])  # Вход
def login():
    session = db_session.create_session()
    if request.method == 'POST':
        user = session.query(User).filter(User.email == request.form['email']).first()
        if user and user.check_password(request.form['password']):
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
        user.set_password(request.form['password'])
        session.add(user)
        session.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html')
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
