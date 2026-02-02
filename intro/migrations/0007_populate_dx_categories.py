# Data migration to populate DX category and subcategories

from django.db import migrations


def create_dx_categories(apps, schema_editor):
    """DXカテゴリとサブカテゴリを作成"""
    Category = apps.get_model('intro', 'Category')
    SubCategory = apps.get_model('intro', 'SubCategory')
    
    # 既存のカテゴリを作成（既存データとの互換性のため）
    existing_categories = [
        {'name': '技術', 'slug': 'tech', 'order': 1},
        {'name': '日常', 'slug': 'daily', 'order': 2},
        {'name': '就活', 'slug': 'work', 'order': 3},
        {'name': '趣味', 'slug': 'hobby', 'order': 4},
        {'name': '旅行', 'slug': 'travel', 'order': 5},
        {'name': '価値観', 'slug': 'values', 'order': 6},
        {'name': 'イベント', 'slug': 'event', 'order': 7},
    ]
    
    for cat_data in existing_categories:
        Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name'], 'order': cat_data['order']}
        )
    
    # DXカテゴリを作成
    dx_category, created = Category.objects.get_or_create(
        slug='dx',
        defaults={'name': 'DX', 'order': 8}
    )
    
    # DXサブカテゴリを作成
    dx_subcategories = [
        {'name': 'AI活用', 'slug': 'ai-utilization', 'order': 1},
        {'name': '医療DX', 'slug': 'medical-dx', 'order': 2},
        {'name': '行政DX', 'slug': 'government-dx', 'order': 3},
        {'name': '教育DX', 'slug': 'education-dx', 'order': 4},
        {'name': '制度・マイナンバー', 'slug': 'system-mynumber', 'order': 5},
        {'name': '可視化モデル（Modeling）', 'slug': 'visualization-modeling', 'order': 6},
    ]
    
    for sub_data in dx_subcategories:
        SubCategory.objects.get_or_create(
            category=dx_category,
            slug=sub_data['slug'],
            defaults={'name': sub_data['name'], 'order': sub_data['order']}
        )
    
    # その他カテゴリを作成
    Category.objects.get_or_create(
        slug='other',
        defaults={'name': 'その他', 'order': 99}
    )


def reverse_dx_categories(apps, schema_editor):
    """ロールバック処理"""
    Category = apps.get_model('intro', 'Category')
    SubCategory = apps.get_model('intro', 'SubCategory')
    
    # DXサブカテゴリを削除
    dx_category = Category.objects.filter(slug='dx').first()
    if dx_category:
        SubCategory.objects.filter(category=dx_category).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0006_add_category_subcategory_models'),
    ]

    operations = [
        migrations.RunPython(create_dx_categories, reverse_dx_categories),
    ]
