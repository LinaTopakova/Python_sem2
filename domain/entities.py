from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int | None
    username: str
    hashed_password: str
    created_at: datetime | None = None


@dataclass
class Prediction:
    id: int | None
    user_id: int
    input_data: str  # base64 строка изображения или путь
    prediction: str  # класс еды
    calories: float
    protein: float
    fat: float
    carbs: float
    created_at: datetime | None = None
