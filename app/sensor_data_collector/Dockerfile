FROM python:3.6.9-slim

WORKDIR /app
COPY ./sensor_data_collector/requirements.txt . 
RUN pip install -r requirements.txt

COPY . .
