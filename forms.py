from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
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
    submit = SubmitField("Submit")


class BookForm(FlaskForm):
    isbn = StringField("ISBN", validators=[DataRequired(), Regexp("\d{13}|\d{10}"), book_exists])
    submit = SubmitField("Submit")

