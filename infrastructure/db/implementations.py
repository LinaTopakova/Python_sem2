from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities import User, Prediction
from infrastructure.db.models import UserModel, PredictionModel
from infrastructure.db.repositories import UserRepository, PredictionRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        db_user = UserModel(username=user.username, hashed_password=user.hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return User(
            id=db_user.id,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at,
        )

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        row = result.scalar_one_or_none()
        if row:
            return User(
                id=row.id,
                username=row.username,
                hashed_password=row.hashed_password,
                created_at=row.created_at,
            )
        return None

    async def get_by_id(self, user_id: int) -> User | None:
        row = await self.session.get(UserModel, user_id)
        if row:
            return User(
                id=row.id,
                username=row.username,
                hashed_password=row.hashed_password,
                created_at=row.created_at,
            )
        return None


class PredictionRepositoryImpl(PredictionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, prediction: Prediction) -> Prediction:
        db_pred = PredictionModel(
            user_id=prediction.user_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
            calories=prediction.calories,
            protein=prediction.protein,
            fat=prediction.fat,
            carbs=prediction.carbs,
            confidence=prediction.confidence,
        )
        self.session.add(db_pred)
        await self.session.commit()
        await self.session.refresh(db_pred)
        return Prediction(
            id=db_pred.id,
            user_id=db_pred.user_id,
            input_data=db_pred.input_data,
            prediction=db_pred.prediction,
            calories=db_pred.calories,
            protein=db_pred.protein,
            fat=db_pred.fat,
            carbs=db_pred.carbs,
            confidence=db_pred.confidence,
            created_at=db_pred.created_at,
        )

    async def get_by_user(self, user_id: int) -> list[Prediction]:
        result = await self.session.execute(
            select(PredictionModel).where(PredictionModel.user_id == user_id)
        )
        rows = result.scalars().all()
        return [
            Prediction(
                id=r.id,
                user_id=r.user_id,
                input_data=r.input_data,
                prediction=r.prediction,
                calories=r.calories,
                protein=r.protein,
                fat=r.fat,
                carbs=r.carbs,
                confidence=r.confidence,
                created_at=r.created_at,
            )
            for r in rows
        ]