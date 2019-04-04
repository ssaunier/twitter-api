release: python manage.py db upgrade
web: gunicorn wsgi:application --access-logfile=-
