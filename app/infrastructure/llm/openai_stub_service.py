import asyncio

from app.domain.entities.llm_response import LLMResponse
from app.domain.repositories.llm_service import LLMService


class OpenAIStubService(LLMService):
    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key

    async def generate(self, *, prompt: str, user_id: str) -> LLMResponse:
        await asyncio.sleep(0.3)
        key_state = "configured" if self._api_key else "missing"
        return LLMResponse(
            content=f"[openai_stub:{key_state}] Simulated answer to: {prompt[:120]}",
            provider="openai_stub",
            model="gpt-stub",
        )
