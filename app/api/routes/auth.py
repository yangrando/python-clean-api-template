from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.api.dependencies import get_current_user, get_login_user_usecase, get_register_user_usecase
from app.core.logging import logger
from app.domain.entities.user import User
from app.usecases.errors import InvalidCredentialsError, UserAlreadyExistsError
from app.usecases.login_user import LoginUserUseCase
from app.usecases.register_user import RegisterUserUseCase

router = APIRouter(tags=["auth"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    is_active: bool
    created_at: datetime


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: RegisterRequest,
    usecase: RegisterUserUseCase = Depends(get_register_user_usecase),
) -> User:
    logger.info("auth.register.attempt", extra={"email": payload.email})
    try:
        user = usecase.execute(email=payload.email, password=payload.password)
    except UserAlreadyExistsError as exc:
        logger.warning("auth.register.conflict", extra={"email": payload.email})
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    logger.info("auth.register.success", extra={"email": payload.email, "user_id": user.id})
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    usecase: LoginUserUseCase = Depends(get_login_user_usecase),
) -> TokenResponse:
    logger.info("auth.login.attempt", extra={"email": payload.email})
    try:
        token, user = usecase.execute(email=payload.email, password=payload.password)
    except InvalidCredentialsError as exc:
        logger.warning("auth.login.failure", extra={"email": payload.email})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    logger.info("auth.login.success", extra={"email": payload.email, "user_id": user.id})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
