from django.db import migrations
from django.conf import settings
import os

def create_superuser(apps, schema_editor):
    # AUTH_USER_MODEL に対応（AbstractUser/Custom User でもOK）
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    UserModel = apps.get_model(app_label, model_name)

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "kazuma012023@gmail.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Kazuma0120")

    # 既に同名ユーザーがいれば何もしない（冪等）
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
