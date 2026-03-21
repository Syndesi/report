FROM python:3.13-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

RUN apk add --no-cache \
    build-base \
    curl \
    git

RUN pip install --no-cache-dir uv

WORKDIR /app

FROM base AS dev

ENV SHELL=/bin/bash

RUN apk add bash

FROM base AS prod

COPY pyproject.toml .
RUN uv sync --no-dev

COPY src ./src

RUN uv pip install -e .

CMD ["prefect", "worker", "start", "--pool", "signalweaver-pool"]
