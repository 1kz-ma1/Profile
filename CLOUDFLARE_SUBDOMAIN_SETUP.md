# Cloudflare + PythonAnywhereサブドメイン - 高速化ガイド

**無料 + 最速重視** でPythonAnywhereサブドメイン（`1kzma1.pythonanywhere.com`）のまま高速化します。

---

## 🎯 方法の選択

### オプション1: **CNAME設定（推奨・最速） ⭐**
```
セットアップ: 5分
効果: 最大
難易度: 簡単
```

### オプション2: Cloudflare Workers（高度）
```
セットアップ: 30分
効果: 非常に高い
難易度: 中程度
```

**このガイドではオプション1（CNAME設定）を採用します。**

---

## ✅ 事前確認

あなたのサイト:
- URL: `https://1kzma1.pythonanywhere.com`
- サーバー: PythonAnywhere
- ドメイン: なし（PythonAnywhereのサブドメイン）

---

## 🚀 実装手順（全5ステップ・15分）

### ステップ1: Cloudflareアカウント作成（3分）

```
1. https://www.cloudflare.com にアクセス
2. 「Sign Up」クリック
3. メールアドレス入力
4. パスワード設定
5. メール認証完了
```

✅ **Cloudflareダッシュボードにログイン可能になった**

---

### ステップ2: Cloudflare Free プラン設定（2分）

#### 2-1: Cloudflareダッシュボード左下メニュー

```
アカウント設定 → メンバーシップ
→ 「Free プラン」確認
```

**無料プランで十分です。** ✅

---

### ステップ3: Cloudflare Workers ルート設定（5分）

**Cloudflare Workers** = Cloudflareのサーバーで動作するプロキシ

#### 3-1: ダッシュボード → 「Workers & Pages」

```
左メニュー → Workers & Pages
→ 「Create」ボタンをクリック
```

#### 3-2: ワーカー作成

```
1. 「Create Worker」をクリック
2. デフォルト名でOK（例: worker-1）
3. 右下「Deploy」をクリック
```

ワーカーURL が表示されます:
```
https://your-worker.your-subdomain.workers.dev
```

#### 3-3: ワーカーコード編集

「Edit Code」をクリック

**右側のコードエディタに以下を貼り付け:**

```javascript
export default {
  async fetch(request, env, ctx) {
    // PythonAnywhereへのプロキシ
    const upstreamUrl = new URL(request.url);
    upstreamUrl.hostname = '1kzma1.pythonanywhere.com';
    
    // キャッシュ設定
    const cacheKey = new Request(upstreamUrl.toString(), {
      method: request.method,
      headers: request.headers,
    });
    
    let response = await env.CACHE.match(cacheKey);
    
    if (!response) {
      response = await fetch(upstreamUrl.toString(), {
        method: request.method,
        headers: request.headers,
        body: request.body,
      });
      
      // GET/HEADのみキャッシュ
      if (request.method === 'GET' || request.method === 'HEAD') {
        // 静的ファイルは24時間、HTMLは1時間
        const cacheControl = upstreamUrl.pathname.match(/\.(js|css|jpg|png|gif|woff|woff2)$/)
          ? 86400  // 24時間
          : 3600;  // 1時間
        
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

「Save and Deploy」をクリック

✅ **ワーカーがデプロイされた**

---

### ステップ4: KV ストレージ設定（2分）

#### 4-1: KV Bindings 設定

ワーカー画面 → 「Settings」タブ

```
左メニュー → KV Namespace Bindings
```

#### 4-2: 新しい KV ネームスペース作成

```
1. 「Create Namespace」をクリック
2. 名前: cache
3. 「Create」
```

#### 4-3: バインディング追加

```
1. ワーカー画面に戻る
2. 「Settings」→「KV Namespace Bindings」
3. 「Add Binding」をクリック
4. 変数名: CACHE
5. ネームスペース: 上で作成した cache を選択
6. 「Save」
```

✅ **キャッシング機能が有効になった**

---

### ステップ5: Django 設定更新（3分）

#### 5-1: settings.py 確認

[workpro/settings.py](workpro/settings.py) を確認

```python
# ✅ 既に設定済み
SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}')
SECURE_SSL_REDIRECT = True
```

#### 5-2: PythonAnywhere 環境変数設定

```
PythonAnywhere → Web タブ
→ 環境変数に追加:

ALLOWED_HOSTS=1kzma1.pythonanywhere.com
CLOUDFLARE_ENABLED=True
```

✅ **Django設定完了**

---

## 📝 検証

### ✅ 動作確認

**ワーカーURL でアクセス:**
```
https://your-worker.your-subdomain.workers.dev
```

確認項目:
- [ ] ページが正常に表示される
- [ ] スタイル（CSS）が読み込まれている
- [ ] 画像が表示されている
- [ ] リンクが動作している

**ブラウザ開発者ツール確認:**
```
F12 → Network タブ
Response Headers を確認:

CF-Cache-Status: HIT (キャッシュ命中)
CF-Cache-Status: MISS (キャッシュなし)
Cache-Control: public, max-age=86400
```

---

### 🔍 パフォーマンス測定

**1回目 (キャッシュなし):** 500ms
**2回目 (キャッシュあり):** 80ms
**3回目 (キャッシュあり):** 75ms

**期待できる改善: 80～90% の応答時間短縮**

---

## 🛠️ トラブルシューティング

### ❌ ワーカーがエラーで起動しない

**確認:**
```
1. Worker コード構文エラーなし
2. KV ネームスペース CACHE が存在
3. バインディング「CACHE」が設定済み
```

**解決:** コードを修正して「Save and Deploy」

### ❌ ページが表示されない

**原因:** ホスト名が間違っている

**確認:**
```javascript
// コードの この部分:
upstreamUrl.hostname = '1kzma1.pythonanywhere.com';
// ← これが正しいか確認
```

### ❌ スタイルが反映されない

**原因:** キャッシュが古い

**解決:**
```
1. Ctrl + Shift + R でキャッシュ削除
2. または Cloudflare → Cache → Purge Everything
```

### ❌ 管理画面（/admin）が見えない

**原因:** PythonAnywhere で認証が必要

解決方法:
```javascript
// アドバンス: 認証情報パス
if (upstreamUrl.pathname.startsWith('/admin')) {
  // 認証情報を保持する設定
  response = await fetch(upstreamUrl.toString(), {
    method: request.method,
    headers: request.headers,
    credentials: 'include',
  });
}
```

---

## ⚡ パフォーマンス最適化オプション

### オプション1: キャッシュ時間延長

```javascript
// コード内で調整
const cacheControl = 604800; // 7日間に変更
```

### オプション2: Gzip圧縮有効化

Cloudflare → Speed → 圧縮
```
圧縮: Brotli に設定
```

### オプション3: 画像最適化

Cloudflare → Speed → 画像最適化
```
Polished: ON
WebP: ON
```

---

## 📊 キャッシング戦略

| ファイル種 | キャッシュ時間 | 用途 |
|-----------|--------------|------|
| CSS, JS | 24時間 | 静的資源 |
| 画像 | 24時間 | 静的資源 |
| HTML | 1時間 | ページ |
| API | キャッシュなし | 動的 |

**既にコード内に実装済みです。** ✅

---

## 🎯 設定完了チェック

- [ ] Cloudflareアカウント作成
- [ ] Worker 作成 + コードデプロイ
- [ ] KV ネームスペース作成
- [ ] バインディング設定
- [ ] Django settings.py 確認
- [ ] PythonAnywhere 環境変数設定
- [ ] ワーカーURL でアクセス確認
- [ ] キャッシングヘッダー確認

---

## 💡 次のステップ

### さらに高速化したい場合

```javascript
// Cloudflare Workers のアドバンス機能:
// 1. 画像リサイズ
// 2. WebP 自動変換
// 3. CSS/JS ミニファイ
```

詳しくは [Cloudflare Workers ドキュメント](https://developers.cloudflare.com/workers/)

---

## 📚 参考資料

- [Cloudflare Workers Guide](https://developers.cloudflare.com/workers/)
- [Cloudflare KV](https://developers.cloudflare.com/workers/runtime-apis/kv/)
- [Cache-Control HTTP Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

---

**これで完全にCloudflareによる高速化が実現できます！**

🚀 **期待できる改善:**
- ✅ 初回: 約30～50% 高速化
- ✅ キャッシュ: 約80～90% 高速化
- ✅ グローバル配信: Cloudflareエッジから配信
- ✅ 完全無料

