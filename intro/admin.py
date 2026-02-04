from django.contrib import admin
from django.conf import settings
from .models import BlogPost, Category, SubCategory, Section, ContactFormSubmission, PortfolioItem
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

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('icon_name', 'name', 'order', 'get_post_count', 'is_active', 'updated_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    readonly_fields = ('created_at', 'updated_at', 'get_post_count')
    
    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'icon', 'order', 'is_active')
        }),
        ('詳細', {
            'fields': ('description',)
        }),
        ('統計情報', {
            'fields': ('get_post_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def icon_name(self, obj):
        """アイコン付きの名前を表示"""
        return str(obj)
    icon_name.short_description = 'セクション'
    
    actions = ['activate_sections', 'deactivate_sections']
    
    def activate_sections(self, request, queryset):
        """選択したセクションを有効化"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count}個のセクションを有効化しました。')
    activate_sections.short_description = '選択したセクションを有効化'
    
    def deactivate_sections(self, request, queryset):
        """選択したセクションを無効化"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count}個のセクションを無効化しました。')
    deactivate_sections.short_description = '選択したセクションを無効化'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category_info', 'get_section_info', 'likes_count', 'post_date', 'is_published')
    list_filter = ('is_published', 'section', 'main_category', 'sub_category', 'post_date')
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
    
    def get_section_info(self, obj):
        """セクション情報を表示"""
        if obj.section:
            return str(obj.section)
        if obj.chapter_title:
            return f"（旧）{obj.chapter_title}"
        if obj.chapter_number:
            return f"（旧）第{obj.chapter_number}章"
        return "未設定"
    get_section_info.short_description = "セクション"
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'post_date', 'is_published')
        }),
        ('カテゴリ', {
            'fields': ('main_category', 'sub_category', 'category'),
            'description': '新しいカテゴリシステム（main_category/sub_category）を使用してください。旧categoryフィールドは後方互換性のために残されています。'
        }),
        ('セクション設定', {
            'fields': ('section', 'chapter_order'),
            'description': 'セクションを選択してください。章構成ビューでのグループ分けに使用されます。'
        }),
        ('ビュー切り替え用設定（旧）', {
            'fields': ('chapter_title', 'chapter_number', 'field_tags', 'related_posts'),
            'classes': ('collapse',),
            'description': '章構成ビューと相関図ビューで使用する設定です。セクション名を自由に入力できます（例: 資格、技術、プロジェクトなど）。'
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


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted_at', 'get_average_score_display', 'design', 'portfolio', 'dx_ai', 'navigation', 'information', 'overall')
    list_filter = ('submitted_at', 'design', 'overall')
    search_fields = ('name', 'message', 'ip_address')
    readonly_fields = ('name', 'design', 'portfolio', 'dx_ai', 'navigation', 'information', 'overall', 'message', 'submitted_at', 'ip_address', 'user_agent', 'get_average_score_display')
    ordering = ('-submitted_at',)
    
    fieldsets = (
        ('送信者情報', {
            'fields': ('name', 'submitted_at', 'ip_address', 'user_agent')
        }),
        ('評価内容', {
            'fields': ('design', 'portfolio', 'dx_ai', 'navigation', 'information', 'overall', 'get_average_score_display')
        }),
        ('ご意見・ご感想', {
            'fields': ('message',)
        }),
    )
    
    def get_average_score_display(self, obj):
        """平均評価点を表示"""
        return f"{obj.get_average_score():.1f}点"
    get_average_score_display.short_description = '平均評価'
    
    def has_add_permission(self, request):
        """管理画面からの新規追加を無効化"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """管理画面からの編集を無効化（閲覧のみ）"""
        return False


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'display_order', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('is_published', 'display_order')
    ordering = ('display_order', '-created_at')
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'description', 'thumbnail')
        }),
        ('リンク', {
            'fields': ('demo_url', 'github_url')
        }),
        ('技術・設定', {
            'fields': ('technologies', 'display_order', 'is_published')
        }),
    )
