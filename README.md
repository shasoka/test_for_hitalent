## Тестовое задание: API-сервис для вопросов и ответов

### 1. Развертывание
1. В `./app/` создать `.env` файл с содержимым вида:
```dotenv
# Переменные для pydantic-settings
APP_CONFIG__DB__URL=postgresql+asyncpg://mega_usr:super_pass@db:5432/cool_db

# Переменные для docker-compose
POSTGRES_USER=mega_usr
POSTGRES_PASSWORD=super_pass
POSTGRES_DB=cool_db
```
2. Для обычного запуска - из корня проекта:
```bash
docker compose -f docker-compose.yaml -p hitalent_prod up --build -d
```
Интерактивная документация `Swagger UI` будет доступна по адресу [`http://localhost:8000/`](http://localhost:8000/) (приложение само сделает редирект на `/docs`).

Для прогона тестов - тоже из корня проекта:
```bash
docker compose -f docker-compose.test.yaml -p hitalent_test up --build --abort-on-container-exit test-fastapi
```
Здесь `--abort-on-container-exit` должен положить оба контейнера (и БД, и само приложение), но для чистоты логов я делал `attach` только к контейнеру с приложением (`test-fastapi`), поэтому БД остается жить. Можно не делать `attach`, тогда оба контейнера исправно остановятся.

После завершения тестов:
```bash
docker compose -f docker-compose.test.yaml -p hitalent_test down -v
```
`hitalent_prod` и `hitalent_test` - названия групп контейнеров, они могут быть любыми. После каждого тестового прогона НЕ обязательно ронять контейнеры с `-v`, т. к. БД от старта к старту будет чистая, но можно делать (и я делал) для уверенности в результате 🙂

### 2. Тезисно о проекте
- 📚 Стек: `FastAPI`, `SQLAlchemy` с асинхронным двжиком `asyncpg`, `Pydantic` и `pydantic-settings` для конфигурации, для миграций использовал `Alembic`, тесты с `pytest` и `pytest-asyncio`, пакетный менеджер `poetry`.
- ✍️ Ко всему написаны docstring'и (кроме тестов и интерактивной документации, решил не тратить время на `Given-When-Then` и `Swagger` и сдать задание раньше).
- 🧪 Интеграционные тесты для всех кейсов `Questions API` (`Answers API` обделил по той же причине, что и документацию к тестам).
- 📃 Имеется логгер в файл (без временной ротации). Логи хранятся в корне проекта, поэтому можно:
```bash
docker exec -it api_service tail -n 100 ../app.log
```
- 🤓 Соблюдены все функциональные и нефункциональные требования, а также рекомендации на тему чистоты и читаемости кода.
- 😶‍🌫️ `README` писал сам!
