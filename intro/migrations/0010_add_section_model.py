# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0009_add_custom_chapter_title'),
    ]

    operations = [
        # Sectionモデルを作成
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='セクション名')),
                ('order', models.IntegerField(default=0, verbose_name='表示順')),
                ('description', models.TextField(blank=True, verbose_name='説明')),
                ('icon', models.CharField(blank=True, max_length=50, verbose_name='アイコン（絵文字）')),
                ('is_active', models.BooleanField(default=True, verbose_name='有効')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
            ],
            options={
                'verbose_name': 'セクション',
                'verbose_name_plural': 'セクション',
                'ordering': ['order', 'name'],
            },
        ),
        
        # BlogPostにsectionフィールドを追加
        migrations.AddField(
            model_name='blogpost',
            name='section',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='posts',
                to='intro.section',
                verbose_name='セクション'
            ),
        ),
        
        # chapter_title, chapter_numberのヘルプテキストを更新（非推奨マーク）
        migrations.AlterField(
            model_name='blogpost',
            name='chapter_title',
            field=models.CharField(
                blank=True,
                max_length=100,
                verbose_name='章のタイトル',
                help_text='非推奨：代わりにセクションを使用してください'
            ),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='chapter_number',
            field=models.IntegerField(
                blank=True,
                null=True,
                verbose_name='章番号',
                help_text='非推奨：代わりにセクションを使用してください'
            ),
        ),
    ]
