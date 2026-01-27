# intro/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost
from .cache_utils import cache_if_anonymous

@cache_page(60 * 60)  # 1時間キャッシュ
def index(request): 
    return render(request, "index.html")

@cache_page(60 * 60)  # 1時間キャッシュ
def about(request): 
    return render(request, "about.html")

def blog(request):
    # フィルター処理
    posts = BlogPost.objects.filter(is_published=True)
    
    # カテゴリフィルター
    category = request.GET.get('category')
    if category:
        posts = posts.filter(category=category)
    
    # ソート処理
    sort = request.GET.get('sort', '-post_date')
    if sort == 'oldest':
        posts = posts.order_by('post_date')
    elif sort == 'title':
        posts = posts.order_by('title')
    else:  # newest (default)
        posts = posts.order_by('-post_date')
    
    # ページネーション（1ページに9件）
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # カテゴリ選択肢を取得
    categories = BlogPost.CATEGORY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
    }
    
    return render(request, "blog.html", context)

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    return render(request, "blog_detail.html", {'post': post})

def portfolio(request): return render(request, "portfolio.html")
def thanks(request): return render(request, "thanks.html")

@csrf_protect
def contact(request):
    if request.method == "POST":
        # フォーム値を取得
        name = request.POST.get("name", "")
        design = request.POST.get("design", "")
        portfolio = request.POST.get("portfolio", "")
        skills = request.POST.get("skills", "")
        impression = request.POST.get("impression", "")
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

【技術スキル紹介の評価】
{skills}点

【全体的な印象】
{impression}点

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
            print(f"メール送信エラー: {e}")
            return render(request, "contact.html", {'error': 'メール送信に失敗しました。後ほどお試しください。'})
    
    return render(request, "contact.html")