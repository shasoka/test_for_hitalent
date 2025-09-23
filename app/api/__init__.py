from fastapi import APIRouter

from core.config import settings
from .questions import router as questions_router

__all__ = ("router",)

router = APIRouter(prefix=settings.api.prefix)

router.include_router(
    questions_router,
    prefix=settings.api.questions.prefix,
    tags=settings.api.questions.tags,
)
