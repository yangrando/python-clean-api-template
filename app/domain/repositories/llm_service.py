from abc import ABC, abstractmethod

from app.domain.entities.llm_response import LLMResponse


class LLMService(ABC):
    @abstractmethod
    async def generate(self, *, prompt: str, user_id: str) -> LLMResponse:
        raise NotImplementedError
