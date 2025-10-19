#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies with Poetry..."
poetry install --only main

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running migrations..."
python manage.py migrate
