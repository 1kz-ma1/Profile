# 本番環境 疎通 検証手順

## 📋 検証フロー

```
① Railway のルート疎通確認
  ↓
② Django Admin ページ表示確認
  ↓
③ API エンドポイント直接確認
  ↓
④ Vercel からのリクエスト確認
  ↓
⑤ 本番用ドメイン固定化
```

---

## ① Railway ルート疎通確認（200 または 404 でOK）

### 目的
Railway が起動し、gunicorn が応答しているか確認

### 確認方法

**方法 A: ブラウザ**
```
https://your-domain.up.railway.app/
```

**期待される結果:**
- HTTP 200: 通常ページ表示
- HTTP 404: Not Found（ルートに page がない場合、OK）
- HTTP 500: ❌ Django エラー → Logs を確認

**方法 B: curl**
```bash
curl -I https://your-domain.up.railway.app/
```

**期待される出力:**
```
HTTP/2 200 
# または
HTTP/2 404 
```

### トラブル時の確認

**Railway Dashboard → Deployments → Latest → Logs**

以下を確認:
```
Starting gunicorn on 0.0.0.0:$PORT
Listening on port 8000
```

---

## ② Django Admin ページ表示確認（CSS が読み込まれているか）

### 目的
静的ファイル（CSS/JS）が正しく配信されているか確認

### 確認方法

```
https://your-domain.up.railway.app/admin/
```

**期待される結果:**
- ログイン画面が表示される
- ✅ CSS が読み込まれて、スタイルが適用されている
- ❌ HTML のみ表示（CSS が 404）→ collectstatic 失敗

### CSS が 404 の場合

**Logs で確認:**
```
Collecting static files...
0 static files copied
```

**対策:**
1. Procfile の release フェーズを確認
2. STATIC_ROOT が正しく設定されているか確認
3. Railway を再度デプロイ

### ログインして確認

**ユーザー名**: `admin`
**パスワード**: （設定した一時パスワード）

---

## ③ API エンドポイント直接確認

### 目的
Django が API を応答しているか確認

### 確認方法

既存のエンドポイントに直接アクセス（例: ブログポスト一覧）

```
https://your-domain.up.railway.app/api/posts/
```

**期待される結果:**
- ✅ JSON が返される
- ❌ 404: エンドポイントが存在しない（models.py を確認）
- ❌ 500: Django エラー（Logs で詳細確認）

**方法 B: curl で詳細確認**
```bash
curl -v https://your-domain.up.railway.app/api/posts/
```

**確認項目:**
- HTTP 200 が返る
- `Content-Type: application/json` が返される
- JSON データが正しく返される

### Logs で API アクセスログを確認

```
GET /api/posts/ HTTP/1.1" 200 12345
```

---

## ④ Vercel からのリクエスト疎通確認

### 目的
Vercel フロント側から Railway バックエンド側へ CORS/CSRF エラーなくリクエストが到達するか確認

### 4.1 まず手動で API を叩く

**ブラウザコンソール（DevTools → Console）から実行:**

```javascript
// NEXT_PUBLIC_API_BASE に Railway URL が設定されているか確認
fetch(process.env.NEXT_PUBLIC_API_BASE + '/api/posts/', {
  credentials: 'include',
})
  .then(r => r.json())
  .then(d => console.log(d))
  .catch(e => console.error(e));
```

**期待される結果:**
```
[
  { id: 1, title: "Post 1", ... },
  { id: 2, title: "Post 2", ... },
  ...
]
```

### 4.2 エラーが出た場合の確認フロー

#### エラー A: CORS エラー

**エラー表示:**
```
Access to fetch at 'https://your-domain.up.railway.app/api/posts/' from origin 'https://your-domain.vercel.app' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

**確認項目:**
1. Django settings.py の `CSRF_TRUSTED_ORIGINS` に Vercel ドメインが含まれているか
   ```python
   CSRF_TRUSTED_ORIGINS = [
       'https://*.vercel.app',  # ← これが必須
       'https://*.railway.app',
   ]
   ```

2. Vercel URL が正しいか
   - Railway の `ALLOWED_HOSTS` に Vercel ドメインを追加する必要はない（CSRF_TRUSTED_ORIGINS で十分）

3. Railway を再度デプロイ

#### エラー B: CSRF エラー

**エラー表示:**
```
403 Forbidden - CSRF verification failed
```

**確認項目:**
1. フロント側で `credentials: 'include'` が設定されているか（API client に実装）
2. Django が CSRF トークンを発行しているか
   - Django は通常、HTML フォームに自動挿入される
   - API の場合、別途 CSRF トークン取得エンドポイントが必要な場合あり

**対策:**
- 必要に応じて、Django に CSRF トークン取得 API を追加
  ```python
  # urls.py
  path('api/csrf-token/', csrf_exempt(get_csrf_token_view))
  ```

### 4.3 Network タブで詳細確認

**DevTools → Network タブ:**

1. フロント側で API リクエストを実行
2. Network タブに表示される API リクエストをクリック
3. 確認項目:
   - **Request Headers:**
     - `Origin: https://your-domain.vercel.app`
     - `Referer: https://your-domain.vercel.app/...`
   - **Response Headers:**
     - `Access-Control-Allow-Origin: https://your-domain.vercel.app` または `*`
     - `Access-Control-Allow-Credentials: true`
   - **Response Status:** `200 OK`

---

## ⑤ 本番用ドメイン固定化

### 現在（ワイルドカード使用）

**Django settings.py:**
```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',      # ← ワイルドカード
    'https://*.railway.app',     # ← ワイルドカード
]

ALLOWED_HOSTS = ['.railway.app', '.vercel.app']  # ← ワイルドカード
```

### 本番化（具体的なドメイン指定）

検証が完了したら、本番用に具体的なドメインに変更:

**Django settings.py:**
```python
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.vercel.app',     # ← 具体的なドメイン
]

ALLOWED_HOSTS = [
    'your-domain.up.railway.app',  # ← 具体的なドメイン
    'localhost',
    '127.0.0.1',
]
```

**変更方法:**

1. **ローカルで settings.py を編集**

2. **GitHub にプッシュ**
   ```bash
   git add workpro/settings.py
   git commit -m "Fix: Use production domains instead of wildcards"
   git push origin main
   ```

3. **Railway が自動デプロイ**

---

## ✅ 検証完了チェックリスト

- [ ] ① Railway ルート (200 or 404)
- [ ] ② Django Admin ページ表示 + CSS 読み込み確認
- [ ] ③ API エンドポイント JSON 応答確認
- [ ] ④ Vercel から API リクエスト成功
- [ ] ⑤ CORS/CSRF エラーなし
- [ ] ⑥ 本番ドメイン固定化完了

---

## 📞 次のステップ

- ステップ 6: 最終チェックリスト
