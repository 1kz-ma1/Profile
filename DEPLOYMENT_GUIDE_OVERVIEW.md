# 📚 Vercel + Railway デプロイメント ドキュメント体系

> このフォルダには、Vercel（フロント）+ Railway（Django バックエンド）で自己紹介サイトを本番公開するための**完全なセットアップガイド**が含まれています。

---

## 📖 ドキュメント一覧

### 📌 **このファイル**
- **DEPLOYMENT_GUIDE_OVERVIEW.md** ← あなたはここです

---

### 🔧 **ステップ別ガイド**

#### ステップ 1: Django 設定確認
**ファイル**: `DEPLOYMENT_GUIDE.md`
- Django settings.py の確認ポイント
- SECRET_KEY、DEBUG、ALLOWED_HOSTS の設定状態確認
- CSRF_TRUSTED_ORIGINS と CORS の確認

#### ステップ 2: Railway 環境変数設定
**ファイル**: `RAILWAY_ENV_SETUP.md`、`RAILWAY_ENV_TEMPLATE.py`
- Railway に設定すべき環境変数の一覧
- スーパーユーザー自動作成の仕組み
- PostgreSQL の設定方法

#### ステップ 3: migrate/collectstatic の実行
**ファイル**: `RAILWAY_DEPLOY_PROCEDURE.md`
- Shell が使えない Railway 新 UI での対応方法
- Procfile の release フェーズの説明
- Deploy Hooks の場所と設定方法

#### ステップ 4: Vercel フロント設定
**ファイル**: `VERCEL_SETUP_GUIDE.md`
- Vercel プロジェクト作成手順
- 環境変数設定（NEXT_PUBLIC_API_BASE）
- API クライアント実装のサンプルコード
- CORS/CSRF エラーの切り分け方法

#### ステップ 5: 疎通検証
**ファイル**: `VERIFICATION_PROCEDURE.md`
- 5ステップの検証フロー
  1. Railway ルート疎通
  2. Django Admin 表示確認
  3. API エンドポイント確認
  4. Vercel からのリクエスト確認
  5. 本番ドメイン固定化

#### ステップ 6: 最終チェック
**ファイル**: `FINAL_CHECKLIST.md`
- デプロイ前チェック（ローカル）
- Railway デプロイチェック
- Vercel デプロイチェック
- CORS/CSRF チェック
- セキュリティチェック
- パフォーマンスチェック
- 本番リリースチェック

---

### 📋 **設定ファイル**

| ファイル | 説明 |
|---------|------|
| `Procfile` | Railway 用デプロイスクリプト（migrate・collectstatic・createsuperuser） |
| `runtime.txt` | Python バージョン指定（3.11.6） |
| `.railwayignore` | Railway デプロイ対象外ファイル |
| `.env.railway` | Railway 環境変数テンプレート（実装見本） |
| `requirements.txt` | Python 依存パッケージ |
| `workpro/settings.py` | Django 設定（CSRF・CORS・static files） |

### 🖥️ **フロントエンド**

| ファイル | 説明 |
|---------|------|
| `frontend/package.json` | Next.js プロジェクト設定 |
| `frontend/.env.example` | フロント環境変数テンプレート |
| `frontend/README.md` | フロント側セットアップガイド |

---

## 🚀 **クイックスタート**

### 1️⃣ **ローカルテスト**（5分）
```bash
# バックエンド
python generate_secret_key.py
python manage.py runserver

# フロント
cd frontend
npm install
npm run dev
```

### 2️⃣ **Railway にプッシュ**（1分）
```bash
git add .
git commit -m "Setup for production"
git push origin main
```

### 3️⃣ **Railway 設定**（5分）
1. Railway.app にログイン
2. Project → Variables → 環境変数を設定
3. PostgreSQL サービス追加
4. Deployment トリガー（自動デプロイ開始）

### 4️⃣ **Vercel 設定**（5分）
1. Vercel.app にログイン
2. Project → Settings → Environment Variables
3. `NEXT_PUBLIC_API_BASE` に Railway URL を設定
4. Deployment トリガー（自動デプロイ開始）

### 5️⃣ **疎通確認**（5分）
```bash
# Railway ルート確認
curl https://your-domain.up.railway.app/

# API 確認
curl https://your-domain.up.railway.app/api/posts/

# Vercel でコンソール確認
fetch(process.env.NEXT_PUBLIC_API_BASE + '/api/posts/')
```

---

## 📊 **ファイルツリー**

```
workpro/
├── DEPLOYMENT_GUIDE.md          # ← Step 1
├── RAILWAY_ENV_SETUP.md         # ← Step 2
├── RAILWAY_ENV_TEMPLATE.py      # 環境変数テンプレート
├── RAILWAY_DEPLOY_PROCEDURE.md  # ← Step 3
├── VERCEL_SETUP_GUIDE.md        # ← Step 4
├── VERIFICATION_PROCEDURE.md    # ← Step 5
├── FINAL_CHECKLIST.md           # ← Step 6
├── Procfile                     # Railway デプロイスクリプト
├── runtime.txt                  # Python バージョン
├── .railwayignore               # Railroad 対象外ファイル
├── .env.railway                 # 環境変数テンプレート
├── requirements.txt             # Python 依存パッケージ
├── manage.py
├── workpro/
│   ├── settings.py              # Django 設定（✅ 完成）
│   ├── urls.py
│   └── wsgi.py
├── frontend/
│   ├── package.json
│   ├── .env.example
│   └── README.md
├── intro/                       # Django アプリ
│   ├── static/                  # 静的ファイル
│   ├── templates/               # Django テンプレート
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── media/                       # ユーザーアップロード
```

---

## 🎯 **目的別読むべきドキュメント**

### 🔍 「Django 設定ってちゃんとできてるの？」
→ **DEPLOYMENT_GUIDE.md** の「Django 側の設定確認」を読む

### 🚀 「Railway に何を設定すればいい？」
→ **RAILWAY_ENV_SETUP.md** + **RAILWAY_DEPLOY_PROCEDURE.md** を読む

### 🖥️「Vercel の設定は？」
→ **VERCEL_SETUP_GUIDE.md** を読む

### 🔗 「CORS/CSRF エラーが出た…」
→ **VERCEL_SETUP_GUIDE.md** の「CORS/CSRF エラー切り分け」セクション

### ✅「いつリリースしていい？」
→ **FINAL_CHECKLIST.md** の全項目に ✅ を入れたら OK

---

## 🔐 **セキュリティ確認事項**

- [ ] SECRET_KEY が環境変数化されている（ソースに含まない）
- [ ] DEBUG = False（本番環境）
- [ ] ALLOWED_HOSTS がワイルドカードではなく具体的なドメイン
- [ ] CSRF_TRUSTED_ORIGINS がワイルドカードではなく具体的なドメイン
- [ ] DJANGO_SUPERUSER_* が初回デプロイ後に削除されている
- [ ] HTTPS でアクセス可能

---

## 🛠️ **トラブルシューティングマップ**

| 問題 | ドキュメント | セクション |
|------|-----------|----------|
| Django 設定がわからない | DEPLOYMENT_GUIDE.md | Django 側の設定確認 |
| Railway デプロイ失敗 | RAILWAY_DEPLOY_PROCEDURE.md | トラブルシューティング |
| CORS エラー | VERCEL_SETUP_GUIDE.md | CORS/CSRF エラー切り分け |
| Static files 404 | RAILWAY_DEPLOY_PROCEDURE.md | Static files 404 対策 |
| API 疎通しない | VERIFICATION_PROCEDURE.md | ④ Vercel からのリクエスト |
| 本番化の準備 | FINAL_CHECKLIST.md | 本番環境リリースチェック |

---

## 📞 **次のステップ**

1. **DEPLOYMENT_GUIDE.md** を読んで Django 設定を確認
2. **RAILWAY_ENV_SETUP.md** で環境変数を準備
3. **RAILWAY_DEPLOY_PROCEDURE.md** に従ってデプロイ
4. **VERCEL_SETUP_GUIDE.md** で Vercel を設定
5. **VERIFICATION_PROCEDURE.md** で疎通確認
6. **FINAL_CHECKLIST.md** で本番リリース判定

---

## 📚 **外部リンク**

- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [CORS MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

**作成日**: 2026年1月19日  
**更新**: Rails 新 UI（Shell/Start Command 非対応）対応版

