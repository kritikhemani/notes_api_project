FROM python:3.12

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]