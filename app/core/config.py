from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("settings",)


class RunConfig(BaseModel):
    app_location: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class AppObjectConfig(BaseModel):
    title: str = "API-сервис для вопросов и ответов"
    summary: str = 'Тестовое задание на вакансию "Junior Python разработчик" 😎'
    description: str = (
        "Добро пожаловать 🤝 \n\n[GitHub➚](https://github.com/shasoka/...)"  # TODO: link
    )

    version: str = "0.0.1"
    swagger_ui_parameters: dict[str, dict[str, str]] = {
        "syntaxHighlight": {
            "theme": "obsidian",
        }
    }


class ApiQuestions(BaseModel):
    prefix: str = "/questions"
    tags: list[str] = ["Questions"]


class ApiAnswers(BaseModel):
    prefix: str = "/answers"
    tags: list[str] = ["Answers"]


class ApiBaseConfig(BaseModel):
    slash: str = "/"
    docs: str = "/docs"

    prefix: str = "/api"
    tags: list[str] = ["Q&A API"]

    # --- Sub-routers ---

    questions: ApiQuestions = ApiQuestions()
    answers: ApiAnswers = ApiAnswers()


class Database(BaseModel):
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
