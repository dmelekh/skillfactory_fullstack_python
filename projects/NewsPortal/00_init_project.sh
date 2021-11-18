#!/bin/bash

# sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate

pip3 install django
# python -m pip install Django
# pip3 list
django-admin startproject Portal
cd ./Portal

python3 manage.py startapp news

# make Models and then
python3 manage.py makemigrations

python3 manage.py migrate

# run Django shell to add rows in tables of models
python3 manage.py shell

# python3 manage.py runserver

