# Dockerfile for GA Controller
FROM python:3.13-slim

WORKDIR /app/ga_controller

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
