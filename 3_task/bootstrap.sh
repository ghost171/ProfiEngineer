#!/bin/sh
export FLASK_APP=./promoactions/index.py
source $(pipenv --venv)/bin/activate
flask run -h localhost -p 8080

