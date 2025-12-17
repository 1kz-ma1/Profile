# Cloudflareの導入ガイド

Cloudflareはグローバルなキャッシュネットワークを提供して、PythonAnywhereの無料プランのパフォーマンス制限を補います。

## メリット

✅ **グローバルCDN**: 静的ファイルの高速配信  
✅ **キャッシング**: データベースアクセス削減  
✅ **キープアライブ**: 接続最適化  
✅ **画像最適化**: 自動圧縮・変換  
✅ **セキュリティ**: DDoS対策  
✅ **無料プランで十分**: ほとんどの機能が使用可能

---

## ステップ1: Cloudflareアカウント作成

1. [Cloudflare](https://www.cloudflare.com/) にアクセス
2. 「Sign Up」をクリック
3. メールアドレスとパスワードで登録
4. メール認証を完了

---

## ステップ2: ドメインを追加

### 既にドメインを持っている場合

1. Cloudflareダッシュボード → 「サイトを追加」
2. 現在のドメイン（例: `example.com`）を入力
3. プランは「無料」を選択
4. 次へ進むとCloudflareのネームサーバーが表示されます

### ドメインをまだ購入していない場合

Cloudflareでドメインを購入するか、以下のレジストラーから購入してください：
- Namecheap
- Google Domains
- お名前.com
- Xserver

---

## ステップ3: ネームサーバーを変更

1. ドメインを購入したサービスのコントロールパネルにログイン
2. ネームサーバー設定を探す
3. Cloudflareから提供された2つのネームサーバーに変更：
   - 例: `luna.ns.cloudflare.com`
   - 例: `nash.ns.cloudflare.com`

**変更が反映されるまで: 24時間程度（多くの場合数分）**

---

## ステップ4: Cloudflareでサイト設定

### ステップ 4.1: DNS設定

ネームサーバー変更後、Cloudflareダッシュボード → 「DNS」

以下のレコードを追加/編集：

```
Type: A
Name: @ (またはドメイン名)
IPv4: PythonAnywhereから提供されたIP
Proxy: ⭐ オン（オレンジ雲）
TTL: 自動

Type: CNAME
Name: www
Target: 1kzma1.pythonanywhere.com
Proxy: ⭐ オン（オレンジ雲）
TTL: 自動
```

PythonAnywhereのIPアドレスを確認：
- PythonAnywhere アカウント → Web タブ
- 「Logging in via SSH」セクションでIPアドレスを確認

---

### ステップ 4.2: ルール・キャッシング設定

1. 「キャッシング」タブ → キャッシュレベル: **キャッシュエブリシング** (推奨)
2. 「キャッシング」→ ブラウザキャッシュTTL: **4時間**
3. 「ルール」→ キャッシュルール設定（下記参照）

### キャッシュルール例

Path: `/static/*` → キャッシュレベル: **キャッシュエブリシング**  
Path: `/media/*` → キャッシュレベル: **キャッシュエブリシング**  
Path: `/api/*` → キャッシュレベル: **キャッシュなし**  
Path: `/admin/*` → キャッシュレベル: **キャッシュなし**

---

### ステップ 4.3: SSL/TLS設定

1. 「SSL/TLS」タブ → 暗号化モード: **フル (厳密)**
2. 自動HTTPSリダイレクト: **有効**

---

### ステップ 4.4: ページルール（オプション）

「ルール」→ ページルール:

```
URL: example.com/admin*
キャッシュレベル: キャッシュなし
セキュリティレベル: 高

URL: example.com/api*
キャッシュレベル: キャッシュなし

URL: example.com/static*
キャッシュレベル: キャッシュエブリシング
キャッシュTTL: 365日
```

---

## ステップ5: Django設定ファイルの更新

`settings.py` を以下のように更新:

```python
# Cloudflare設定
CLOUDFLARE_ENABLED = True

# ALLOWED_HOSTS に Cloudflare ドメインを追加
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '1kzma1.pythonanywhere.com',
    'example.com',  # あなたのドメイン
    'www.example.com',
    '.pythonanywhere.com',
    '.cloudflare.com',
]

# Cloudflareの信頼できるプロキシ設定
SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}')
SECURE_SSL_REDIRECT = True

# セキュリティヘッダー
SECURE_HSTS_SECONDS = 31536000  # 1年
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## ステップ6: PythonAnywhereで設定

1. PythonAnywhere アカウント → Web タブ
2. Web app 設定 → WSGI configuration file を確認
3. 環境変数に追加:

```bash
ALLOWED_HOSTS=example.com,www.example.com,1kzma1.pythonanywhere.com
```

---

## ステップ7: キャッシング最適化

### HTML のキャッシュ（オプション）

静的ページ（`/about`, `/portfolio` など）:

```python
# views.py
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition

# 1時間キャッシュ
@cache_page(60 * 60)
def about(request):
    return render(request, 'about.html')
```

### API レスポンスのキャッシング

```python
# views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5分
def api_posts(request):
    posts = BlogPost.objects.all()
    return JsonResponse({'posts': list(posts.values())})
```

---

## ステップ8: 検証

1. ブラウザで `https://example.com` にアクセス
2. Cloudflareが機能しているか確認:

```
ブラウザの開発者ツール → Network tab
Response Headers を確認:
- CF-Ray: ... (Cloudflare ID)
- Server: cloudflare
```

---

## パフォーマンス最適化チェックリスト

- [ ] ドメインがCloudflareに登録されている
- [ ] ネームサーバーが変更済み（24時間以内に反映）
- [ ] DNS A/CNAMEレコード設定完了
- [ ] SSL/TLS 設定 = フル（厳密）
- [ ] HTTPSリダイレクト: 有効
- [ ] キャッシュレベル: キャッシュエブリシング
- [ ] ブラウザキャッシュ: 4時間
- [ ] 静的ファイルのキャッシュTTL: 高い（30日以上）
- [ ] `settings.py` 更新完了
- [ ] PythonAnywhereで環境変数設定完了

---

## トラブルシューティング

### ネームサーバーが反映されない

```bash
# Linuxコマンドで確認
nslookup example.com
dig example.com @1.1.1.1
```

### SSL エラー

→ Cloudflare 「SSL/TLS」→ 暗号化モード: **フル（厳密）** に変更

### キャッシュされない

→ ブラウザ開発者ツール → Network → Response Headers で確認  
→ `CF-Cache-Status: MISS` の場合はルール設定を確認

### 403 Forbidden エラー

→ `ALLOWED_HOSTS` に Cloudflare ドメインが含まれているか確認

---

## 次のステップ

1. **Brotli圧縮**: Cloudflare「Speed」→ 圧縮: 有効
2. **画像最適化**: 「Speed」→ 画像最適化: Polished
3. **HTTP/2**: デフォルトで有効
4. **キープアライブ**: Cloudflare → デフォルトで有効

これらの設定により、PythonAnywhereの無料プランでも大幅なパフォーマンス向上が期待できます！
