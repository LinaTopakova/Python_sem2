from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import User, Prediction


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError


class PredictionRepository(ABC):
    @abstractmethod
    async def create(self, prediction: Prediction) -> Prediction:
        raise NotImplementedError

    @abstractmethod
    async def get_by_user(self, user_id: int) -> list[Prediction]:
        raise NotImplementedError
