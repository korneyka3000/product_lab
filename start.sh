#!/bin/bash

python manage.py collectstatic --noinput

gunicorn --bind :8000 test_for_product_lab.wsgi:application
