FROM ubuntu:20.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update

RUN apt-get install -y python3-pip \
    mysql-server \
    libmysqlclient-dev 

# ENV GROUP_ID=1000 \
#     USER_ID=1000
RUN mkdir -p /home/www

# create the app user
RUN addgroup --system www && adduser --system --group www
# WORKDIR /var/www/
ENV HOME=/home/www
# ADD . /var/www/
# ADD ./requirements.txt /var/www/requirements.txt
COPY . $HOME
WORKDIR $HOME
RUN pip install -r requirements.txt
RUN chown -R www:www $HOME

USER www

EXPOSE 5090

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5090", "wsgi"]