from app.domain.repositories.llm_service import LLMService


class GenerateAIResponseUseCase:
    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def execute(self, *, prompt: str, user_id: str) -> dict:
        result = await self._llm_service.generate(prompt=prompt, user_id=user_id)
        return {
            "response": result.content,
            "provider": result.provider,
            "model": result.model,
        }
