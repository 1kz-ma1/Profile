# Railway 本番環境用 環境変数 - 実装チェックリスト

## 🔐 必須環境変数の確認手順

### 1. SECRET_KEY の生成と設定

**ローカルで生成:**
```bash
python generate_secret_key.py
```

**出力例:**
```
Generated SECRET_KEY:
django-insecure-abc123xyz...
```

**Railroad Dashboard への設定:**
- Railway.app にアクセス → Project 選択
- Settings → Variables
- 「Add Variable」をクリック
- **Key**: `xrw@pbg35nm6*ir4s^0&1s2e^*cp6w3er45imb%8fn54acxn!b`
- **Value**: 上記で生成した値をペースト
- 保存 → Deployment が自動トリガー

---

### 2. DEBUG = False（本番環境での必須設定）

**設定内容:**
- **Key**: `DEBUG`
- **Value**: `False`
- 保存

---

### 3. ALLOWED_HOSTS（Railway 公開ドメイン）

Railway デプロイ後、自動的に以下の形式でドメイン割り当てられます:
```
https://web-production-91779.up.railway.app/
```

または Railway dashboard で確認:
- Railway Dashboard → Deployment → URL を確認

**設定内容:**
- **Key**: `ALLOWED_HOSTS`
- **Value**: `your-domain.up.railway.app,localhost,127.0.0.1`
- 保存

---

### 4. DATABASE_URL（PostgreSQL 自動設定）

**PostgreSQL サービスの追加:**
1. Railway Dashboard → Project → 「+ New」
2. Database → PostgreSQL を選択
3. 自動作成後、環境変数に `DATABASE_URL` が自動追加される

**確認方法:**
- Railway Dashboard → Variables で `DATABASE_URL` の値を確認
- 形式: `postgresql://user:password@host:port/dbname`

---

### 5. スーパーユーザー自動作成（初回のみ）

**目的**: Shell が使えない Railway 新UI で、スーパーユーザーを作成するための代替手段

**流れ:**
1. 環境変数を一時的に設定
2. デプロイ実行（Procfile の release フックで自動作成）
3. ユーザー確認（/admin でログイン）
4. 環境変数を削除

**設定内容:**

| Key | Value | 説明 |
|-----|-------|------|
| `DJANGO_SUPERUSER_USERNAME` | `admin` | スーパーユーザー名 |
| `DJANGO_SUPERUSER_EMAIL` | `admin@example.com` | メールアドレス |
| `DJANGO_SUPERUSER_PASSWORD` | `TempPass123!` | 一時パスワード（複雑に） |

**Procfile での実行:**

Procfile は以下のコマンドを `release` フェーズで実行:
```bash
python manage.py migrate && \
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 2>/dev/null || true && \
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').first(); u.set_password('$DJANGO_SUPERUSER_PASSWORD'); u.save() if u else None" 2>/dev/null || true && \
python manage.py collectstatic --noinput
```

（実際には `Procfile` を編集で詳細指示あり）

---

### 6. メール設定（オプション）

コンタクト機能がある場合、Gmail で設定:

1. [Google アカウント設定](https://myaccount.google.com/security)
2. 「2段階認証」を有効化
3. 「アプリパスワード」を生成（メール用）

**設定内容:**

| Key | Value |
|-----|-------|
| `EMAIL_HOST_USER` | あなたの Gmail アドレス |
| `EMAIL_HOST_PASSWORD` | 生成したアプリパスワード（16 文字） |

---

### 7. SSL/Security（本番推奨）

HTTPS を強制し、セキュリティを向上:

| Key | Value |
|-----|-------|
| `SECURE_SSL_REDIRECT` | `True` |
| `SECURE_HSTS_SECONDS` | `31536000` |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | `True` |
| `SECURE_HSTS_PRELOAD` | `True` |

---

## 🔄 デプロイ実行フロー

```
1. SECRET_KEY 生成 → Variable 設定
   ↓
2. DEBUG = False 設定
   ↓
3. ALLOWED_HOSTS に Railway ドメイン設定
   ↓
4. PostgreSQL サービス追加（DATABASE_URL 自動化）
   ↓
5. DJANGO_SUPERUSER_* 一時設定
   ↓
6. Deploy トリガー（自動デプロイ開始）
   ↓
7. Logs で migrate/collectstatic/createsuperuser 成功を確認
   ↓
8. /admin でスーパーユーザーでログイン確認
   ↓
9. DJANGO_SUPERUSER_* を Variables から削除
   ↓
10. 再度デプロイ（環境変数削除を反映）
```

---

## ⚠️ よくあるトラブル

### エラー: `DJANGO_SUPERUSER_* で createsuperuser 失敗`

**原因**: ユーザーがすでに存在する場合

**対策**: Procfile の `createsuperuser` コマンドに `2>/dev/null || true` を末尾に追加（既に実装予定）

### エラー: `Database connection error`

**確認**:
1. PostgreSQL サービスが Railway で「Deploy in progress」でないか
2. `DATABASE_URL` が Variable に存在するか
3. `conn_max_age=600` の設定が settings.py にあるか

---

## 📞 次のステップ

- ステップ 3: migrate/collectstatic の実行方針
