from app.core.config import Settings
from app.core.security import create_access_token
from app.domain.repositories.token_service import TokenService


class JWTTokenService(TokenService):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create_access_token(self, *, subject: str) -> str:
        return create_access_token(
            subject=subject,
            secret_key=self._settings.secret_key,
            algorithm=self._settings.jwt_algorithm,
            expires_minutes=self._settings.access_token_expire_minutes,
        )
