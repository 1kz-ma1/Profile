# intro/views.py
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import BlogPost, Category, SubCategory, Section
from .cache_utils import cache_if_anonymous

logger = logging.getLogger(__name__)

@cache_page(60 * 60)  # 1時間キャッシュ
def index(request): 
    return render(request, "index.html")

@cache_page(60 * 60)  # 1時間キャッシュ
def about(request): 
    return render(request, "about.html")

def blog(request):
    # フィルター処理
    posts = BlogPost.objects.filter(is_published=True).prefetch_related('related_posts')
    
    # メインカテゴリフィルター
    main_category_slug = request.GET.get('main_category')
    if main_category_slug:
        posts = posts.filter(main_category__slug=main_category_slug)
    
    # サブカテゴリフィルター
    sub_category_slug = request.GET.get('sub_category')
    if sub_category_slug:
        posts = posts.filter(sub_category__slug=sub_category_slug)
    
    # 旧カテゴリフィルター（後方互換性）
    category = request.GET.get('category')
    if category and not main_category_slug:
        posts = posts.filter(category=category)
    
    # ビュー切り替え用のデータを取得
    view_mode = request.GET.get('view', 'grid')
    
    # ソート処理（章構成ビューの場合はセクション順）
    sort = request.GET.get('sort', '-post_date')
    if view_mode == 'chapters':
        # セクションの表示順、セクション内順序、投稿日順
        posts = posts.order_by('section__order', 'chapter_order', 'chapter_number', 'post_date')
    elif sort == 'oldest':
        posts = posts.order_by('post_date')
    elif sort == 'title':
        posts = posts.order_by('title')
    else:  # newest (default)
        posts = posts.order_by('-post_date')
    
    # ページネーション（1ページに9件）- グリッドビューのみ
    if view_mode == 'grid':
        paginator = Paginator(posts, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        # 章構成・マップビューはページネーションなし
        page_obj = posts
    
    # カテゴリ・セクション情報を取得
    categories = Category.objects.all().prefetch_related('subcategories')
    sections = Section.objects.filter(is_active=True).order_by('order', 'name')
    old_categories = BlogPost.CATEGORY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'all_posts': posts,  # 章構成・マップビュー用
        'categories': categories,
        'sections': sections,  # アクティブなセクション一覧
        'old_categories': old_categories,
        'current_main_category': main_category_slug,
        'current_sub_category': sub_category_slug,
        'current_category': category,
        'current_sort': sort,
        'view_mode': view_mode,
    }
    
    return render(request, "blog.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    return render(request, "blog_detail.html", {'post': post})

@csrf_protect
def like_post(request, pk):
    """ブログ記事に良いねをつける"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    
    # セッションで管理：この記事に良いねしたかどうかチェック
    liked_posts = request.session.get('liked_posts', [])
    
    if pk in liked_posts:
        # 既に良いねしている場合は良いねを取り消す
        liked_posts.remove(pk)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        # 良いねを追加
        liked_posts.append(pk)
        post.likes_count += 1
        liked = True
    
    post.save()
    request.session['liked_posts'] = liked_posts
    
    return JsonResponse({
        'success': True,
        'likes_count': post.likes_count,
        'liked': liked,
    })

def portfolio(request): return render(request, "portfolio.html")
def thanks(request): return render(request, "thanks.html")

@csrf_protect
def contact(request):
    if request.method == "POST":
        # フォーム値を取得
        name = request.POST.get("name", "")
        design = request.POST.get("design", "")
        portfolio = request.POST.get("portfolio", "")
        dx_ai = request.POST.get("dx_ai", "")
        navigation = request.POST.get("navigation", "")
        information = request.POST.get("information", "")
        overall = request.POST.get("overall", "")
        message = request.POST.get("message", "")
        
        # メール本文を作成
        email_body = f"""
お問い合わせフォームからの送信です。

【お名前】
{name}

【サイトの見やすさ・デザイン評価】
{design}点

【作品紹介の作品についての評価】
{portfolio}点

【DX×AIモデル（100年後の東京）の評価】
{dx_ai}点

【ナビゲーションの使いやすさ】
{navigation}点

【情報の分かりやすさ】
{information}点

【全体的な満足度】
{overall}点

【ご意見・ご感想】
{message}

---
このメールはポートフォリオサイトのお問い合わせフォームから自動送信されました。
"""
        
        try:
            # メール送信
            send_mail(
                subject=f'ポートフォリオサイトへのお問い合わせ - {name}様より',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return redirect("intro:thanks")
        except Exception as e:
            # エラーログを記録（本番環境ではログファイルに記録）
            logger.error(f"メール送信エラー: {type(e).__name__}: {str(e)}")
            logger.error(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            logger.error(f"EMAIL_HOST: {settings.EMAIL_HOST}")
            logger.error(f"EMAIL_PORT: {settings.EMAIL_PORT}")
            logger.error(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
            return render(request, "contact.html", {'error': 'メール送信に失敗しました。後ほどお試しください。'})
    
    return render(request, "contact.html")