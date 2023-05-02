#!/bin/bash

python3 ./manage.py migrate --no-input --skip-checks
python3 ./manage.py runserver 0.0.0.0:8000
python3 ./manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin2',' ', 'admin')"

