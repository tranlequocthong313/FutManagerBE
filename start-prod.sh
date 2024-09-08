#!/bin/bash


pip install -r requirements.txt

python3 manage.py collectstatic --no-input

python3 manage.py makemigrations 
python3 manage.py migrate

python3 manage.py createcachetable
python3 manage.py createdefaultdata


