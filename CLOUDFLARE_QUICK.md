# Cloudflare Workers 簡単セットアップ

**PythonAnywhereサブドメイン用・無料・最速**

---

## ⚡ 最短ルート（15分）

### 1️⃣ Cloudflare アカウント作成（3分）

```
1. https://www.cloudflare.com
2. Sign Up
3. メール認証
```

### 2️⃣ Worker 作成（2分）

```
Cloudflare ダッシュボード
  → Workers & Pages
  → Create
  → Create Worker
```

ワーカー作成完了 ✅

### 3️⃣ コード貼り付け（3分）

Worker 画面 → Edit Code

以下をコピペ:

```javascript
export default {
  async fetch(request, env, ctx) {
    const upstreamUrl = new URL(request.url);
    upstreamUrl.hostname = '1kzma1.pythonanywhere.com';
    
    const cacheKey = new Request(upstreamUrl.toString(), {
      method: request.method,
    });
    
    let response = await env.CACHE.match(cacheKey);
    
    if (!response) {
      response = await fetch(upstreamUrl.toString(), {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });
      
      if (request.method === 'GET' || request.method === 'HEAD') {
        const cacheControl = upstreamUrl.pathname.match(/\.(js|css|jpg|png|gif|woff)$/)
          ? 86400 : 3600;
        
        const cacheHeaders = new Headers(response.headers);
        cacheHeaders.set('Cache-Control', `public, max-age=${cacheControl}`);
        response = new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: cacheHeaders,
        });
        
        ctx.waitUntil(env.CACHE.put(cacheKey, response.clone()));
      }
    }
    
    return response;
  }
};
```

→ Save and Deploy ✅

### 4️⃣ KV ストレージ設定（3分）

```
Settings → KV Namespace Bindings
  → Add Binding
  → 変数名: CACHE
  → Create Namespace で「cache」を作成
  → Save
```

✅ 完了！

### 5️⃣ Django 設定（2分）

PythonAnywhere → Web タブ

環境変数追加:
```
ALLOWED_HOSTS=1kzma1.pythonanywhere.com
CLOUDFLARE_ENABLED=True
```

Reload

✅ 完了！

---

## 🔗 アクセス

Worker URL でアクセス:
```
https://your-worker.your-subdomain.workers.dev
```

---

## ✨ 結果

| 項目 | 改善 |
|------|------|
| 初回 | 500ms → 250ms ⚡ |
| キャッシュ | 500ms → 50ms 🚀 |
| 無料 | YES ✅ |
| セットアップ | 15分 ⏱️ |

---

## 🆘 問題が起きた？

### ページ表示されない
→ コードの `1kzma1.pythonanywhere.com` が正しいか確認

### キャッシュされない
→ F12 → Network → CF-Cache-Status 確認

### Admin が見えない
→ PythonAnywhereで別途ログイン必要（Workerでは無視OK）

---

**セットアップ完了！サイト高速化できます 🎉**

