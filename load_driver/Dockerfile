FROM python:3.13-slim

WORKDIR /app
COPY load-driver.py .

RUN pip install --no-cache-dir requests

CMD ["python", "load-driver.py"]
