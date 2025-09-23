from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Answer
from core.schemas import AnswerCreate
from crud.questions import check_if_question_exists

__all__ = ("create_answer_in_db",)


async def create_answer_in_db(
    session: AsyncSession,
    question_id: int,
    answer_in: AnswerCreate,
) -> Answer:
    await check_if_question_exists(session, question_id)

    answer = Answer(**answer_in.dict())
    answer.question_id = question_id
    session.add(answer)
    await session.commit()
    return answer
