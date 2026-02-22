from fastapi import FastAPI

from app.api.routes.ai import router as ai_router
from app.api.routes.auth import router as auth_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

if settings.environment == "production" and len(settings.secret_key) < 32:
    raise RuntimeError("SECRET_KEY must have at least 32 characters in production.")

app = FastAPI(title=settings.app_name)
app.include_router(auth_router)
app.include_router(ai_router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
