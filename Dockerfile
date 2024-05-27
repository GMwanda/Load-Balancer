
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y docker.io
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install docker
RUN pip install docker gunicorn

COPY . .

EXPOSE 5000

ENV SERVER_ID DefaultServer
ENV DOCKER_HOST unix://var/run/docker.sock

CMD ["gunicorn","-b","0.0.0.0:5000", "Task:app"]
