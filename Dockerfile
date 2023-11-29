FROM python:3.10.13-slim-bullseye AS base

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        bash \
        unzip \
        curl \
        openjdk-11-jre \
    && rm -rf /var/lib/apt/lists/*

# Install Requirements
ADD requirements.txt /
RUN pip install -r /requirements.txt && rm /requirements.txt

# Copy the app source
ADD src/integratedexercise /app

# Copy docker files
ADD docker/ /

CMD [ "/bin/bash", "-c", "/entrypoint.sh" ]