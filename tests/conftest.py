import asyncio
import logging
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio

from app.core.models.base import Base
from app.core.models.db_setup import db_helper

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


@pytest.fixture
def base_url():
    return "http://test/api"


@pytest_asyncio.fixture(autouse=True)
async def db_lifespan():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db_helper.dispose()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[Any, Any]:
    async with db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()
