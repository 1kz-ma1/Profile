from django.contrib import admin
from django.conf import settings
from .models import BlogPost, Category, SubCategory
import os

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'created_at')
    search_fields = ('name', 'slug')
    ordering = ('order', 'name')
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'order', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'slug')
    ordering = ('category', 'order', 'name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category_info', 'likes_count', 'post_date', 'is_published')
    list_filter = ('is_published', 'main_category', 'sub_category', 'post_date')
    search_fields = ('title', 'content', 'excerpt')
    ordering = ('-post_date',)
    date_hierarchy = 'post_date'
    readonly_fields = ('created_at', 'updated_at')
    
    def get_category_info(self, obj):
        """カテゴリ情報を表示"""
        if obj.main_category:
            if obj.sub_category:
                return f"{obj.main_category.name} - {obj.sub_category.name}"
            return obj.main_category.name
        return obj.get_category_display() if obj.category else "未設定"
    get_category_info.short_description = "カテゴリ"
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'post_date', 'is_published')
        }),
        ('カテゴリ', {
            'fields': ('main_category', 'sub_category', 'category'),
            'description': '新しいカテゴリシステム（main_category/sub_category）を使用してください。旧categoryフィールドは後方互換性のために残されています。'
        }),
        ('ビュー切り替え用設定', {
            'fields': ('chapter_number', 'chapter_order', 'field_tags', 'related_posts'),
            'classes': ('collapse',),
            'description': '章構成ビューと相関図ビューで使用する設定です。'
        }),
        ('内容', {
            'fields': ('excerpt', 'content', 'image')
        }),
        ('エンゲージメント', {
            'fields': ('likes_count',)
        }),
        ('メタ情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('related_posts',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """サブカテゴリをメインカテゴリでフィルタリング"""
        if db_field.name == "sub_category":
            # JavaScriptで動的にフィルタリングする方が良いが、
            # シンプルにすべてのサブカテゴリを表示
            pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """image フィールドをドロップダウンに変換"""
        if db_field.name == 'image':
            # staticfiles/img/ 配下の画像一覧を取得
            img_dir = os.path.join(settings.BASE_DIR, 'staticfiles', 'img')
            choices = [('', '---')]
            
            if os.path.exists(img_dir):
                for filename in sorted(os.listdir(img_dir)):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        choices.append((filename, filename))
            
            from django.forms import ChoiceField, Select
            return ChoiceField(
                choices=choices,
                required=False,
                widget=Select(attrs={'style': 'width: 100%; max-width: 500px;'}),
                **kwargs
            )
        
        return super().formfield_for_dbfield(db_field, request, **kwargs)
