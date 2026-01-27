# Generated migration for category system

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('intro', '0003_create_initial_superuser'),
    ]

    operations = [
        # Create BlogCategory model
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='カテゴリ名')),
                ('slug', models.SlugField(max_length=50, unique=True, verbose_name='スラッグ')),
                ('description', models.TextField(blank=True, verbose_name='説明')),
                ('image', models.ImageField(upload_to='category_images/', verbose_name='カテゴリ画像')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
            ],
            options={
                'verbose_name': 'ブログカテゴリ',
                'verbose_name_plural': 'ブログカテゴリ',
                'ordering': ['name'],
            },
        ),
        
        # Create initial categories with placeholder image paths
        migrations.RunPython(create_categories),
        
        # Add category ForeignKey to BlogPost (temporary)
        migrations.AddField(
            model_name='blogpost',
            name='category_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='intro.blogcategory', verbose_name='カテゴリ'),
        ),
        
        # Migrate data from old category to new category
        migrations.RunPython(migrate_categories),
        
        # Remove old category field and image field
        migrations.RemoveField(
            model_name='blogpost',
            name='category',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='image',
        ),
        
        # Rename category_new to category
        migrations.RenameField(
            model_name='blogpost',
            old_name='category_new',
            new_name='category',
        ),
        
        # Make category non-nullable
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='intro.blogcategory', verbose_name='カテゴリ'),
        ),
    ]

def create_categories(apps, schema_editor):
    """初期カテゴリを作成"""
    BlogCategory = apps.get_model('intro', 'BlogCategory')
    
    categories = [
        {'name': '技術', 'slug': 'tech', 'image': 'category_images/きれいな銀河.jpg'},
        {'name': '日常', 'slug': 'daily', 'image': 'category_images/白強め青リボン.jpg'},
        {'name': '就活', 'slug': 'work', 'image': 'category_images/100年後の東京.jpg'},
        {'name': '趣味', 'slug': 'hobby', 'image': 'category_images/森の夜景.jpg'},
        {'name': '旅行', 'slug': 'travel', 'image': 'category_images/きれいな砂漠の夜空.jpg'},
        {'name': '価値観', 'slug': 'values', 'image': 'category_images/青強め青リボン.jpg'},
        {'name': 'イベント', 'slug': 'event', 'image': 'category_images/黒い大理石.jpg'},
        {'name': 'その他', 'slug': 'other', 'image': 'category_images/白強め青リボン.jpg'},
    ]
    
    for cat_data in categories:
        BlogCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'image': cat_data['image'],
            }
        )

def migrate_categories(apps, schema_editor):
    """既存のブログ記事をカテゴリマスターに紐づける"""
    BlogPost = apps.get_model('intro', 'BlogPost')
    BlogCategory = apps.get_model('intro', 'BlogCategory')
    
    # Map old category values to new category slugs
    category_map = {
        'tech': 'tech',
        'daily': 'daily',
        'work': 'work',
        'hobby': 'hobby',
        'travel': 'travel',
        'values': 'values',
        'event': 'event',
        'other': 'other',
    }
    
    for post in BlogPost.objects.all():
        old_category = post.category
        new_slug = category_map.get(old_category, 'other')
        try:
            category_obj = BlogCategory.objects.get(slug=new_slug)
            post.category_new = category_obj
            post.save()
        except BlogCategory.DoesNotExist:
            # Fallback to 'other' category
            category_obj = BlogCategory.objects.get(slug='other')
            post.category_new = category_obj
            post.save()

def reverse_migrate(apps, schema_editor):
    """ロールバック用（逆向き）"""
    pass
