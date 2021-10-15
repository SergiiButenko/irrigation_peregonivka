FROM python:3.9.5-slim

WORKDIR /app
COPY ./notification_service/requirements.txt . 
RUN pip install -r requirements.txt

COPY . .