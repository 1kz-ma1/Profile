# Railway デプロイ手順（新 UI）

## 環境変数なし Shell/Start Command が使える UI の場合の対応

### パターン A：Deploy Hooks が使える UI（推奨）

**UI 遷移:**
1. Railway.app → Project 選択
2. Settings タブ → 「Deploy」セクション
3. 「Pre-Deploy Command」または「Deploy Hooks」を探す

**見つからない場合の遷移:**
- Settings → Deploy → Environment → Variables
- または Settings → Integrations → GitHub
- または左サイドバー → Deployments

---

### パターン B：Deploy Hooks が見つからない場合（新 UI）

#### 対応 1: Environment を新規作成して Shell を有効化

**手順:**

1. **新しい Environment を作成**
   - Settings → Environments → 「+ New」
   - Environment 名: `production` または `prod`
   - Save

2. **Deploy Webhook を設定**
   - その Environment の Deploy → Services
   - 「Run Command」→ 「Pre-Deployment」
   - コマンド:
     ```bash
     python manage.py migrate && python manage.py collectstatic --noinput
     ```

3. 成功したら、GitHub から main に Push すると自動デプロイ

---

### パターン C：それでも Shell が出ない場合（代替手段）

**方法 1: Procfile の release フェーズで実行（現在の実装）**

上記で実装した Procfile の `release:` コマンドが実行される。

確認方法:
- Railway Dashboard → Deployments → 「Latest」
- Logs で以下の出力を確認:
  ```
  Running release command...
  ✅ Password set for admin
  ```

**方法 2: Render へバックエンド移行（最後の手段）**

もし Railway で完全に不可な場合は、Render.com への移行を検討。
（ただし、Procfile の release フェーズでは十分対応可能）

---

## 📋 本番環境での実際の流れ

### ① 初回デプロイ（スーパーユーザー作成込み）

1. **ローカルで SECRET_KEY 生成**
   ```bash
   python generate_secret_key.py
   ```

2. **Railway 環境変数を設定**
   - Railway Dashboard → Project → Variables → Add Variable
   
   以下を設定:
   ```
   SECRET_KEY           = (生成した値)
   DEBUG                = False
   ALLOWED_HOSTS        = (your-domain.up.railway.app)
   DJANGO_SUPERUSER_USERNAME = admin
   DJANGO_SUPERUSER_EMAIL    = admin@example.com
   DJANGO_SUPERUSER_PASSWORD = TempPass123!
   ```

3. **PostgreSQL サービスを追加**
   - Railway Dashboard → Project → 「+ New」
   - Database → PostgreSQL
   - 自動作成後、DATABASE_URL が Variable に追加される

4. **Deployment トリガー**
   - GitHub main に `Procfile` の変更をプッシュ
   - Railway が自動デプロイ開始

5. **Logs で確認**
   - Railway Dashboard → Deployments → 「Latest」
   - Logs タブで以下を確認:
     ```
     Running release command...
     Operations to perform:
       Apply all migrations: ...
     ✅ Password set for admin
     Collecting static files...
     ```

6. **本番環境で動作確認**
   - アクセス: `https://your-domain.up.railway.app/admin/`
   - ユーザー名: `admin`
   - パスワード: `TempPass123!`（一時パスワード）

### ② スーパーユーザー作成後の対応

1. **初期パスワードを管理画面で変更**
   - `/admin/` → Users → admin → 新しいパスワード設定

2. **環境変数から削除**（セキュリティ上重要）
   - Railway Dashboard → Variables
   - 削除対象:
     - `DJANGO_SUPERUSER_USERNAME`
     - `DJANGO_SUPERUSER_EMAIL`
     - `DJANGO_SUPERUSER_PASSWORD`

3. **再度デプロイ（環境変数削除を反映）**
   - GitHub に dummy commit をプッシュ
     ```bash
     git commit --allow-empty -m "Remove superuser env vars"
     git push origin main
     ```
   - Railway が自動デプロイ

---

## 🔍 トラブルシューティング

### エラー: `createsuperuser 失敗 - ユーザーが存在`

**症状**: Logs に以下が表示
```
IntegrityError: duplicate key value violates unique constraint "auth_user_username_key"
```

**対策**: 既に存在するため OK。パスワード設定のステップで更新される（既に実装）

---

### エラー: `collectstatic 失敗 - CSS が 404`

**症状**: ブラウザで `/static/css/style.css` が 404

**対策**:
1. Logs で `Collecting static files...` が成功しているか確認
2. 失敗している場合:
   - STATIC_ROOT のパスを確認（settings.py）
   - STATICFILES_DIRS が存在するか確認
   - Railway で再度デプロイ

### エラー: `Migration 失敗 - Database connection`

**症状**: Logs に以下
```
django.db.utils.OperationalError: could not connect to server
```

**対策**:
1. PostgreSQL が Railway で起動しているか確認
2. `DATABASE_URL` の形式が正しいか確認
3. 数秒後に再度デプロイ（一時的な接続エラーの場合）

---

## ✅ デプロイ成功の目印

✅ Logs に以下が表示されたら成功:

```
Running release command...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, intro, sessions
Running migrations:
  Applying admin...
  Applying auth...
  ...
✅ Password set for admin
Collecting static files...
  123 static files copied to '.../staticfiles', 456 unmodified.
```

---

## 📞 次のステップ

- ステップ 4: Vercel 側設定確認
