FROM python:3.10.13-slim-bullseye AS base

# Copy docker files
ADD docker/ /

# Install Requirements
ADD requirements.txt /
RUN pip install -r /requirements.txt && rm /requirements.txt

ADD src/integratedexercise /app

CMD [ "/bin/bash", "-c", "/entrypoint.sh" ]