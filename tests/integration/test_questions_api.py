import uuid

import pytest
from httpx import ASGITransport, AsyncClient, Response
from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.main import app
from app.core.models import Answer, Question


@pytest.mark.asyncio
class TestQuestionsAPI:

    @staticmethod
    async def _take_answers_snaphost(
        db_session: AsyncSession,
    ) -> list[Answer]:
        query_result: QueryResult = await db_session.execute(select(Answer))
        return list(query_result.scalars().all())

    @staticmethod
    async def _take_questions_snaphost(
        db_session: AsyncSession,
    ) -> list[Question]:
        query_result: QueryResult = await db_session.execute(select(Question))
        return list(query_result.scalars().all())

    @staticmethod
    async def _get_question_selectinload(
        question_id: int,
        db_session: AsyncSession,
    ) -> Question | None:
        query_result: QueryResult = await db_session.execute(
            select(Question)
            .where(Question.id == question_id)
            .options(selectinload(Question.answers))
        )
        return query_result.scalar_one_or_none()

    @staticmethod
    async def _get_question(
        question_id: int,
        db_session: AsyncSession,
    ) -> Question | None:
        query_result: QueryResult = await db_session.execute(
            select(Question).where(Question.id == question_id)
        )
        return query_result.scalar_one_or_none()

    @staticmethod
    async def _get_answer(
        answer_id: int,
        db_session: AsyncSession,
    ) -> Answer | None:
        query_result: QueryResult = await db_session.execute(
            select(Answer).where(Answer.id == answer_id)
        )
        return query_result.scalar_one_or_none()

    @staticmethod
    async def _add_question_and_answer(
        db_session: AsyncSession,
        question_text: str,
        answer_text: str,
    ) -> tuple[Question, Answer, uuid.UUID]:
        question: Question = Question(text=question_text)
        db_session.add(question)
        await db_session.commit()
        await db_session.refresh(question)

        user_id: uuid.UUID = uuid.uuid4()
        answer: Answer = Answer(
            user_id=user_id,
            text=answer_text,
            question_id=question.id,
        )
        db_session.add(answer)

        await db_session.commit()
        await db_session.refresh(question)

        return question, answer, user_id

    async def _post_question(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
        text: str,
    ) -> tuple[list[Question], list[Question], dict, int]:
        old_db_questions: list[Question] = await self._take_questions_snaphost(
            db_session=db_session,
        )

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Выполнение запроса
            request_body: dict = {"text": text}
            response: Response = await ac.post(
                questions_prefix,
                json=request_body,
            )

        response_data: dict = response.json()
        new_db_questions: list[Question] = await self._take_questions_snaphost(
            db_session=db_session,
        )

        return old_db_questions, new_db_questions, response_data, response.status_code

    async def _test_invalid_question_creation(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
        invalid_text: str,
        expected_error_message: str = "Недопустимая сущность",
    ) -> None:
        old_db_questions, new_db_questions, response_data, status_code = (
            await self._post_question(
                db_session=db_session,
                base_url=base_url,
                questions_prefix=questions_prefix,
                text=invalid_text,
            )
        )

        assert status_code == 422
        assert response_data["message"] == expected_error_message
        assert len(old_db_questions) == len(new_db_questions)

    async def test_get_all_questions_without_answers_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ) -> None:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Добавление вопроса в БД
            question: Question = Question(text="Question to get")
            db_session.add(question)
            await db_session.commit()
            await db_session.refresh(question)

            # Выполнение запроса
            response: Response = await ac.get(questions_prefix)

        # Проверка
        response_data: dict = response.json()
        db_questions: list[Question] = await self._take_questions_snaphost(
            db_session=db_session,
        )

        assert response.status_code == 200
        assert response_data[0]["text"] == "Question to get"
        assert len(db_questions) == len(response_data) == 1

    async def test_create_question_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ) -> None:
        old_db_questions, new_db_questions, response_data, status_code = (
            await self._post_question(
                db_session=db_session,
                base_url=base_url,
                questions_prefix=questions_prefix,
                text="Question to create",
            )
        )

        assert status_code == 200
        assert response_data["text"] == new_db_questions[0].text == "Question to create"
        assert len(old_db_questions) + 1 == len(new_db_questions)

    async def test_create_question_422_text_field_is_empty(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        await self._test_invalid_question_creation(
            db_session=db_session,
            base_url=base_url,
            questions_prefix=questions_prefix,
            invalid_text="",
        )

    async def test_create_question_422_text_field_consist_of_spaces(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        await self._test_invalid_question_creation(
            db_session=db_session,
            base_url=base_url,
            questions_prefix=questions_prefix,
            invalid_text="",
        )

    async def test_get_question_with_answers_by_id_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Добавление вопроса и ответа в БД
            question, answer, user_id = await self._add_question_and_answer(
                db_session=db_session,
                question_text="Question to get",
                answer_text="Answer to get",
            )

            response: Response = await ac.get(questions_prefix + f"{question.id}")

        response_data: dict = response.json()
        db_question: Question | None = await self._get_question_selectinload(
            db_session=db_session,
            question_id=question.id,
        )

        assert response.status_code == 200
        assert db_question is not None
        assert db_question.text == response_data["text"] == "Question to get"
        assert len(db_question.answers) == len(response_data["answers"]) == 1
        assert (
            db_question.answers[0].text
            == response_data["answers"][0]["text"]
            == "Answer to get"
        )
        assert (
            str(db_question.answers[0].user_id)
            == response_data["answers"][0]["user_id"]
            == str(user_id)
        )

    async def test_get_question_with_answers_by_id_404(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            response: Response = await ac.get(questions_prefix + "0")

        response_data: dict = response.json()
        db_question: Question | None = await self._get_question_selectinload(
            db_session=db_session,
            question_id=0,
        )

        assert response.status_code == 404
        assert db_question is None
        assert response_data["message"] == "Сущность не найдена"

    async def test_delete_question_with_answers_by_id_200(
        self,
        db_session: AsyncSession,
        base_url: str,
        questions_prefix: str,
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url=base_url,
        ) as ac:
            # Добавление вопроса и ответа в БД
            question, answer, user_id = await self._add_question_and_answer(
                db_session=db_session,
                question_text="Question to delete",
                answer_text="Answer to delete",
            )

            # Сохранение количества вопросов и ответов до удаления
            old_db_questions: list[Question] = await self._take_questions_snaphost(
                db_session=db_session
            )
            old_db_answers: list[Answer] = await self._take_answers_snaphost(
                db_session=db_session
            )

            response: Response = await ac.delete(questions_prefix + f"{question.id}")

        response_data: dict = response.json()

        # Получение новых списков вопросов и ответов
        new_db_questions: list[Question] = await self._take_questions_snaphost(
            db_session=db_session
        )
        new_db_answers: list[Answer] = await self._take_answers_snaphost(
            db_session=db_session
        )

        # Получение вопроса после удаления
        deleted_db_question: Question | None = await self._get_question(
            db_session=db_session,
            question_id=question.id,
        )

        # Получение ответа после удаления
        deleted_db_answer: Answer | None = await self._get_answer(
            db_session=db_session,
            answer_id=answer.id,
        )

        assert response.status_code == 200
        assert response_data["text"] == question.text == "Question to delete"
        assert deleted_db_question is None
        assert deleted_db_answer is None
        assert len(new_db_questions) + 1 == len(old_db_questions)
        assert len(new_db_answers) + 1 == len(old_db_answers)
