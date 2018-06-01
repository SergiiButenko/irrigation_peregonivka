FROM ubuntu:latest  
RUN apt-get update  
RUN apt-get install --no-install-recommends --no-install-suggests -y curl  
RUN apt-get -y install python3-pip
RUN apt-get -y install python-dev python-rpi.gpio
RUN apt-get -y install libpq-dev python3-dev
# RUN adduser sprinkler gpio
# RUN chown root.gpio /dev/gpiomem
# RUN chmod g+rw /dev/gpiomem

RUN mkdir /var/www
WORKDIR /src
COPY . /src/

RUN pip3 install -r requirements.txt
WORKDIR .
# Start gunicorn
CMD ["/usr/local/bin/gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:7543", "--pythonpath", ".", "--user", "root", "gunicorn_irrigation_web:app"]