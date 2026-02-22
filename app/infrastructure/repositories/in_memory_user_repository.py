from threading import Lock

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users_by_id: dict[str, User] = {}
        self._users_by_email: dict[str, User] = {}
        self._lock = Lock()

    def add(self, user: User) -> User:
        with self._lock:
            self._users_by_id[user.id] = user
            self._users_by_email[user.email.lower()] = user
        return user

    def get_by_email(self, email: str) -> User | None:
        return self._users_by_email.get(email.lower())

    def get_by_id(self, user_id: str) -> User | None:
        return self._users_by_id.get(user_id)
