from datetime import date, datetime

from flask_login import UserMixin
from web.app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    gender = db.Column(db.String(10), default="")
    height = db.Column(db.Float, default=0.0)
    weight = db.Column(db.Float, default=0.0)
    profile_image = db.Column(db.Text, default="")
    calories_goal = db.Column(db.Float, default=2000)
    protein_goal = db.Column(db.Float, default=75)
    fat_goal = db.Column(db.Float, default=65)
    carbs_goal = db.Column(db.Float, default=300)
    created_at = db.Column(db.DateTime, default=datetime.now)

    predictions = db.relationship("Prediction", backref="user", lazy=True)
    diary_entries = db.relationship("DiaryEntry", backref="user", lazy=True)
    weight_entries = db.relationship("WeightEntry", backref="user", lazy=True)


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)


class DiaryEntry(db.Model):
    __tablename__ = "diary_entry"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    food_name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, default=100.0)
    image_data = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.now)


class WeightEntry(db.Model):
    __tablename__ = "weight_entry"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.now)
