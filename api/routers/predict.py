from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.dependencies import get_prediction_service
from services.prediction_service import PredictionService

router = APIRouter(tags=["predict"])


class PredictRequest(BaseModel):
    image_base64: str
    user_id: int = 1  # временно, пока нет JWT-авторизации


class PredictResponse(BaseModel):
    food_name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    confidence: float


@router.post("/predict", response_model=PredictResponse)
async def predict(  # type: ignore[misc]
    request: PredictRequest,
    service: PredictionService = Depends(get_prediction_service),
) -> PredictResponse:
    pred = await service.predict(request.user_id, request.image_base64)
    return PredictResponse(
        food_name=pred.prediction,
        calories=pred.calories,
        protein=pred.protein,
        fat=pred.fat,
        carbs=pred.carbs,
        confidence=pred.confidence,
    )