from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from typing import AsyncGenerator

from app.core.config import settings


class DatabaseSetup:
    def __init__(
        self,
        url: str,
        echo: bool = False,  # Вывод информации о запросах
        echo_pool: bool = False,  # Вывод информации о подключениях
        max_overflow: int = 10,  # Количество переполнения подключений
        pool_size: int = 5,  # Количество одновременных подключений
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


# Объект, используемый в механизме внедрения зависимостей для получения
# подключения к БД
db_helper = DatabaseSetup(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)
