#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input --clear
python manage.py migrate
