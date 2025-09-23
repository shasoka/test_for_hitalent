from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question
from core.schemas.question import QuestionCreate
from crud.questions import create_question_in_db, get_questions_from_db

__all__ = ("get_questions_svc",)


async def get_questions_svc(session: AsyncSession) -> list[Question]:
    return await get_questions_from_db(session)


async def create_question_svc(
    session: AsyncSession,
    question_in: QuestionCreate,
) -> Question:
    return await create_question_in_db(session, question_in)
