"""Пакет, содержащий API-роутеры."""

from fastapi import APIRouter

from app.core.config import settings
from app.api.questions import router as questions_router
from app.api.answers import router as answers_router

__all__ = ("router",)

router = APIRouter(prefix=settings.api.prefix)

router.include_router(
    questions_router,
    prefix=settings.api.questions.prefix,
    tags=settings.api.questions.tags,
)

router.include_router(
    answers_router,
    # Опущен префикс из-за POST /questions/{id}/answers/
    tags=settings.api.answers.tags,
)
