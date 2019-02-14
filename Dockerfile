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
COPY ./iotowl/ /var/www/iotowl/
COPY ./static/ /var/www/iotowl/
COPY ./templates/ /var/www/iotowl/

#Install dracocollector django app 
COPY ./dracocollector/ /var/www/iotowl/

EXPOSE 8080
CMD apache2ctl -D FOREGROUND
#CMD python3 /var/www/dracoserver/manage.py runserver &
