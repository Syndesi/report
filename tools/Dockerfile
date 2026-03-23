FROM python:3.13-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src:${PYTHONPATH:-}"

RUN apk add --no-cache \
    build-base \
    curl \
    git && \
    pip install --no-cache-dir uv

RUN adduser -D worker

WORKDIR /app

FROM base AS dev

ENV SHELL=/bin/bash

RUN apk add bash
USER worker

FROM base AS prod

COPY src ./src
COPY notebooks ./notebooks
COPY pyproject.toml .

RUN chown -R worker:worker /app && \
    chmod -R 755 /app

USER worker
RUN uv sync --no-dev && \
    uv pip install -e .

EXPOSE 2718

CMD ["uv", "run", "--no-dev", "-m", "marimo", "run", "--no-token", "--host", "0.0.0.0", "notebooks"]
