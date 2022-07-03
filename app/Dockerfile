FROM ubuntu:20.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update

RUN apt-get install -y python3-pip \
    mysql-server \
    libmysqlclient-dev 

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
ADD ./requirements.txt /var/www/requirements.txt

RUN pip install -r requirements.txt
RUN adduser --system --group www
# RUN addgroup --gid $GROUP_ID www
# RUN adduser --uid $USER_ID --home "www" --shell /bin/sh 

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]