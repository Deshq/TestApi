#! /bin/bash

pipenv run python manage.py makemigrations --no-input

pipenv run python manage.py migrate --no-input

exec "$@"
