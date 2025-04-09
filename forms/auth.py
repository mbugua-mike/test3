from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models.user import User
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10, message='Phone number must be exactly 10 digits.')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already registered. Please use a different one.')

    def validate_password(self, password):
        pw = password.data
        errors = []
        if len(pw) < 8:
            errors.append("Password must be at least 8 characters long.")
        if not re.search("[a-z]", pw):
            errors.append("Password must contain at least one lowercase letter.")
        if not re.search("[A-Z]", pw):
            errors.append("Password must contain at least one uppercase letter.")
        if not re.search("[0-9]", pw):
            errors.append("Password must contain at least one digit.")
        if not re.search("[!@#$%^&*(),.?\":{}|<>_-]", pw):
            errors.append("Password must contain at least one special character (e.g., !@#$).")
            
        if errors:
            raise ValidationError(" - ".join(errors))

    def validate_phone_number(self, phone_number):
        if not phone_number.data.isdigit():
            raise ValidationError('Phone number must contain only digits.') 