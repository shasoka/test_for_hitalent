from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NoEntityFoundException
from core.models import Answer
from core.schemas import AnswerCreate
from crud.questions import get_question_by_id_or_404

__all__ = ("create_answer_in_db",)


async def get_answer_by_id_or_404(
    session: AsyncSession,
    answer_id: int,
) -> Answer:
    query_result: QueryResult = await session.execute(
        select(Answer).where(Answer.id == answer_id)
    )
    answer: Answer | None = query_result.scalar_one_or_none()
    if answer is None:
        raise NoEntityFoundException(f"Ответ с id={answer_id} не найден в БД")
    return answer


async def create_answer_in_db(
    session: AsyncSession,
    question_id: int,
    answer_in: AnswerCreate,
) -> Answer:
    await get_question_by_id_or_404(session, question_id)

    answer = Answer(**answer_in.dict())
    answer.question_id = question_id
    session.add(answer)
    await session.commit()
    return answer
