from flask import render_template, url_for, flash, redirect, Blueprint
from flask_login import login_user, login_required, logout_user
from app.auth.forms import LoginForm, ResetPasswordForm
from app.models.user import User
from . import auth_bp

@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data.strip()):
            login_user(user)
            return redirect(url_for("auth.menu_page"))
        flash("Invalid username or password. In case of problems reach to JustinSven.Wenzel@gls-germany.com.", "danger")
    return render_template("forms/login.html", form=form)  # app/auth/templates/forms/login.html


@auth_bp.route("/resetpassword", methods=["GET", "POST"])
def reset_password_page():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email.data.strip()).first()
        if attempted_user and attempted_user.check_email(form.email.data.strip()):
            if attempted_user.reset_password():
                flash("Password reset successful! Check your email for the new password.", "success")
            else:
                flash("Failed to send reset email. Please try again or contact JustinSven.Wenzel@gls-germany.com.", "danger")
        else:
            flash("Email address not found in the system.", "danger")
        return redirect(url_for("auth.reset_password_page"))
    return render_template("forms/reset_password.html", form=form)  # app/auth/templates/reset_password.html


@auth_bp.route("/menu")
@login_required
def menu_page():
    return render_template("menu.html")  # app/templates/menu.html (global)

@auth_bp.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for("auth.login_page"))

