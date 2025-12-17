# Cloudflareキャッシング最適化ユーティリティ
# intro/cache_utils.py

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.http import condition
from django.views.generic import View
from functools import wraps
import hashlib


def cloudflare_cache(timeout=3600, key_prefix=None):
    """
    Cloudflareキャッシング対応デコレータ
    
    使用例:
        @cloudflare_cache(timeout=3600)  # 1時間
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            response = cache_page(timeout)(view_func)(request, *args, **kwargs)
            # Cloudflare向けのキャッシュヘッダーを追加
            response['Cache-Control'] = f'public, max-age={timeout}'
            if key_prefix:
                response['X-Cache-Key'] = key_prefix
            return response
        return wrapped_view
    return decorator


def cache_if_anonymous(timeout=3600):
    """
    アノニマスユーザーのみキャッシュ
    ログイン中のユーザーはキャッシュしない
    
    使用例:
        @cache_if_anonymous(timeout=7200)  # 2時間
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # ログイン中はキャッシュしない
                response = view_func(request, *args, **kwargs)
                response['Cache-Control'] = 'private, no-cache'
                return response
            else:
                # アノニマスユーザーはキャッシュ
                return cache_page(timeout)(view_func)(request, *args, **kwargs)
        return wrapped_view
    return decorator


class CloudflareCachedView(View):
    """Cloudflare対応キャッシュビュー基底クラス"""
    cache_timeout = 3600  # デフォルト1時間
    
    @method_decorator(cache_page(cache_timeout))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
