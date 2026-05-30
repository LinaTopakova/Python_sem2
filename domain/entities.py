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
    input_data: str  # base64
    prediction: str  # food class
    calories: float
    protein: float
    fat: float
    carbs: float
    confidence: float = 0.0
    created_at: datetime | None = None


@dataclass
class FoodInfo:
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
