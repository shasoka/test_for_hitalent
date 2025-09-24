from typing import Sequence

from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NoEntityFoundException
from app.core.models import Question
from app.core.schemas import QuestionCreate

__all__ = (
    "create_question_in_db",
    "delete_question_in_db",
    "get_questions_from_db",
    "get_question_with_answers_from_db",
    "get_question_by_id_or_404",
)


async def get_question_by_id_or_404(
    session: AsyncSession,
    question_id: int,
) -> Question:
    query_result: QueryResult = await session.execute(
        select(Question).where(Question.id == question_id)
    )
    question: Question | None = query_result.scalar_one_or_none()
    if question is None:
        raise NoEntityFoundException(f"Вопрос с id={question_id} не найден в БД")
    return question


async def get_questions_from_db(session: AsyncSession) -> list[Question]:
    query_result: QueryResult = await session.execute(select(Question))
    questions: Sequence[Question] = query_result.scalars().all()
    return list(questions)


async def get_question_with_answers_from_db(
    question_id: int,
    session: AsyncSession,
) -> Question:
    query_result: QueryResult = await session.execute(
        select(Question)
        .where(Question.id == question_id)
        .options(selectinload(Question.answers))
    )
    question: Question = query_result.scalar_one_or_none()
    if question is None:
        raise NoEntityFoundException(f"Вопрос с id={question_id} не найден в БД")
    return question


async def create_question_in_db(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    question = Question(**question_in.dict())
    session.add(question)
    await session.commit()
    return question


async def delete_question_in_db(
    session: AsyncSession,
    question_id: int,
) -> Question:
    question_to_delete: Question = await get_question_by_id_or_404(
        session=session,
        question_id=question_id,
    )

    await session.delete(question_to_delete)
    await session.commit()
    return question_to_delete
