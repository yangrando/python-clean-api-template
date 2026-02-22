from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import Settings, get_settings
from app.core.security import TokenError, decode_access_token, hash_password, verify_password
from app.domain.entities.user import User
from app.domain.repositories.llm_service import LLMService
from app.domain.repositories.token_service import TokenService
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.memory import user_repository
from app.infrastructure.llm.fake_llm_service import FakeLLMService
from app.infrastructure.llm.openai_stub_service import OpenAIStubService
from app.infrastructure.security.jwt_token_service import JWTTokenService
from app.usecases.generate_ai_response import GenerateAIResponseUseCase
from app.usecases.login_user import LoginUserUseCase
from app.usecases.register_user import RegisterUserUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_user_repository() -> UserRepository:
    return user_repository


def get_llm_service(settings: Settings = Depends(get_settings)) -> LLMService:
    if settings.llm_provider == "openai_stub":
        return OpenAIStubService(api_key=settings.openai_api_key)
    return FakeLLMService()


def get_register_user_usecase(
    repository: UserRepository = Depends(get_user_repository),
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repository=repository, password_hasher=hash_password)


def get_token_service(settings: Settings = Depends(get_settings)) -> TokenService:
    return JWTTokenService(settings=settings)


def get_login_user_usecase(
    repository: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service),
) -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repository=repository,
        password_verifier=verify_password,
        token_service=token_service,
    )


def get_generate_ai_response_usecase(
    llm_service: LLMService = Depends(get_llm_service),
) -> GenerateAIResponseUseCase:
    return GenerateAIResponseUseCase(llm_service=llm_service)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(get_user_repository),
    settings: Settings = Depends(get_settings),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token=token, secret_key=settings.secret_key, algorithm=settings.jwt_algorithm)
    except TokenError as exc:
        raise credentials_exc from exc

    subject = payload.get("sub")
    if not isinstance(subject, str):
        raise credentials_exc

    user = repository.get_by_id(subject)
    if user is None:
        raise credentials_exc

    return user
