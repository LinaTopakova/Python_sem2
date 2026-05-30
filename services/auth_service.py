from domain.entities import User
from infrastructure.db.repositories import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def register(self, username: str, password: str) -> User:
        hashed = pwd_context.hash(password)
        user = User(id=None, username=username, hashed_password=hashed)
        return await self.user_repo.create(user)

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self.user_repo.get_by_username(username)
        if user and pwd_context.verify(password, user.hashed_password):
            return user
        return None
