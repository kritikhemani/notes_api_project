FROM python:3.12

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "echo 'Running migrations...' && python -m alembic upgrade head && echo 'Starting server...' && uvicorn app.main:app --host 0.0.0.0 --port $PORT"]