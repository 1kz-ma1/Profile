#!/usr/bin/env python
"""
Railroad 本番環境用 環境変数 テンプレート

以下の値を Railway Dashboard → Variables に設定してください。
DATABASE_URL は Railway PostgreSQL 自動設定のため、ここでは記載不要です。
"""

# =====================================================
# === 必須設定 ===
# =====================================================

# Django セキュリティ
SECRET_KEY = "django-insecure-xxxxx..."  # python generate_secret_key.py で生成
DEBUG = "False"  # 本番は必ず False

# ホスト設定
# 値例: my-project.up.railway.app
ALLOWED_HOSTS = "my-project.up.railway.app,localhost"

# =====================================================
# === Optional: メール設定 ===
# =====================================================

EMAIL_HOST_USER = "your-email@gmail.com"
EMAIL_HOST_PASSWORD = "your-gmail-app-password"  # Gmail アプリパスワード

# =====================================================
# === Optional: SSL/Security（本番環境推奨） ===
# =====================================================

SECURE_SSL_REDIRECT = "True"
SECURE_HSTS_SECONDS = "31536000"
SECURE_HSTS_INCLUDE_SUBDOMAINS = "True"
SECURE_HSTS_PRELOAD = "True"

# =====================================================
# === スーパーユーザー自動作成（初回デプロイ時のみ） ===
# =====================================================
# 注意: デプロイ後、すぐに削除してください。

DJANGO_SUPERUSER_USERNAME = "admin"
DJANGO_SUPERUSER_EMAIL = "admin@example.com"
DJANGO_SUPERUSER_PASSWORD = "secure-temporary-password-12345"

# =====================================================
# === DATABASE_URL（自動設定、手動入力不要） ===
# =====================================================
# Railway が PostgreSQL サービス追加時に自動設定します
# 確認: Railway Dashboard → Variables の DATABASE_URL を確認

# DATABASE_URL = postgresql://user:password@db.railway.internal:5432/railway
