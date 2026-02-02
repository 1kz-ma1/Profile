# Generated migration for custom chapter title field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0008_add_view_switcher_fields'),
    ]

    operations = [
        # カスタムセクション名フィールドを追加
        migrations.AddField(
            model_name='blogpost',
            name='chapter_title',
            field=models.CharField(blank=True, max_length=100, verbose_name='セクション名', help_text='章構成ビューでのグループ名（例: 資格、技術、第1章など）。未入力時は章番号から自動生成'),
        ),
        # 章番号のヘルプテキストを更新
        migrations.AlterField(
            model_name='blogpost',
            name='chapter_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='章番号（旧）', help_text='セクション名が未設定の場合の表示順（例: 1=第1章）。セクション名を優先推奨'),
        ),
        # 章内順序のverbose_nameを更新
        migrations.AlterField(
            model_name='blogpost',
            name='chapter_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='セクション内順序', help_text='同じセクション内での表示順序'),
        ),
    ]
