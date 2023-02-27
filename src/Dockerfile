FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src


RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

COPY ./pyproject.toml ./poetry.lock* /src/
RUN poetry update && poetry install

COPY . .
