#!/bin/sh

if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
  echo "DEBUG mode: skipping makemigrations and collectstatic."
  python manage.py migrate --noinput
else
  python manage.py makemigrations --noinput
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
fi

exec "$@"
