#!/bin/sh

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
