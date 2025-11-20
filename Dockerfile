FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "src.api_proxy.main:app", "--host", "0.0.0.0", "--port", "8000"]
