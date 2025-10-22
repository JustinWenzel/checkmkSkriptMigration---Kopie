from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import Email, DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username:*", validators=[DataRequired()])
    password = PasswordField("Password:*", validators=[DataRequired()])
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    email = EmailField('Email address:*', validators=[DataRequired(), Email()])
    submit = SubmitField(label="Reset Password")