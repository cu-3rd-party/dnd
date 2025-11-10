FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "my_app.wsgi:application"]
