from dataclasses import dataclass


@dataclass(slots=True)
class LLMResponse:
    content: str
    provider: str
    model: str
