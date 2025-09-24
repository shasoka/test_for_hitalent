import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Result as QueryResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.models import Question


@pytest.mark.asyncio
class TestQuestionsAPI:

    async def test_get_all_questions_without_answers(
        self,
        db_session: AsyncSession,
        base_url: str,
    ):
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
            response = await ac.get("/questions/")

        # Проверка

        data = response.json()
        result: QueryResult = await db_session.execute(select(Question))
        db_questions = result.scalars().all()

        assert response.status_code == 200
        assert len(db_questions) == len(data) == 1
        assert data[0]["text"] == "Question to get"
