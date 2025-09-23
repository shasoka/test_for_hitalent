from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Answer, db_helper
from core.schemas import AnswerCreate, AnswerRead

__all__ = ("router",)

from services.answers import create_answer_svc

router = APIRouter()


@router.post(
    settings.api.questions.prefix + "/{id}" + settings.api.answers.prefix,
    response_model=AnswerRead,
)
async def create_answer(
    id: int,
    answer_in: AnswerCreate,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Answer:
    return await create_answer_svc(session, id, answer_in)
