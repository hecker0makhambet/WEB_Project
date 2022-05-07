from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, IntegerField, FileField,\
    TextAreaField


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("LOGIN")


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField("SIGN UP")


class ProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    about = TextAreaField('about', validators=[DataRequired()])
    price = IntegerField('price(KZT)', validators=[DataRequired()])
    is_private = BooleanField('is_private')
    Avatar = FileField('Choose avatar')
    submit = SubmitField('ADD', validators=[DataRequired()])


class AvatarForm(FlaskForm):
    Avatar = FileField('Edit avatar')
    submit = SubmitField('Save avatar', name='avatar')


class ProfileForm(FlaskForm):
    name = StringField('Edit name')
    about = TextAreaField('Edit info about me')
    email = EmailField('Edit email')
    submit = SubmitField('Save changes')


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Save changes')


class ProductEditForm(FlaskForm):
    name = StringField('Edit name')
    about = TextAreaField('Edit information')
    price = IntegerField('Edit price')
    is_private = BooleanField('Is private')
    submit = SubmitField('Save changes')
