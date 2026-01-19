# Vercel フロント設定ガイド

## 1. Vercel プロジェクト作成

### 1.1 プロジェクト設定

**UI 遷移:**
1. vercel.com にアクセス
2. GitHub でログイン
3. Dashoard → 「Add New」→ 「Project」
4. リポジトリ選択（このリポジトリ）
5. 「Import」

### 1.2 Deploy 設定

**フレームワーク検出:**
- Vercel が自動検出しない場合：
  - Framework Preset: 「Other」を選択
  - Root Directory: `frontend/` に設定

**ビルドコマンド:**
```
npm install && npm run build
```

**出力ディレクトリ:**
```
.next
```

---

## 2. 環境変数設定（本番）

**Vercel Dashboard → Project → Settings → Environment Variables**

### 設定項目

| Key | Value | 説明 |
|-----|-------|------|
| `NEXT_PUBLIC_API_BASE` | `https://your-domain.up.railway.app` | Railway バックエンドの本番URL |

**注意**: 
- Railway デプロイ完了後、ドメインが確定してから設定
- `NEXT_PUBLIC_` プレフィックスでブラウザに公開される

---

## 3. フロント側での API 呼び出し実装

### 3.1 API Client の作成

**ファイル: `frontend/lib/api.js` (新規作成)**

```javascript
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function fetchAPI(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    credentials: 'include', // CSRF トークン送信
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

// 例: ブログポスト取得
export async function getBlogPosts() {
  return fetchAPI('/api/posts/');
}
```

### 3.2 コンポーネントから呼び出し

```javascript
import { getBlogPosts } from '@/lib/api';

export default async function BlogPage() {
  const posts = await getBlogPosts();
  
  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>{post.title}</article>
      ))}
    </div>
  );
}
```

---

## 4. CORS/CSRF エラー切り分け

### 4.1 ブラウザコンソールでエラー確認

**F12 → Console タブで確認:**

#### エラー A: CORS エラー
```
Access to XMLHttpRequest at 'https://...' from origin 'https://your-domain.vercel.app' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

**対策:**
1. Django settings.py の `CSRF_TRUSTED_ORIGINS` を確認
2. `https://*.vercel.app` が含まれているか
3. Railway を再デプロイ

#### エラー B: CSRF Token エラー
```
403 Forbidden
Reason given for failure: CSRF verification failed
```

**対策:**
1. フロント側で `credentials: 'include'` を設定（上記コード参照）
2. POST リクエストに CSRF トークンを含める必要がある場合:
   ```javascript
   // Django から CSRF トークンを取得
   async function getCSRFToken() {
     const response = await fetch(`${API_BASE}/api/csrf-token/`, {
       credentials: 'include',
     });
     const data = await response.json();
     return data.csrfToken;
   }
   
   // POST リクエストで送信
   const token = await getCSRFToken();
   await fetchAPI('/api/posts/', {
     method: 'POST',
     headers: {
       'X-CSRFToken': token,
     },
     body: JSON.stringify(data),
   });
   ```

### 4.2 Network タブでリクエスト確認

**F12 → Network タブ:**

1. API リクエストを実行
2. 対象の HTTP リクエストをクリック
3. Request Headers で以下を確認:
   - `Origin: https://your-domain.vercel.app` が送信されているか
   - `Referer: https://your-domain.vercel.app/...` が送信されているか

4. Response Headers で以下を確認:
   - `Access-Control-Allow-Origin: https://your-domain.vercel.app`
   - `Access-Control-Allow-Credentials: true`

### 4.3 Django 側のログで確認

**Railway Dashboard → Deployments → Logs:**

```
WARNING: Forbidden (403): /api/posts/ CSRF verification failed.
```

の場合:
- Django の CSRF_TRUSTED_ORIGINS を確認
- Railway を再デプロイ

---

## 5. 環境変数の本番化

### 現在（開発）

**frontend/.env.example:**
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### 本番化

**Vercel Dashboard → Settings → Environment Variables:**
- 本番環境に Railway URL を設定
- Staging 環境にローカル URL を設定（オプション）

---

## 6. デプロイ実行

### Git にプッシュ

```bash
git add .
git commit -m "Setup Vercel frontend with Railway backend"
git push origin main
```

### Vercel が自動デプロイ

- Vercel Dashboard → Deployments で進度確認
- デプロイ完了後、Production URL で確認

---

## ✅ 動作確認チェックリスト

- [ ] Vercel URL で HTTP 200 が返る
- [ ] ブラウザコンソールに CORS エラーがない
- [ ] API エンドポイントへのリクエストが 200 で返る
- [ ] フロント側で API データが表示される

---

## 📞 次のステップ

- ステップ 5: 疎通と検証の順序
