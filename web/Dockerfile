FROM ubuntu:latest  
#FROM resin/rpi-raspbian:jessie
RUN apt-get update  
RUN apt-get install --no-install-recommends --no-install-suggests -y curl  
RUN apt-get -y install python3-pip python-dev python-rpi.gpio
RUN apt-get -y install libpq-dev python3-dev

RUN mkdir /var/www
WORKDIR /src
COPY . /src/

RUN pip3 install -r requirements.txt
WORKDIR .
# Start gunicorn
EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:8000", "--pythonpath", ".", "--user", "root", "gunicorn_irrigation_web:app"]