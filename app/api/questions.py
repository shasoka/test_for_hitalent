from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Question
from core.schemas import QuestionRead
from core.schemas.question import QuestionCreate, QuestionWithAnswersRead

from services.questions import (
    create_question_svc,
    get_question_with_answers_svc,
    get_questions_svc,
)

__all__ = ("router",)

router = APIRouter()


@router.get("/", response_model=list[QuestionRead])
async def get_questions(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[Question]:
    return await get_questions_svc(session)


@router.get("/{id}", response_model=QuestionWithAnswersRead)
async def get_question_with_answers(
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await get_question_with_answers_svc(id, session)


@router.post("/", response_model=QuestionRead)
async def create_question(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    question_in: QuestionCreate,
) -> Question:
    return await create_question_svc(session, question_in)
