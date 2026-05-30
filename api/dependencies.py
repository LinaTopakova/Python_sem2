from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.database import get_async_session
from infrastructure.db.implementations import UserRepositoryImpl, PredictionRepositoryImpl
from infrastructure.ml.food_model import FoodClassifier
from services.auth_service import AuthService
from services.prediction_service import PredictionService


async def get_user_repo(session: AsyncSession = Depends(get_async_session)) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


async def get_prediction_repo(
    session: AsyncSession = Depends(get_async_session),
) -> PredictionRepositoryImpl:
    return PredictionRepositoryImpl(session)


def get_classifier() -> FoodClassifier:
    return FoodClassifier()


async def get_auth_service(
    user_repo: UserRepositoryImpl = Depends(get_user_repo),
) -> AuthService:
    return AuthService(user_repo)


async def get_prediction_service(
    classifier: FoodClassifier = Depends(get_classifier),
    pred_repo: PredictionRepositoryImpl = Depends(get_prediction_repo),
) -> PredictionService:
    return PredictionService(classifier, pred_repo)
