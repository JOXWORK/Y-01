FROM python:3.13.7-trixie AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /application

RUN pip install --upgrade pip wheel "poetry==2.4.0"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY application .

RUN chmod +x entrypoint.sh run

FROM base AS app

ENTRYPOINT ["./entrypoint.sh"]

CMD ["./run"]

FROM base AS worker

CMD ["taskiq", "worker", "core.taskiq.broker:broker", "core.tasks"]