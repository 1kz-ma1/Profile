
web: cd workpro && gunicorn workpro.wsgi --bind 0.0.0.0:$PORT
release: cd workpro && python manage.py migrate && python manage.py collectstatic --noinput