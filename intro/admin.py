from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'post_date', 'is_published')
    list_filter = ('is_published', 'category', 'post_date')
    search_fields = ('title', 'content', 'excerpt')
    ordering = ('-post_date',)
    date_hierarchy = 'post_date'
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('image',)  # 画像フィールドを管理画面から非表示
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'category', 'post_date', 'is_published')
        }),
        ('内容', {
            'fields': ('excerpt', 'content')  # image を削除
        }),
        ('メタ情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
