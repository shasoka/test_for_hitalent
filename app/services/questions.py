from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Question
from app.core.schemas import QuestionCreate
from app.crud.questions import (
    create_question_in_db,
    delete_question_in_db,
    get_question_with_answers_from_db,
    get_questions_from_db,
)

__all__ = (
    "get_questions_svc",
    "get_question_with_answers_svc",
    "create_question_svc",
    "delete_question_svc",
)


async def get_questions_svc(session: AsyncSession) -> list[Question]:
    return await get_questions_from_db(session=session)


async def get_question_with_answers_svc(
    id: int,
    session: AsyncSession,
) -> Question:
    return await get_question_with_answers_from_db(
        session=session,
        question_id=id,
    )


async def create_question_svc(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    return await create_question_in_db(
        session=session,
        question_in=question_in,
    )


async def delete_question_svc(
    session: AsyncSession,
    id: int,
) -> Question:
    return await delete_question_in_db(
        session=session,
        question_id=id,
    )
