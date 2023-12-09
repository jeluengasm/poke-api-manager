ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION} AS python

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

# Configure Poetry
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install apt packages and Install poetry separated from system interpreter
RUN apt-get update && \
  apt-get install ssh -y && \
  pip install -U pip setuptools && \
  pip install poetry==${POETRY_VERSION}

WORKDIR ${APP_HOME}

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false &&\
    if [ "${BUILD_ENV}" = "local" ]; then \
      poetry install --no-interaction --no-ansi; \
    else \
      poetry install --no-interaction --no-ansi --without dev,test,django-test ; \
    fi

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    && useradd django --user-group --create-home --shell /bin/bash \
    && chown django:django -R ${APP_HOME} \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY ./container/${BUILD_ENV}/scripts/entrypoint.sh ./container/${BUILD_ENV}/scripts/start.sh /

# Fix windows docker bug, convert CRLF to LF
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh && sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

# copy application code to WORKDIR
COPY . ${APP_HOME}
USER django
