FROM debian:stretch

RUN apt-get update
RUN apt-get -y install apt-utils
RUN apt-get -y install net-tools
RUN apt-get -y install bash
RUN apt-get -y install vim
RUN apt-get -y install less
RUN apt-get -y install apache2
RUN apt-get -y install python3
RUN apt-get -y install libapache2-mod-wsgi-py3
RUN apt-get -y install python3-pip

#Install python libraries
RUN pip3 install django
RUN pip3 install requests

#Configure apache 
COPY ./iotowl-apache2.conf /etc/apache2/conf-available
RUN a2enconf iotowl-apache2

#Install landing page
COPY ./landing-page/css/ /var/www/html/css/
COPY ./landing-page/js/ /var/www/html/js/
COPY ./landing-page/index.html /var/www/html/index.html

#Install django iotowl project
COPY --chown=www-data:www-data ./iotowl/ /var/www/iotowl/iotowl/
COPY --chown=www-data:www-data ./static/ /var/www/iotowl/static/
COPY --chown=www-data:www-data ./templates/ /var/www/iotowl/templates/

#Install the database (there has to be a better way.
#Right now all data will be lost once the container is shut down.
COPY --chown=www-data:www-data ./db.sqlite3 /var/www/iotowl/

#Install dracocollector django app 
COPY --chown=www-data:www-data ./dracocollector/ /var/www/iotowl/dracocollector/

EXPOSE 8080
CMD apache2ctl -D FOREGROUND
#CMD python3 /var/www/dracoserver/manage.py runserver &
