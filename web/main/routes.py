import base64
import requests
from flask import Blueprint, current_app, flash, render_template, request
from flask_login import current_user, login_required

from web.app import db
from web.models import Prediction

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    result = None
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
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            result = data
        except Exception as e:
            flash(f"Ошибка ML API: {e}", "danger")
            return render_template("predict.html")

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
        flash("Предсказание сохранено!", "success")

    return render_template("predict.html", result=result)


@main_bp.route("/history")
@login_required
def history():
    preds = (
        Prediction.query.filter_by(user_id=current_user.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
    return render_template("history.html", predictions=preds)
