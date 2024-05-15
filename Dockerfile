FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir flask

COPY . .

EXPOSE 5000

ENV SERVER_ID DefaultServer

CMD ["python","Task.py"]