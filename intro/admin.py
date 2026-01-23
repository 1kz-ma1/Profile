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
