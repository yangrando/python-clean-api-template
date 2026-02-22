from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, *, subject: str) -> str:
        raise NotImplementedError
