from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField("Username:*", validators=[DataRequired()])
    password = PasswordField("Password:*", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username:*", validators=[DataRequired(), Length(min=3, max=30, message="Username must be between 3 and 30 characters")])
    email_address = EmailField("Email address:*", validators=[DataRequired(), Email(message="Please enter a valid email address")])
    password = PasswordField("Password:*", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long")])
    confirm_password = PasswordField("Confirm Password:*", validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError("Username already exists. Please choose a different one.")

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data.strip()).first()
        if user:
            raise ValidationError("Email address already registered. Please use a different one.")


class ResetPasswordForm(FlaskForm):
    email = EmailField('Email address:*', validators=[DataRequired(), Email()])
    submit = SubmitField(label="Reset Password")