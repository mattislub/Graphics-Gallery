#!/bin/sh

APP_PORT="8000"
set -e

python manage.py wait_for_db
python manage.py tailwind install --no-input
python manage.py tailwind build --no-input
echo yes | python manage.py collectstatic
python manage.py migrate

gunicorn --bind "0.0.0.0:${APP_PORT}" --workers=4 app.wsgi
