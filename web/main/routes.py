import base64
from datetime import date, timedelta

import requests
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from web.app import db
from web.models import DiaryEntry, Prediction, WeightEntry

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

        # Сохраняем результат распознавания
        pred = Prediction(
            user_id=current_user.id,
            input_data=img_base64,
            prediction=data["food_name"],
            calories=data["calories"],
            protein=data["protein"],
            fat=data["fat"],
            carbs=data["carbs"],
            confidence=data.get("confidence", 0.0),
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
    image_data = request.form.get("image_data", "")

    if not food_name:
        flash("Нет данных для добавления", "danger")
        return redirect(url_for("main.predict"))

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
    date_str = request.args.get("date")
    if date_str:
        try:
            viewing_date = date.fromisoformat(date_str)
        except ValueError:
            viewing_date = date.today()
    else:
        viewing_date = date.today()

    entries = (
        DiaryEntry.query.filter_by(user_id=current_user.id, date=viewing_date)
        .order_by(DiaryEntry.created_at.desc())
        .all()
    )

    total_cal = sum(e.calories for e in entries)
    total_protein = sum(e.protein for e in entries)
    total_fat = sum(e.fat for e in entries)
    total_carbs = sum(e.carbs for e in entries)

    # Данные для графиков за последние 7 дней
    days = []
    calories_per_day = []
    weight_per_day = []
    for i in range(6, -1, -1):
        d = date.today() - timedelta(days=i)
        days.append(d.strftime("%d.%m"))
        day_cal = (
            db.session.query(func.sum(DiaryEntry.calories))
            .filter(DiaryEntry.user_id == current_user.id, DiaryEntry.date == d)
            .scalar()
        ) or 0
        calories_per_day.append(day_cal)
        last_weight = (
            WeightEntry.query.filter_by(user_id=current_user.id, date=d)
            .order_by(WeightEntry.created_at.desc())
            .first()
        )
        weight_per_day.append(last_weight.weight if last_weight else None)

    return render_template(
        "diary.html",
        entries=entries,
        total_cal=total_cal,
        total_protein=total_protein,
        total_fat=total_fat,
        total_carbs=total_carbs,
        viewing_date=viewing_date,
        today=date.today(),
        timedelta=timedelta,
        days=days,
        calories_per_day=calories_per_day,
        weight_per_day=weight_per_day,
        goals={
            "calories": current_user.calories_goal,
            "protein": current_user.protein_goal,
            "fat": current_user.fat_goal,
            "carbs": current_user.carbs_goal,
        },
    )


@main_bp.route("/add-weight", methods=["POST"])
@login_required
def add_weight():
    weight_str = request.form.get("weight", "")
    try:
        weight = float(weight_str)
    except (ValueError, TypeError):
        flash("Вес должен быть числом, а не стихотворением!", "danger")
        return redirect(url_for("main.diary"))

    if weight < 20 or weight > 500:
        flash("Вес от 20 до 500 кг. Даже у слона бывают сомнения!", "warning")
        return redirect(url_for("main.diary"))

    entry = WeightEntry(user_id=current_user.id, weight=weight)
    db.session.add(entry)
    db.session.commit()
    flash(f"Вес {weight} кг записан. Ступенька весов скрипнула, но выдержала.", "success")
    return redirect(url_for("main.diary"))

@main_bp.route("/delete-entry/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    if entry.user_id != current_user.id:
        flash("Чужая еда — не ваша забота!", "danger")
        return redirect(url_for("main.diary"))
    db.session.delete(entry)
    db.session.commit()
    flash("Запись удалена. Калории испарились, но совесть осталась.", "success")
    return redirect(url_for("main.diary"))

@main_bp.route("/history")
@login_required
def history():
    preds = (
        Prediction.query.filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return render_template("history.html", predictions=preds)