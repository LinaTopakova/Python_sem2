from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from web.app import db, login_manager
from web.forms import LoginForm, ProfileForm, RegisterForm
from web.models import User

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    return User.query.get(int(user_id))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Проверка, существует ли уже пользователь с таким логином
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash(
                "Пользователь с таким логином уже существует. Придумайте что-нибудь пооригинальнее!",
                "danger",
            )
            return render_template("register.html", form=form)

        height = form.height.data
        weight = form.weight.data

        if height < 50 or height > 250:
            flash(
                "С таким ростом вас не пустят даже в лилипутский цирк! Укажите от 50 до 250 см.",
                "warning",
            )
            return render_template("register.html", form=form)
        if weight < 20 or weight > 500:
            flash(
                "Вы весите как пёрышко или как слон? Введите вес от 20 до 500 кг.",
                "warning",
            )
            return render_template("register.html", form=form)

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password_hash=hashed_pw,
            gender=form.gender.data,
            height=height,
            weight=weight,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Регистрация прошла успешно! Теперь войдите.", "success")
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


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        height = form.height.data
        weight = form.weight.data
        cal_goal = form.calories_goal.data
        prot_goal = form.protein_goal.data
        fat_goal = form.fat_goal.data
        carb_goal = form.carbs_goal.data

        if height and (height < 50 or height > 250):
            flash(
                "Рост от 50 до 250 см, пожалуйста. Вы же не дюймовочка и не Гулливер?",
                "warning",
            )
            return render_template("profile.html", form=form)
        if weight and (weight < 20 or weight > 500):
            flash(
                "Вес от 20 до 500 кг. Если вы воздушный шарик или кит, выберите другое значение.",
                "warning",
            )
            return render_template("profile.html", form=form)
        if cal_goal and (cal_goal < 500 or cal_goal > 10000):
            flash(
                "Калории: 500–10000 ккал. Вы не ядерный реактор и не фотосинтезируете!",
                "warning",
            )
            return render_template("profile.html", form=form)
        if prot_goal and (prot_goal < 0 or prot_goal > 500):
            flash(
                "Белки: 0–500 г. Пожалейте почки, они вам ещё пригодятся.",
                "warning",
            )
            return render_template("profile.html", form=form)
        if fat_goal and (fat_goal < 0 or fat_goal > 500):
            flash(
                "Жиры: 0–500 г. Не надо купаться в оливковом масле.",
                "warning",
            )
            return render_template("profile.html", form=form)
        if carb_goal and (carb_goal < 0 or carb_goal > 1000):
            flash(
                "Углеводы: 0–1000 г. Макароны — это вкусно, но знайте меру.",
                "warning",
            )
            return render_template("profile.html", form=form)

        # Сохраняем профиль
        current_user.gender = form.gender.data
        current_user.height = height or 0
        current_user.weight = weight or 0
        current_user.calories_goal = cal_goal or 2000
        current_user.protein_goal = prot_goal or 75
        current_user.fat_goal = fat_goal or 65
        current_user.carbs_goal = carb_goal or 300
        db.session.commit()
        flash(
            "Профиль обновлён. Теперь вы киборг с идеальными настройками!",
            "success",
        )
        return redirect(url_for("auth.profile"))
    return render_template("profile.html", form=form)
