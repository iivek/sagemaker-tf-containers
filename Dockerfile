FROM ubuntu:latest

ENV SAVEDMODEL_LOCAL=/app/models

RUN apt-get update -qq && apt-get install -qqy curl python3.9 python3-pip

# install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Docker from Docker Inc. repositories.
RUN curl -sSL https://get.docker.com/ | sh

COPY . /app
WORKDIR /app

# generate Dockerfile
RUN mkdir ${SAVEDMODEL_LOCAL}
ENTRYPOINT ["/bin/bash", "./model_server.sh"]
