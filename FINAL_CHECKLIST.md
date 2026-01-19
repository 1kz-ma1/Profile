# Vercel + Railway 本番環境 最終チェックリスト

## 🚀 デプロイ前チェック（ローカル）

### Django/Backend

- [ ] `python generate_secret_key.py` を実行して SECRET_KEY を取得
- [ ] `.env.railway` に実際の値が記入されているか確認（テンプレートではなく）
- [ ] `python manage.py runserver` でローカルが起動するか確認
- [ ] `python manage.py migrate` でマイグレーション成功
- [ ] `python manage.py collectstatic --noinput` で static ファイル収集成功
- [ ] requirements.txt に全ての必須パッケージが列記されているか確認
- [ ] Procfile の `release` コマンドが正しく記述されているか確認

### Frontend

- [ ] `cd frontend && npm install` が成功するか確認
- [ ] `.env.example` に `NEXT_PUBLIC_API_BASE` が記入されているか確認
- [ ] `npm run dev` でローカル開発サーバー起動確認

---

## 🔌 Railway デプロイチェック

### 環境変数設定

- [ ] `SECRET_KEY` が設定されている（`django-insecure-` で始まる長い文字列）
- [ ] `DEBUG = False` に設定されている
- [ ] `ALLOWED_HOSTS` に Railway ドメインが設定されている
  - 例: `my-app.up.railway.app`
- [ ] PostgreSQL サービスが追加されて `DATABASE_URL` が自動生成されている

### スーパーユーザー設定（初回のみ）

- [ ] `DJANGO_SUPERUSER_USERNAME` が設定されている（例: `admin`）
- [ ] `DJANGO_SUPERUSER_EMAIL` が設定されている
- [ ] `DJANGO_SUPERUSER_PASSWORD` が設定されている（複雑なパスワード）

### デプロイ実行

- [ ] GitHub にプッシュしてから、Railway が自動デプロイ開始
- [ ] Railway Logs で以下を確認:
  ```
  Running release command...
  Operations to perform:
    Apply all migrations: ...
  ✅ Password set for admin
  Collecting static files...
  ```

### 動作確認

- [ ] `https://your-domain.up.railway.app/admin/` にアクセス
- [ ] スーパーユーザーでログイン可能（ユーザー名: `admin`、パスワード: 設定値）
- [ ] Admin ページの CSS が正しく読み込まれている
- [ ] API エンドポイント `https://your-domain.up.railway.app/api/posts/` で JSON 応答確認

### セキュリティ対応

- [ ] Django で `/admin/` にアクセスしてスーパーユーザーパスワードを新しいものに変更
- [ ] Railway Variables から以下を削除（セキュリティ）:
  - `DJANGO_SUPERUSER_USERNAME`
  - `DJANGO_SUPERUSER_EMAIL`
  - `DJANGO_SUPERUSER_PASSWORD`
- [ ] Railway を再度デプロイして削除を反映

---

## 🖥️ Vercel デプロイチェック

### プロジェクト設定

- [ ] Vercel Dashboard で Root Directory が `frontend/` に設定されている
- [ ] ビルドコマンド: `npm install && npm run build`
- [ ] 出力ディレクトリ: `.next`

### 環境変数設定

- [ ] `NEXT_PUBLIC_API_BASE` に Railway 本番URL が設定されている
  - 例: `https://my-app.up.railway.app`

### デプロイ実行

- [ ] GitHub にプッシュしてから、Vercel が自動デプロイ開始
- [ ] Vercel Deployments で ✅ Deployment successful を確認

### 動作確認

- [ ] Vercel Production URL で HTTP 200 が返る
- [ ] ブラウザでページが表示される
- [ ] 開発者ツール → Console でエラーがないか確認
- [ ] ページ内で API データが表示されている

---

## 🔗 CORS/CSRF チェック

### Django 側

- [ ] settings.py で `CSRF_TRUSTED_ORIGINS` に Vercel ドメインが含まれている:
  ```python
  CSRF_TRUSTED_ORIGINS = [
      'https://your-domain.vercel.app',  # ← 本番 Vercel URL
      'https://your-domain.up.railway.app',  # ← Railway 本番 URL
  ]
  ```
- [ ] `CORS_ALLOWED_ORIGINS` にも同様に含まれている

### Vercel 側（ブラウザでの確認）

- [ ] ブラウザコンソール（F12 → Console）で CORS エラーがない
- [ ] Network タブで API リクエストが 200 で返っている
- [ ] Response Headers に `Access-Control-Allow-Origin` が含まれている

---

## 📧 メール機能チェック（オプション）

- [ ] Railway Variables に以下が設定されている（メール機能がある場合）:
  - `EMAIL_HOST_USER`: Gmail アドレス
  - `EMAIL_HOST_PASSWORD`: Gmail アプリパスワード
- [ ] コンタクトフォームがある場合、テストメール送信可能か確認

---

## 🛡️ セキュリティチェック（本番化前）

### HTTPS

- [ ] `https://` でアクセス可能か確認
- [ ] ブラウザに「保護されている」と表示されるか確認

### Secret Key

- [ ] SECRET_KEY が環境変数化されているか確認
- [ ] ソースコード内にハードコードされていないか確認

### DEBUG

- [ ] Django DEBUG が `False` に設定されているか確認
- [ ] エラーページがデバッグ情報を表示していないか確認

### ALLOWED_HOSTS

- [ ] 本番化時にワイルドカードを外して、具体的なドメインのみ許可
  - ❌ `ALLOWED_HOSTS = ['.railway.app']`
  - ✅ `ALLOWED_HOSTS = ['my-app.up.railway.app']`

### CSRF_TRUSTED_ORIGINS

- [ ] 本番化時にワイルドカードを外して、具体的なドメインのみ許可
  - ❌ `CSRF_TRUSTED_ORIGINS = ['https://*.vercel.app']`
  - ✅ `CSRF_TRUSTED_ORIGINS = ['https://my-domain.vercel.app']`

---

## 📊 パフォーマンスチェック

- [ ] Vercel Deployment Analytics で LCP/FID/CLS を確認
- [ ] Railway Monitoring で CPU/Memory の使用率を確認
- [ ] API レスポンス時間が許容範囲か確認（<500ms 推奨）

---

## ✅ 本番環境リリースチェック

すべてのチェック項目に ✅ が入ったら本番運用開始

### リリース作業

- [ ] GitHub の `main` ブランチが最新状態か確認
- [ ] Railway と Vercel Deployments が最新の状態か確認
- [ ] 社内テストユーザーで最終動作確認
- [ ] 公開予定日時をテスト済みと確認

### ドメイン（カスタム）の設定

- [ ] 独自ドメインを Railway に設定（オプション）
  - Railway Dashboard → Custom Domain
- [ ] 独自ドメインを Vercel に設定（オプション）
  - Vercel Dashboard → Project Settings → Domains

---

## 🚨 本番トラブル時の対応

### エラーが発生した場合

| 症状 | 確認項目 | 対策 |
|------|--------|------|
| ページが表示されない（Railway 500） | Railway Logs で error 確認 | ERROR 行を確認して修正 → git push |
| API が CORS エラー | Network tab で response header 確認 | CSRF_TRUSTED_ORIGINS 設定確認 → Railway 再デプロイ |
| Static files が 404 | collectstatic ログ確認 | STATIC_ROOT/STATICFILES_DIRS 確認 → Railway 再デプロイ |
| DB 接続エラー | DATABASE_URL environment variable 確認 | PostgreSQL サービス起動確認 |

### ロールバック

- [ ] GitHub の前のコミットに戻す
  ```bash
  git revert HEAD
  git push origin main
  ```
- [ ] Railway/Vercel が自動デプロイして復旧

---

## 📞 サポート情報

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **CORS Issues**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

---

## 🎯 チェックリスト完了

✅ 全項目確認済み → **本番環境リリース可能**

🚀 お疲れ様でした！
