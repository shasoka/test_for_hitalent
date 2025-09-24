"""Модуль, содержащий настройки приложения."""

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("settings",)


class RunConfig(BaseModel):
    """Конфигурация запуска приложения."""

    app_location: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class AppObjectConfig(BaseModel):
    """Конфигурация объекта FastAPI."""

    title: str = "API-сервис для вопросов и ответов"
    summary: str = 'Тестовое задание на вакансию "Junior Python разработчик" 😎'
    description: str = (
        "Добро пожаловать 🤝 \n\n[GitHub➚](https://github.com/shasoka/test_for_hitalent)"
    )

    version: str = "0.0.1"
    swagger_ui_parameters: dict[str, dict[str, str]] = {
        "syntaxHighlight": {
            "theme": "obsidian",
        }
    }


class ApiQuestions(BaseModel):
    """Конфигурация Questions API."""

    prefix: str = "/questions"
    tags: list[str] = ["Questions"]


class ApiAnswers(BaseModel):
    """Конфигурация Questions API."""

    prefix: str = "/answers"
    tags: list[str] = ["Answers"]


class ApiBaseConfig(BaseModel):
    """Базовая конфигурация API."""

    slash: str = "/"
    docs: str = "/docs"

    prefix: str = "/api"
    tags: list[str] = ["Q&A API"]

    questions: ApiQuestions = ApiQuestions()
    answers: ApiAnswers = ApiAnswers()


class Database(BaseModel):
    """Конфигурация ORM и БД."""

    url: PostgresDsn  # подтягивается из .env
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    """Основной класс конфигурации приложения."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=".env",
        # игнорирует переменные, которые начинаются не с префикса
        extra="ignore",
    )

    run: RunConfig = RunConfig()
    app: AppObjectConfig = AppObjectConfig()
    api: ApiBaseConfig = ApiBaseConfig()
    db: Database


# noinspection PyArgumentList
settings: Settings = Settings()
