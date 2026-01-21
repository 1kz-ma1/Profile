web: DJANGO_SETTINGS_MODULE=workpro.settings gunicorn workpro.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 60
release: python manage.py migrate && python manage.py collectstatic --noinput