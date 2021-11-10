#!/bin/bash

sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate

pip3 install django
# python -m pip install Django
pip3 list
django-admin startproject my_project
cd ./my_project

python3 manage.py runserver
