#!/bin/sh

echo "Waiting for postgresql to start..."
./wait-for.sh db:5432 

echo "Migrating the databse..."
python manage.py migrate 

echo "Starting the server...******************************************************************"
python manage.py runserver 0.0.0.0:8000