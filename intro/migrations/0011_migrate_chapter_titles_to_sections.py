# Generated migration - データ移行
from django.db import migrations


def migrate_chapter_titles_to_sections(apps, schema_editor):
    """既存のchapter_titleをSectionモデルに移行"""
    BlogPost = apps.get_model('intro', 'BlogPost')
    Section = apps.get_model('intro', 'Section')
    
    # 既存の一意なchapter_titleを取得（空でないもののみ）
    existing_titles = BlogPost.objects.exclude(chapter_title='').values_list('chapter_title', flat=True).distinct()
    
    # 各タイトルに対してSectionを作成（既に存在しなければ）
    for index, title in enumerate(existing_titles, start=1):
        if title:  # 空でない場合のみ
            section, created = Section.objects.get_or_create(
                name=title,
                defaults={
                    'order': index * 10,  # 10刻みで順序を設定（後で挿入しやすいように）
                    'description': '',
                    'icon': '📖',  # デフォルトアイコン
                    'is_active': True,
                }
            )
            
            # このタイトルを持つすべての投稿にセクションを割り当て
            BlogPost.objects.filter(chapter_title=title).update(section=section)
    
    # chapter_numberのみ設定されている投稿の処理
    posts_with_number = BlogPost.objects.filter(chapter_title='').exclude(chapter_number__isnull=True)
    for post in posts_with_number:
        chapter_name = f'第{post.chapter_number}章'
        section, created = Section.objects.get_or_create(
            name=chapter_name,
            defaults={
                'order': post.chapter_number * 10 if post.chapter_number else 999,
                'description': '',
                'icon': '📖',
                'is_active': True,
            }
        )
        post.section = section
        post.save()


def reverse_migration(apps, schema_editor):
    """ロールバック時の処理（必要に応じて）"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0010_add_section_model'),
    ]

    operations = [
        migrations.RunPython(migrate_chapter_titles_to_sections, reverse_migration),
    ]
