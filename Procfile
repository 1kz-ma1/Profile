web: gunicorn workpro.wsgi:application --log-file -
release: python manage.py migrate && python manage.py collectstatic --noinput
