from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class User:
    id: str
    email: str
    password_hash: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
