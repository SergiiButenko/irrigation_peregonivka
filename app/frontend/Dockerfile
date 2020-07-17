FROM python:3.6.9-slim
EXPOSE 8010

WORKDIR /app
COPY ./frontend/requirements.txt . 
RUN pip install -r requirements.txt

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .