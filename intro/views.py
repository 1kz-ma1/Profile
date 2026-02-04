# intro/views.py
import logging
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import BlogPost, Category, SubCategory, Section, ContactFormSubmission, PortfolioItem
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

def portfolio(request):
    items = PortfolioItem.objects.filter(is_published=True)
    return render(request, "portfolio.html", {'items': items})
def thanks(request): return render(request, "thanks.html")

@csrf_protect
def contact(request):
    if request.method == "POST":
        # フォーム値を取得
        name = request.POST.get("name", "")
        design = request.POST.get("design", 0)
        portfolio = request.POST.get("portfolio", 0)
        dx_ai = request.POST.get("dx_ai", 0)
        navigation = request.POST.get("navigation", 0)
        information = request.POST.get("information", 0)
        overall = request.POST.get("overall", 0)
        message = request.POST.get("message", "")
        
        try:
            # IPアドレスとユーザーエージェントを取得
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            if ip_address:
                ip_address = ip_address.split(',')[0].strip()
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # データベースに保存
            submission = ContactFormSubmission.objects.create(
                name=name,
                design=int(design) if design else 0,
                portfolio=int(portfolio) if portfolio else 0,
                dx_ai=int(dx_ai) if dx_ai else 0,
                navigation=int(navigation) if navigation else 0,
                information=int(information) if information else 0,
                overall=int(overall) if overall else 0,
                message=message,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            logger.info(f"お問い合わせ受信: {name}様 (ID: {submission.id}, 平均評価: {submission.get_average_score():.1f}点)")
            return redirect("intro:thanks")
            
        except Exception as e:
            # エラーログを記録
            import traceback
            logger.error(f"お問い合わせ保存エラー: {type(e).__name__}: {str(e)}")
            logger.error(f"詳細トレースバック:\n{traceback.format_exc()}")
            return render(request, "contact.html", {'error': 'お問い合わせの送信に失敗しました。もう一度お試しください。'})
    
    return render(request, "contact.html")