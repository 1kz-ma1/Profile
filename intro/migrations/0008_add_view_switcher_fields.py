# Generated migration for blog view switcher fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0007_populate_dx_categories'),
    ]

    operations = [
        # 章番号フィールド
        migrations.AddField(
            model_name='blogpost',
            name='chapter_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='章番号', help_text='章構成ビューでの表示順（例: 1=第1章）'),
        ),
        # 章内順序フィールド
        migrations.AddField(
            model_name='blogpost',
            name='chapter_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='章内順序', help_text='同じ章内での表示順序'),
        ),
        # 分野タグフィールド
        migrations.AddField(
            model_name='blogpost',
            name='field_tags',
            field=models.CharField(blank=True, max_length=200, verbose_name='分野タグ', help_text='カンマ区切りで複数指定可能（例: Python,Django,Web開発）'),
        ),
        # 関連記事（多対多）
        migrations.AddField(
            model_name='blogpost',
            name='related_posts',
            field=models.ManyToManyField(blank=True, to='intro.blogpost', verbose_name='関連記事', help_text='相関図ビューで関連を表示する記事'),
        ),
    ]
