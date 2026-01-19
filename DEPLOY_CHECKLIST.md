# Railway + Vercel デプロイメント チェックリスト

## ✅ セットアップ完了項目

### バックエンド（Django/Railway）
- [x] Procfile 作成（gunicorn 起動設定）
- [x] runtime.txt 作成（Python 3.11.6 指定）
- [x] .railwayignore 作成（デプロイ対象外ファイル指定）
- [x] settings.py 更新
  - [x] Railway ドメイン対応（.railway.app）
  - [x] CSRF_TRUSTED_ORIGINS 設定
  - [x] CORS 設定
- [x] requirements.txt 更新
- [x] .env.railway テンプレート作成

### フロント（Next.js/Vercel）
- [x] frontend/package.json 作成
- [x] frontend/.eslintrc.json 作成
- [x] frontend/README.md 作成
- [x] frontend/.env.example テンプレート作成

### その他
- [x] 不要なファイル削除（CLOUDFLARE_*.md、RENDER_DEPLOY.md、render.yaml）
- [x] .gitignore 更新
- [x] DEPLOYMENT_GUIDE.md 作成

## 📋 デプロイ前の準備

### 1. GitHub リポジトリへプッシュ
```bash
git add .
git commit -m "Setup for Vercel+Railway deployment"
git push origin main
```

### 2. Railway セットアップ

#### 2.1 Railway プロジェクト作成
- https://railway.app にアクセス
- GitHub でログイン
- 「New Project」→「Deploy from GitHub」選択
- このリポジトリ選択

#### 2.2 環境変数設定（Railway Dashboard）
Railway Dashboard → Project → Variables で以下を設定：

```
SECRET_KEY=django-insecure-生成されたキーを入力
DEBUG=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=Gmail用のアプリパスワード
```

**注意**: `DATABASE_URL` と `RAILWAY_PUBLIC_DOMAIN` は自動設定

#### 2.3 PostgreSQL データベース追加
- Railway Dashboard で「+ New」→「Database」→「PostgreSQL」
- 自動で `DATABASE_URL` が環境変数に追加される

#### 2.4 デプロイ実行
Railway が自動的にデプロイを開始（約2-5分）

### 3. Vercel セットアップ

#### 3.1 Vercel プロジェクト作成
- https://vercel.com にアクセス
- GitHub でログイン
- 「Add New」→「Project」選択
- このリポジトリ選択

#### 3.2 デプロイ設定
- Root Directory: `frontend` に設定

#### 3.3 環境変数設定
Vercel Dashboard → Settings → Environment Variables で：

```
NEXT_PUBLIC_API_URL=https://your-railway-domain.railway.app
```

**注意**: Railway のデプロイ完了後のドメインを確認してから設定してください

#### 3.4 デプロイ実行
Vercel が自動的にデプロイを開始（約1-2分）

## 🔗 デプロイ後の確認

### 1. Railway ドメイン確認
- Railway Dashboard → Project → Deployments
- 「Your Application」セクションでドメイン確認

### 2. Vercel ドメイン確認
- Vercel Dashboard → Deployments
- 「Production」のドメイン確認

### 3. API 接続確認
ブラウザで以下にアクセス：
```
https://your-vercel-domain.vercel.app
```

コンソールエラーがないか確認

### 4. API 動作確認
```bash
curl https://your-railway-domain.railway.app/api/
```

### 5. Django Admin アクセス
```
https://your-railway-domain.railway.app/admin/
```

## ⚠️ よくあるエラー

### CORS エラー
**症状**: ブラウザのコンソールに `Access-Control-Allow-Origin` エラー

**対策**:
1. Railway の環境変数 `ALLOWED_HOSTS` を確認
2. Django settings.py の `CORS_TRUSTED_ORIGINS` を確認
3. Railway を再デプロイ

### 静的ファイル 404
**症状**: CSS/JS が読み込まれない

**対策**:
1. Railway の Procfile に `release: python manage.py collectstatic --noinput` を追加
2. Railway を再デプロイ

### データベース接続エラー
**症状**: `django.db.utils.OperationalError`

**対策**:
1. Railway Dashboard で PostgreSQL が起動しているか確認
2. `DATABASE_URL` 環境変数が正しく設定されているか確認
3. Railway を再デプロイ

## 🚀 今後のデプロイ

### バックエンド更新時
```bash
# ローカルで動作確認
python manage.py runserver

# GitHub にプッシュ
git add .
git commit -m "Update backend"
git push origin main

# Railway が自動でデプロイ
```

### フロント更新時
```bash
# ローカルで動作確認
cd frontend
npm run dev

# GitHub にプッシュ
git add .
git commit -m "Update frontend"
git push origin main

# Vercel が自動でデプロイ
```

## 📞 サポート

- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
