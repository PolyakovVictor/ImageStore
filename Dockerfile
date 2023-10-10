FROM python:3.8

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install

COPY FastAPI /app/FastAPI

WORKDIR /app/FastAPI

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
