#!/usr/bin/env bash

set -o errexit

# Install dependencies
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# No need to collect static files
# python manage.py collectstatic --noinput --clear

# Make the file executable
chmod +x build.sh
