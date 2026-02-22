from uuid import uuid4
from typing import Callable

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.usecases.errors import UserAlreadyExistsError


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, password_hasher: Callable[[str], str]) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def execute(self, *, email: str, password: str) -> User:
        existing = self._user_repository.get_by_email(email)
        if existing:
            raise UserAlreadyExistsError("user already exists")

        user = User(id=str(uuid4()), email=email.lower(), password_hash=self._password_hasher(password))
        return self._user_repository.add(user)
