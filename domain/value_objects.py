from dataclasses import dataclass


@dataclass
class FoodInfo:
    name: str
    calories_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    carbs_per_100g: float
