FROM python:3.10-slim

WORKDIR /app

COPY app/ /app/
COPY data/ /data/

RUN pip install -r /app/requirements.txt


CMD ["python", "main.py", "-h"]

