FROM python:3.9.5-alpine

WORKDIR /app
COPY ./device_discovery/requirements.txt . 
RUN pip install -r requirements.txt

COPY ./app .