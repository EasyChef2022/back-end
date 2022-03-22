release: python3 manage.py makemigrations
release: python3 manage.py migrate
web: gunicorn EasyChef.wsgi:application --log-file -