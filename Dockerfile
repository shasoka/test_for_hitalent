FROM python:3.12.4

ARG INSTALL_DEV=false

WORKDIR /image

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install poetry==2.2.1

RUN poetry config virtualenvs.create false && \
    if [ "$INSTALL_DEV" = "true" ]; then \
        poetry install --with dev --no-interaction --no-ansi; \
    else \
        poetry install --only main --no-interaction --no-ansi; \
    fi

COPY . .

WORKDIR /image/app
