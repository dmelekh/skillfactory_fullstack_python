#!/bin/bash

source ./venv/bin/activate
cd ./my_project
python3 manage.py migrate
# python3 manage.py runserver 
# no exceptions got!
python3 manage.py createsuperuser
# http://127.0.0.1:8000/admin

python3 manage.py runserver

