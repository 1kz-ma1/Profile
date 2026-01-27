from django.contrib import admin
from django.conf import settings
from .models import BlogPost
import os

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'post_date', 'is_published')
    list_filter = ('is_published', 'category', 'post_date')
    search_fields = ('title', 'content', 'excerpt')
    ordering = ('-post_date',)
    date_hierarchy = 'post_date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'category', 'post_date', 'is_published')
        }),
        ('内容', {
            'fields': ('excerpt', 'content', 'image')
        }),
        ('メタ情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
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
