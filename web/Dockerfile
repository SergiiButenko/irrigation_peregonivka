FROM ubuntu:latest  
RUN apt-get update  
RUN apt-get install --no-install-recommends --no-install-suggests -y curl  
RUN apt-get -y install python3-pip
RUN apt-get -y install python-dev python-rpi.gpio

RUN mkdir /var/www
WORKDIR /src
COPY . /src/

RUN pip3 install -r requirements.txt
WORKDIR .
# Start gunicorn
CMD ["/usr/local/bin/gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:7543", "--pythonpath", ".", "gunicorn_irrigation_web:app"]