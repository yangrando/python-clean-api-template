import asyncio

from app.domain.entities.llm_response import LLMResponse
from app.domain.repositories.llm_service import LLMService


class FakeLLMService(LLMService):
    async def generate(self, *, prompt: str, user_id: str) -> LLMResponse:
        await asyncio.sleep(0.2)
        return LLMResponse(
            content=f"Simulated response for user {user_id}: {prompt[:120]}",
            provider="fake",
            model="fake-llm-v1",
        )
