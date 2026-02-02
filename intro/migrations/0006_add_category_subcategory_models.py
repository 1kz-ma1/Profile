# Generated migration for category and subcategory models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0005_blogpost_likes_count'),
    ]

    operations = [
        # Create Category model
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='カテゴリ名')),
                ('slug', models.SlugField(unique=True, verbose_name='スラッグ')),
                ('order', models.IntegerField(default=0, verbose_name='表示順')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
            ],
            options={
                'verbose_name': 'カテゴリ',
                'verbose_name_plural': 'カテゴリ',
                'ordering': ['order', 'name'],
            },
        ),
        # Create SubCategory model
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='サブカテゴリ名')),
                ('slug', models.SlugField(verbose_name='スラッグ')),
                ('order', models.IntegerField(default=0, verbose_name='表示順')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='intro.category', verbose_name='メインカテゴリ')),
            ],
            options={
                'verbose_name': 'サブカテゴリ',
                'verbose_name_plural': 'サブカテゴリ',
                'ordering': ['order', 'name'],
                'unique_together': {('category', 'slug')},
            },
        ),
        # Update BlogPost model - add new fields
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.CharField(blank=True, choices=[('tech', '技術'), ('daily', '日常'), ('work', '就活'), ('hobby', '趣味'), ('travel', '旅行'), ('values', '価値観'), ('event', 'イベント'), ('dx', 'DX'), ('other', 'その他')], default='other', max_length=20, null=True, verbose_name='旧カテゴリ'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='main_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='intro.category', verbose_name='メインカテゴリ'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='intro.subcategory', verbose_name='サブカテゴリ'),
        ),
    ]
