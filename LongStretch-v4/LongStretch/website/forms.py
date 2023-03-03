from turtle import title
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from .models import User
import email_validator


class RegistrationForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    sport= StringField('Sport')
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6),EqualTo('confirm_password', message='Passwords must match')])
    confirm_password=PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    submit= SubmitField('Sign Up')

    def validate_username(self,username):
        user =User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken. Choose another")

    def validate_email(self,email):
        user =User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already registered. Try logging in")

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    remember = BooleanField('Remember me')
    submit= SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')