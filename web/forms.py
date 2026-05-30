from flask_wtf import FlaskForm
from wtforms import FloatField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    gender = SelectField(
        "Пол",
        choices=[("male", "Мужской"), ("female", "Женский")],
        validators=[DataRequired(message="Выберите пол, чтобы мы знали, как к вам обращаться!")],
    )
    height = FloatField(
        "Рост (см)",
        validators=[
            DataRequired(message="Рост обязателен. Вы же не призрак?"),
        ],
    )
    weight = FloatField(
        "Вес (кг)",
        validators=[
            DataRequired(message="Вес обязателен. Даже у гномов есть вес."),
        ],
    )
    submit = SubmitField("Зарегистрироваться")


class ProfileForm(FlaskForm):
    gender = SelectField(
        "Пол",
        choices=[("", "Не указан"), ("male", "Мужской"), ("female", "Женский")],
    )
    height = FloatField("Рост (см)", validators=[Optional()])
    weight = FloatField("Вес (кг)", validators=[Optional()])
    profile_image = StringField("Фото профиля (base64)")
    calories_goal = FloatField("Цель калорий (ккал/день)", validators=[Optional()])
    protein_goal = FloatField("Цель белка (г/день)", validators=[Optional()])
    fat_goal = FloatField("Цель жиров (г/день)", validators=[Optional()])
    carbs_goal = FloatField("Цель углеводов (г/день)", validators=[Optional()])
    submit = SubmitField("Сохранить")