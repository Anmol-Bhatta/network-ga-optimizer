# Dockerfile for Simulated Server
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server-app.py .

EXPOSE 80
CMD ["python", "server-app.py"]
