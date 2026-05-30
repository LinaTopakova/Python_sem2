import base64
from datetime import date

import requests
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from web.app import db
from web.models import DiaryEntry, Prediction

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    result = None
    img_base64 = None
    if request.method == "POST":
        file = request.files.get("image")
        if not file:
            flash("Выберите изображение", "danger")
            return render_template("predict.html")

        img_bytes = file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        ml_api_url = current_app.config["ML_API_URL"] + "/api/v1/predict"
        try:
            resp = requests.post(
                ml_api_url,
                json={"image_base64": img_base64, "user_id": current_user.id},
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            result = data
        except Exception as e:
            flash(f"Ошибка ML API: {e}", "danger")
            return render_template("predict.html")

        # Сохраняем результат распознавания в историю
        pred = Prediction(
            user_id=current_user.id,
            input_data=img_base64,
            prediction=data["food_name"],
            calories=data["calories"],
            protein=data["protein"],
            fat=data["fat"],
            carbs=data["carbs"],
        )
        db.session.add(pred)
        db.session.commit()
        flash("Предсказание сохранено! Вы можете добавить блюдо в дневник.", "success")

    return render_template("predict.html", result=result, img_base64=img_base64)


@main_bp.route("/add-to-diary", methods=["POST"])
@login_required
def add_to_diary():
    food_name = request.form.get("food_name")
    calories_100 = float(request.form.get("calories", 0))
    protein_100 = float(request.form.get("protein", 0))
    fat_100 = float(request.form.get("fat", 0))
    carbs_100 = float(request.form.get("carbs", 0))
    weight = float(request.form.get("weight", 100))
    image_data = request.form.get("image_data", "")  # base64

    if not food_name:
        flash("Нет данных для добавления", "danger")
        return redirect(url_for("main.predict"))

    # Пересчёт на фактический вес
    factor = weight / 100.0
    entry = DiaryEntry(
        user_id=current_user.id,
        food_name=food_name,
        calories=round(calories_100 * factor, 1),
        protein=round(protein_100 * factor, 1),
        fat=round(fat_100 * factor, 1),
        carbs=round(carbs_100 * factor, 1),
        weight=weight,
        image_data=image_data,
    )
    db.session.add(entry)
    db.session.commit()
    flash(f"{food_name} ({weight} г) добавлено в дневник!", "success")
    return redirect(url_for("main.diary"))


@main_bp.route("/diary")
@login_required
def diary():
    today = date.today()
    entries_today = (
        DiaryEntry.query
        .filter_by(user_id=current_user.id, date=today)
        .order_by(DiaryEntry.created_at.desc())
        .all()
    )
    total_calories = sum(e.calories for e in entries_today)

    # Получим также историю за предыдущие дни (сгруппированную по дате)
    past_days = (
        db.session.query(DiaryEntry.date, func.sum(DiaryEntry.calories).label("total"))
        .filter(DiaryEntry.user_id == current_user.id, DiaryEntry.date < today)
        .group_by(DiaryEntry.date)
        .order_by(DiaryEntry.date.desc())
        .all()
    )

    return render_template(
        "diary.html",
        entries=entries_today,
        total_calories=total_calories,
        past_days=past_days,
    )


@main_bp.route("/history")
@login_required
def history():
    preds = (
        Prediction.query.filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return render_template("history.html", predictions=preds)