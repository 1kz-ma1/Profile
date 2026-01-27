from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('tech', '技術'),
        ('daily', '日常'),
        ('work', '就活'),
        ('hobby', '趣味'),
        ('travel', '旅行'),
        ('values', '価値観'),
        ('event', 'イベント'),
        ('other', 'その他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="タイトル")
    content = models.TextField(verbose_name="内容")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="抜粋")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name="カテゴリ")
    image = models.CharField(max_length=255, blank=True, default='', verbose_name="画像パス", help_text="staticfiles/img/ 内のファイル名を指定（例: blog-header.jpg）")
    post_date = models.DateTimeField(default=timezone.now, verbose_name="投稿日時")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    is_published = models.BooleanField(default=True, verbose_name="公開")
    
    class Meta:
        verbose_name = "ブログ記事"
        verbose_name_plural = "ブログ記事"
        ordering = ['-post_date']
    
    def __str__(self):
        return self.title
    
    def get_category_display_name(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, 'その他')
    
    def get_image_url(self):
        """Get image URL from static files - returns None if not set"""
        if self.image:
            return f"/static/img/{self.image}"
        return None
