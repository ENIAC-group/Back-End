#!/bin/sh

echo "Waiting for postgresql to start..."
./wait-for.sh db:5432 

echo "Migrating the databse...################################################################"
python manage.py migrate --noinput

echo "set admin *******************************************"
DJANGO_SUPERUSER_PASSWORD=eniac@1403 python manage.py createsuperuser --no-input --email=eniakgroupiust@gmail.com

echo "Starting the server...******************************************************************"
python manage.py runserver 0.0.0.0:8000

