#!/bin/bash

source ~/.bashrc
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL --rut $DJANGO_SUPERUSER_RUT --nombre $DJANGO_SUPERUSER_USERNAME --apellidoP $DJANGO_SUPERUSER_APELLIDOP --apellidoM $DJANGO_SUPERUSER_APELLIDOM
service apache2 restart
gunicorn SigVip.wsgi