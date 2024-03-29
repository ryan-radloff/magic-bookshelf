from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError, EqualTo
import requests

def book_exists(form, field):
    if(requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:" + field.data).json()["totalItems"] == 0):
        raise ValidationError("ISBN not found. Try alternate format?")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Submit")

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Submit")


class BookForm(FlaskForm):
    isbn = StringField("ISBN", validators=[DataRequired(), Regexp("\d{13}|\d{10}"), book_exists])
    streetNameNum = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired(), Regexp("\w{2}")])
    zipcode = StringField("Zip", validators=[DataRequired(), Regexp("\d{5}")])
    submit = SubmitField("Submit")

class RequestForm(FlaskForm):
    streetNameNum = StringField("Street", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired(), Regexp("\w{2}")])
    zipcode = StringField("Zip", validators=[DataRequired(), Regexp("\d{5}")])
    submit = SubmitField("Submit")
