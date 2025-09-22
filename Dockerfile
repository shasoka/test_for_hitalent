FROM python:3.12.4

WORKDIR /image

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry==2.2.1

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

COPY . .

WORKDIR /image/app

CMD ["gunicorn", "main:app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000", "--access-logfile", "-"]
