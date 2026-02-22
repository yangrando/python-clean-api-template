from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user, get_generate_ai_response_usecase
from app.core.logging import logger
from app.domain.entities.user import User
from app.usecases.generate_ai_response import GenerateAIResponseUseCase

router = APIRouter(tags=["ai"])


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)


class GenerateResponse(BaseModel):
    prompt: str
    response: str
    provider: str
    model: str
    latency_ms: int


@router.post("/generate", response_model=GenerateResponse)
async def generate(
    payload: GenerateRequest,
    current_user: User = Depends(get_current_user),
    usecase: GenerateAIResponseUseCase = Depends(get_generate_ai_response_usecase),
) -> GenerateResponse:
    started = datetime.now(UTC)
    logger.info(
        "llm.generate.request",
        extra={"user_id": current_user.id, "prompt_size": len(payload.prompt)},
    )
    result = await usecase.execute(prompt=payload.prompt, user_id=current_user.id)
    latency_ms = int((datetime.now(UTC) - started).total_seconds() * 1000)

    logger.info(
        "llm.generate.success",
        extra={"user_id": current_user.id, "provider": result["provider"], "latency_ms": latency_ms},
    )

    return GenerateResponse(prompt=payload.prompt, latency_ms=latency_ms, **result)
