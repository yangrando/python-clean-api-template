from typing import Callable

from app.domain.entities.user import User
from app.domain.repositories.token_service import TokenService
from app.domain.repositories.user_repository import UserRepository
from app.usecases.errors import InvalidCredentialsError


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_verifier: Callable[[str, str], bool],
        token_service: TokenService,
    ) -> None:
        self._user_repository = user_repository
        self._password_verifier = password_verifier
        self._token_service = token_service

    def execute(self, *, email: str, password: str) -> tuple[str, User]:
        user = self._user_repository.get_by_email(email.lower())
        if user is None or not self._password_verifier(password, user.password_hash):
            raise InvalidCredentialsError("invalid credentials")
        access_token = self._token_service.create_access_token(subject=user.id)
        return access_token, user
