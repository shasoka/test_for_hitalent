"""Модуль, описывающий эндпоинты, связанные с сущностью Question."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, Question
from app.core.schemas import QuestionRead
from app.core.schemas import QuestionCreate, QuestionWithAnswersRead

from app.services.questions import (
    create_question_svc,
    delete_question_svc,
    get_question_with_answers_svc,
    get_questions_svc,
)

__all__ = ("router",)

router = APIRouter()


@router.get("/", response_model=list[QuestionRead])
async def get_questions(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[Question]:
    return await get_questions_svc(session=session)


@router.get("/{id}", response_model=QuestionWithAnswersRead)
async def get_question_with_answers(
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Question:
    return await get_question_with_answers_svc(
        session=session,
        question_id=id,
    )


@router.post("/", response_model=QuestionRead)
async def create_question(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    question_in: QuestionCreate,
) -> Question:
    return await create_question_svc(
        session=session,
        question_in=question_in,
    )


@router.delete("/{id}", response_model=QuestionRead)
async def delete_question(
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Question:
    return await delete_question_svc(
        session=session,
        question_id=id,
    )
