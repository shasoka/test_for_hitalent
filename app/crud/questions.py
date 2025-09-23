from typing import Coroutine, Sequence

from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question

__all__ = ("get_questions_from_db", "create_question_in_db")

from core.schemas.question import QuestionCreate


async def get_questions_from_db(session: AsyncSession) -> list[Question]:
    query_result: QueryResult = await session.execute(select(Question))
    questions: Sequence[Question] = query_result.scalars().all()
    return list(questions)


async def create_question_in_db(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    question = Question(**question_in.dict())
    session.add(question)
    await session.commit()
    return question
