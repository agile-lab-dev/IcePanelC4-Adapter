FROM python:3.11

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY server_start.sh .

WORKDIR /app/src
COPY src/. .

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

EXPOSE 5002

ENTRYPOINT ["bash", "server_start.sh"]
