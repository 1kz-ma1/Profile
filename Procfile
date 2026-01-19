web: gunicorn workpro.wsgi:application --log-file -
release: sh -c 'python manage.py migrate && python manage.py collectstatic --noinput && (python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 2>/dev/null || true) && (python manage.py shell << EOF
from django.contrib.auth.models import User
import os
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
if username and password:
    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.save()
        print(f"✅ Password set for {username}")
EOF
2>/dev/null || true)'
