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

class Section(models.Model):
    """章構成ビュー用のセクション"""
    name = models.CharField(max_length=100, unique=True, verbose_name="セクション名", help_text="例: 資格、技術、プロジェクト、第1章など")
    order = models.IntegerField(default=0, verbose_name="表示順", help_text="数値が小さいほど上に表示されます")
    description = models.TextField(blank=True, verbose_name="説明", help_text="このセクションの説明（任意）")
    icon = models.CharField(max_length=10, blank=True, verbose_name="アイコン", help_text="絵文字など（例: 📖, 💻, 🚀）")
    is_active = models.BooleanField(default=True, verbose_name="有効", help_text="無効にすると章構成ビューに表示されません")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    class Meta:
        verbose_name = "セクション"
        verbose_name_plural = "セクション"
        ordering = ['order', 'name']
    
    def __str__(self):
        icon = f"{self.icon} " if self.icon else ""
        return f"{icon}{self.name}"
    
    def get_post_count(self):
        """このセクションの記事数を取得"""
        return self.posts.filter(is_published=True).count()
    get_post_count.short_description = "記事数"

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
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name="セクション", help_text="章構成ビューでのグループ（推奨）")
    chapter_title = models.CharField(max_length=100, blank=True, verbose_name="セクション名（旧）", help_text="非推奨：代わりにセクション選択を使用してください")
    chapter_number = models.IntegerField(null=True, blank=True, verbose_name="章番号（旧）", help_text="非推奨：代わりにセクション選択を使用してください")
    chapter_order = models.IntegerField(null=True, blank=True, verbose_name="セクション内順序", help_text="同じセクション内での表示順序（数値が小さいほど上）")
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
        """セクションタイトルを取得（Sectionモデルを優先）"""
        # Sectionモデルが設定されていればそれを使用（最優先）
        if self.section:
            return str(self.section)
        # 旧カスタムセクション名が設定されていればそれを使用
        if self.chapter_title:
            return self.chapter_title
        # 章番号が設定されていれば「第○章」形式
        if self.chapter_number:
            return f"第{self.chapter_number}章"
        # どちらも未設定の場合
        return "未分類"
    
    def get_chapter_sort_key(self):
        """セクションのソートキーを取得"""
        # Sectionモデルがある場合はその表示順を使用
        if self.section:
            return f"{self.section.order:05d}_{self.section.name}"
        # 旧カスタムタイトルがある場合はそれを使用
        if self.chapter_title:
            return self.chapter_title
        # 章番号がある場合は数値でソート
        if self.chapter_number:
            return f"chapter_{self.chapter_number:05d}"
        # 未分類は最後
        return "zzz_未分類"


class ContactFormSubmission(models.Model):
    """お問い合わせフォーム送信データ"""
    name = models.CharField(max_length=100, verbose_name="お名前")
    design = models.IntegerField(verbose_name="サイトの見やすさ・デザイン", help_text="1-5")
    portfolio = models.IntegerField(verbose_name="作品紹介の評価", help_text="1-5")
    dx_ai = models.IntegerField(verbose_name="DX×AI作品の評価", help_text="1-5")
    navigation = models.IntegerField(verbose_name="ナビゲーションの使いやすさ", help_text="1-5")
    information = models.IntegerField(verbose_name="情報の分かりやすさ", help_text="1-5")
    overall = models.IntegerField(verbose_name="全体的な満足度", help_text="1-5")
    message = models.TextField(blank=True, verbose_name="ご意見・ご感想")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="送信日時")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IPアドレス")
    user_agent = models.TextField(blank=True, verbose_name="ユーザーエージェント")
    
    class Meta:
        verbose_name = "お問い合わせ"
        verbose_name_plural = "お問い合わせ一覧"
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.name}様 ({self.submitted_at.strftime('%Y/%m/%d %H:%M')})"
    
    def get_average_score(self):
        """平均評価点を計算"""
        scores = [self.design, self.portfolio, self.dx_ai, self.navigation, self.information, self.overall]
        return sum(scores) / len(scores)


class PortfolioItem(models.Model):
    """作品紹介アイテム"""
    title = models.CharField(max_length=200, verbose_name="作品タイトル")
    description = models.TextField(verbose_name="説明")
    thumbnail = models.ImageField(upload_to='portfolio_images/', verbose_name="サムネイル画像")
    demo_url = models.URLField(blank=True, verbose_name="デモURL", help_text="作品のデモページURL")
    github_url = models.URLField(blank=True, verbose_name="GitHubリポジトリURL")
    technologies = models.CharField(max_length=500, verbose_name="使用技術", help_text="カンマ区切りで入力（例: Python, Django, PostgreSQL）")
    display_order = models.IntegerField(default=0, verbose_name="表示順", help_text="数値が小さいほど上に表示")
    is_published = models.BooleanField(default=True, verbose_name="公開")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    class Meta:
        verbose_name = "作品"
        verbose_name_plural = "作品"
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_tech_list(self):
        """技術タグをリスト形式で取得"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
