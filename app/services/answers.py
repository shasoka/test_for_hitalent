"""Модуль, содержащий бизнес-логику, связанную с сущностью Answer."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NoEntityFoundException
from app.core.models import Answer
from app.core.schemas import AnswerCreate
from app.crud.answers import (
    create_answer_in_db,
    delete_answer_in_db,
    get_answer_by_id,
)
from app.crud.questions import get_question_by_id

__all__ = ("create_answer_svc", "get_answer_by_id_svc")


async def create_answer_svc(
    session: AsyncSession,
    question_id: int,
    answer_in: AnswerCreate,
) -> Answer:
    """
    Функция, позволяющая создать ответ на вопрос по его идентификатору.
    В случае, если такого вопроса не существует, выбрасывается исключение
    NoEntityFoundException.

    :param session: сессия подключения к БД;
    :param question_id: ижентификатор вопроса;
    :param answer_in: объект типа AnswerCreate, полученный из тела запроса;
    :return: созданный объект типа Answer.
    """

    if await get_question_by_id(session=session, question_id=question_id):
        return await create_answer_in_db(
            session=session,
            question_id=question_id,
            answer_in=answer_in,
        )
    raise NoEntityFoundException(f"Вопрос с id={question_id} не найден в БД")


async def get_answer_by_id_svc(
    answer_id: int,
    session: AsyncSession,
) -> Answer:
    """
    Функция, позволяющая получить ответ по его идентификатору.
    В случае, если ответ не найден, выбрасывается исключение
    NoEntityFoundException.

    :param answer_id: идентификатор ответа;
    :param session: сессия подключения к БД;
    :return: найденный объект типа Answer.
    """

    if answer := (
        await get_answer_by_id(
            session=session,
            answer_id=answer_id,
        )
    ):
        return answer
    raise NoEntityFoundException(f"Ответ с id={id} не найден в БД")


async def delete_answer_svc(
    answer_id: int,
    session: AsyncSession,
) -> Answer:
    """
    Функция, позволяющая удалить ответ по его идентификатору.
    В случае, если такой ответ не найден, выбрасывается исключение
    NoEntityFoundException.

    :param answer_id: идентификатор ответа;
    :param session: сессия подключения к БД;
    :return: удаленный ответ.
    """

    if answer_to_delete := (
        await get_answer_by_id(
            session=session,
            answer_id=answer_id,
        )
    ):
        return await delete_answer_in_db(
            session=session,
            answer_to_delete=answer_to_delete,
        )
    raise NoEntityFoundException(f"Ответ с id={answer_id} не найден в БД")
