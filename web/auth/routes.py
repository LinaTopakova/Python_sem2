from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from web.app import db, login_manager
from web.forms import LoginForm, RegisterForm
from web.models import User

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    return User.query.get(int(user_id))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Регистрация прошла успешно!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Неверные учётные данные", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
