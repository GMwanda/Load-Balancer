
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV SERVER_ID DefaultServer
ENV DOCKER_HOST unix://var/run/docker.sock

CMD ["gunicorn","-b","0.0.0.0:5000", "Task:app"]
