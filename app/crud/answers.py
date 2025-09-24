"""Модуль, содержащий CRUD-операции сущности Answer."""

from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Answer
from app.core.schemas import AnswerCreate
from app.crud.questions import get_question_by_id

__all__ = ("create_answer_in_db", "get_answer_by_id")


async def get_answer_by_id(
    session: AsyncSession,
    answer_id: int,
) -> Answer | None:
    """
    Функция получения ответа по его id.

    :param session: сессия подключения к БД;
    :param answer_id: идентификатор ответа;
    :return: объект Answer.
    """

    query_result: QueryResult = await session.execute(
        select(Answer).where(Answer.id == answer_id)
    )
    return query_result.scalar_one_or_none()


async def create_answer_in_db(
    session: AsyncSession,
    question_id: int,
    answer_in: AnswerCreate,
) -> Answer:
    """
    Функция создания записи в таблице answers по идентификатору вопроса.

    :param session: сессия подключения к БД;
    :param question_id: идентификатор вопроса, к которому добавляется ответ;
    :param answer_in: объект типа AnswerCreate, полученный из тела запроса;
    :return: созданный объект Answer.
    """

    answer = Answer(**answer_in.dict())
    answer.question_id = question_id
    session.add(answer)
    await session.commit()
    return answer


async def delete_answer_in_db(
    session: AsyncSession,
    answer_to_delete: Answer,
) -> Answer:
    """
    Функция удаления записи из таблицы answers по соответствующему объекту
    Answer.

    :param session: сессия подключения к БД;
    :param answer_to_delete: идентификатор ответа;
    :return: удаленный объект Answer.
    """

    await session.delete(answer_to_delete)
    await session.commit()
    return answer_to_delete
