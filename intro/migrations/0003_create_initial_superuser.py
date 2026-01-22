from django.db import migrations
from django.conf import settings
import os

def create_superuser(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    UserModel = apps.get_model(app_label, model_name)

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpass")

    if not UserModel.objects.filter(username=username).exists():
        UserModel.objects.create_superuser(username=username, email=email, password=password)

def noop(apps, schema_editor):
    # 逆マイグレーションは何もしない（安全）
    pass

class Migration(migrations.Migration):

    dependencies = [
        # 直前の intro のマイグレーションに合わせて修正してください
        # 例：("intro", "0001_initial")
        ("intro", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser, noop),
    ]
