# 🔍 診断＆修正完了レポート

## 📊 **診断日時**: 2026-01-21

### ✅ **根本原因パターンの診断結果**

| パターン | 状態 | 備考 |
|---------|------|------|
| **A: パッケージ/パス不整合** | ✅ OK | Procfile に `cd` なし・外側/内側 `__init__.py` 存在 |
| **B: Procfile 誤フォーマット** | ⚠️ 修正 | 先頭に空行があった → 削除 |
| **C: release 未実行** | ✅ OK | `release: python manage.py migrate && collectstatic` 設定済み |
| **D: DATABASE_URL 未適用** | ✅ OK | `dj_database_url.config()` で正しく参照 |
| **E: CSRF/Host 不一致** | ⚠️ 修正 | 新ドメイン `web-production-519fa` に合わせて修正 |
| **F: DEBUG 既定値** | ✅ OK | `DEBUG=False` が既定値 |
| **G: Root Directory 不整合** | ✅ OK | Root = repo root、Procfile は cd なし |
| **H: Pre-deploy 書式ミス** | ✅ OK | Procfile 使用、Pre-deploy 不使用 |
| **I: 静的ファイル未収集** | ✅ OK | `collectstatic` を release に含む |

---

## 🛠️ **実施した修正**

### 1️⃣ **Procfile: 先頭空行削除** (パターンB)

**Before:**
```
[空行]
web: gunicorn workpro.wsgi --bind 0.0.0.0:$PORT
```

**After:**
```
web: gunicorn workpro.wsgi --bind 0.0.0.0:$PORT
release: python manage.py migrate && python manage.py collectstatic --noinput
```

### 2️⃣ **settings.py: ALLOWED_HOSTS シンプル化** (パターンE)

**Before:**
```python
default_allowed = ['localhost', '127.0.0.1', '.railway.app', '.vercel.app']
# (複数行の if/for ロジック)
ALLOWED_HOSTS = default_allowed  # ワイルドカード依存
```

**After:**
```python
# 環境変数で設定（本番は具体的なドメイン）
env_allowed = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,.railway.app,.vercel.app')
ALLOWED_HOSTS = [h.strip() for h in env_allowed.split(',') if h.strip()]
```

**本番環境での設定方法:**
```
Railway → web サービス → Variables
ALLOWED_HOSTS = web-production-519fa.up.railway.app,localhost,127.0.0.1
```

### 3️⃣ **settings.py: CSRF_TRUSTED_ORIGINS 修正** (パターンE)

**Before:**
```python
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-519fa.up.railway.app",
    "https://your-portfolio.vercel.app",  # ❌ ダミー
    "http://localhost:3000",
]
```

**After:**
```python
# 末尾スラッシュなし・ワイルドカードなし
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-519fa.up.railway.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### 4️⃣ **settings.py: CORS_ALLOWED_ORIGINS 修正** (パターンE)

**Before:**
```python
CORS_ALLOWED_ORIGINS = [
    'https://*.railway.app',  # ❌ ワイルドカード
    'https://*.vercel.app',   # ❌ ワイルドカード
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

**After:**
```python
# 本番は具体的なドメイン指定
CORS_ALLOWED_ORIGINS = [
    "https://web-production-519fa.up.railway.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## 📋 **次のステップ: 本番デプロイ用チェック**

### ✅ **ローカルテスト**
```bash
# 1. 動作確認
python manage.py runserver

# 2. migrate/collectstatic テスト
python manage.py migrate
python manage.py collectstatic --noinput
```

### ✅ **GitHub プッシュ**
```bash
git add Procfile workpro/settings.py
git commit -m "Fix: Procfile formatting, ALLOWED_HOSTS/CSRF/CORS for web-production-519fa"
git push origin main
```

### ✅ **Railway 環境変数確認 & 設定**

**web サービス → Variables → 以下を確認/設定:**

| Key | Value | 確認 |
|-----|-------|------|
| `DATABASE_URL` | `postgresql://...caboose.proxy.rlwy.net:.../railway` | ✅ |
| `SECRET_KEY` | `django-insecure-...` | ✅ |
| `DEBUG` | `False` | ✅ |
| `ALLOWED_HOSTS` | `web-production-519fa.up.railway.app,localhost,127.0.0.1` | ⬅️ **設定** |

**注意: 前後スペースなし！**

### ✅ **デプロイ実行**

Git push 後、Railway が自動デプロイ開始

**確認項目（Logs）:**
```
Running release command...
Applying admin.0001_initial... OK
Applying auth.0001_initial... OK
...
Collecting static files...
151 static files copied to '...staticfiles'
```

### ✅ **本番環境テスト**

1. **ルート確認**
   ```bash
   curl -I https://web-production-519fa.up.railway.app/
   # HTTP/2 200 or 404 OK
   ```

2. **Admin ページ**
   ```
   https://web-production-519fa.up.railway.app/admin/
   # CSS 正常に読み込まれているか確認
   ```

3. **CSRF 403 が出た場合**
   - ブラウザ: Cookie 削除 + サイトデータ削除
   - `CSRF_TRUSTED_ORIGINS` が新ドメイン `web-production-519fa` に合っているか再確認
   - Railway を再度デプロイ

---

## 🚀 **確認チェックリスト（5分フロー）**

- [ ] Procfile が repo root にあり、先頭に空行なし
- [ ] `python manage.py migrate` ローカルで成功
- [ ] `python manage.py collectstatic --noinput` ローカルで成功
- [ ] GitHub に commit & push 完了
- [ ] Railway **web サービス** → Variables に `ALLOWED_HOSTS` 設定
- [ ] デプロイログで `Applying … OK` と `Collecting static files` を確認
- [ ] `/admin` で CSS 正常表示・ログイン可能
- [ ] 403 が出ないことを確認

---

## 📞 **トラブル時の対応**

### 症状: 502 connection dial timeout
→ **パターンA**: Procfile に `cd` が残っていないか確認

### 症状: 紫の Railway エラー画面
→ **パターンB**: Procfile が正規フォーマットか確認（先頭空白・改行問題）

### 症状: no such table: auth_user
→ **パターンC**: release フェーズが実行されているか Logs で確認

### 症状: 403 CSRF verification failed
→ **パターンE**: ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS が新ドメインか確認・Cookie 削除

---

**修正完了日時**: 2026-01-21
