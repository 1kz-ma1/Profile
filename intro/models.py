from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage

class Category(models.Model):
    """メインカテゴリ"""
    name = models.CharField(max_length=50, unique=True, verbose_name="カテゴリ名")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="スラッグ")
    order = models.IntegerField(default=0, verbose_name="表示順")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """サブカテゴリ"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="メインカテゴリ")
    name = models.CharField(max_length=50, verbose_name="サブカテゴリ名")
    slug = models.SlugField(max_length=50, verbose_name="スラッグ")
    order = models.IntegerField(default=0, verbose_name="表示順")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    
    class Meta:
        verbose_name = "サブカテゴリ"
        verbose_name_plural = "サブカテゴリ"
        ordering = ['order', 'name']
        unique_together = [['category', 'slug']]
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class BlogPost(models.Model):
    # 後方互換性のための旧カテゴリ選択肢（既存データ用）
    CATEGORY_CHOICES = [
        ('tech', '技術'),
        ('daily', '日常'),
        ('work', '就活'),
        ('hobby', '趣味'),
        ('travel', '旅行'),
        ('values', '価値観'),
        ('event', 'イベント'),
        ('dx', 'DX'),
        ('other', 'その他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="タイトル")
    content = models.TextField(verbose_name="内容")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="抜粋")
    # 旧カテゴリフィールド（後方互換性のため残す）
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', blank=True, null=True, verbose_name="旧カテゴリ")
    # 新カテゴリシステム
    main_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="メインカテゴリ")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="サブカテゴリ")
    
    # ビュー切り替え用フィールド
    chapter_number = models.IntegerField(null=True, blank=True, verbose_name="章番号", help_text="章構成ビューでの表示順（例: 1=第1章）")
    chapter_order = models.IntegerField(null=True, blank=True, verbose_name="章内順序", help_text="同じ章内での表示順序")
    field_tags = models.CharField(max_length=200, blank=True, verbose_name="分野タグ", help_text="カンマ区切りで複数指定可能（例: Python,Django,Web開発）")
    related_posts = models.ManyToManyField('self', blank=True, symmetrical=True, verbose_name="関連記事", help_text="相関図ビューで関連を表示する記事")
    
    image = models.CharField(max_length=255, blank=True, default='', verbose_name="画像パス", help_text="staticfiles/img/ 内のファイル名を指定（例: blog-header.jpg）")
    likes_count = models.IntegerField(default=0, verbose_name="良いね数")
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
        """カテゴリ表示名を取得（新システム優先）"""
        if self.main_category:
            if self.sub_category:
                return f"{self.main_category.name} - {self.sub_category.name}"
            return self.main_category.name
        # 旧システムのフォールバック
        return dict(self.CATEGORY_CHOICES).get(self.category, 'その他')
    
    def get_image_url(self):
        """Get image URL from static files - returns None if not set"""
        if self.image:
            return f"/static/img/{self.image}"
        return None
    
    def get_field_tags_list(self):
        """分野タグをリストで取得"""
        if self.field_tags:
            return [tag.strip() for tag in self.field_tags.split(',') if tag.strip()]
        return []
    
    def get_chapter_title(self):
        """章タイトルを取得"""
        if self.chapter_number:
            return f"第{self.chapter_number}章"
        return "未分類"
