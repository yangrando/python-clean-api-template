import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_llm_service, get_user_repository
from app.infrastructure.llm.fake_llm_service import FakeLLMService
from app.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from main import app


@pytest.fixture
def client() -> TestClient:
    repository = InMemoryUserRepository()

    def override_repo() -> InMemoryUserRepository:
        return repository

    def override_llm() -> FakeLLMService:
        return FakeLLMService()

    app.dependency_overrides[get_user_repository] = override_repo
    app.dependency_overrides[get_llm_service] = override_llm
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
