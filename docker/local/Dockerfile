FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

ARG user=user
ARG group=user
ARG uid=1000
ARG gid=1000

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Adds our application code to the image
COPY . /app
WORKDIR /app/

RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}

RUN chown -R user /app
RUN chmod u+x  gunicorn_start.sh

EXPOSE 8000
