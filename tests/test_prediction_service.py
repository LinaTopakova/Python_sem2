import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.entities import Prediction
from services.prediction_service import PredictionService


@pytest.mark.asyncio
async def test_predict() -> None:
    classifier = MagicMock()
    classifier.predict.return_value = ("pizza", 0.95)
    repo = AsyncMock()
    repo.create.return_value = Prediction(
        id=1,
        user_id=1,
        input_data="img",
        prediction="pizza",
        calories=266,
        protein=11,
        fat=10,
        carbs=33,
        confidence=0.95,
    )
    service = PredictionService(classifier, repo)
    pred = await service.predict(1, "base64...")
    assert pred.prediction == "pizza"
    assert pred.calories == 266
    assert pred.confidence == 0.95
