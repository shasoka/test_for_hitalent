from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import Answer, db_helper
from core.schemas import AnswerCreate, AnswerRead
from services.answers import (
    create_answer_svc,
    delete_answer_svc,
    get_answer_by_id_svc,
)

__all__ = ("router",)


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


@router.get(settings.api.answers.prefix + "/{id}", response_model=AnswerRead)
async def get_answer_by_id(
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Answer:
    return await get_answer_by_id_svc(id, session)


@router.delete(
    settings.api.answers.prefix + "/{id}",
    response_model=AnswerRead,
)
async def delete_answer(
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Answer:
    return await delete_answer_svc(id, session)
