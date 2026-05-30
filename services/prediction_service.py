from domain.entities import Prediction
from infrastructure.ml.food_model import FoodClassifier
from infrastructure.ml.food_calories import CALORIE_TABLE
from infrastructure.db.repositories import PredictionRepository


class PredictionService:
    def __init__(self, classifier: FoodClassifier, prediction_repo: PredictionRepository) -> None:
        self.classifier = classifier
        self.prediction_repo = prediction_repo

    async def predict(self, user_id: int, image_base64: str) -> Prediction:
        food_name, confidence = self.classifier.predict(image_base64)
        cal, prot, fat, carb = CALORIE_TABLE.get(food_name, (0.0, 0.0, 0.0, 0.0))
        prediction = Prediction(
            id=None,
            user_id=user_id,
            input_data=image_base64,
            prediction=food_name,
            calories=cal,
            protein=prot,
            fat=fat,
            carbs=carb,
        )
        return await self.prediction_repo.create(prediction)
