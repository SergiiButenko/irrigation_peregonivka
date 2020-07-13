FROM python:3.6.9-slim

WORKDIR /app
COPY ./ping/requirements.txt . 
RUN pip install -r requirements.txt

COPY . .