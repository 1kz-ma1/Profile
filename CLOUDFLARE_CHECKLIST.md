# Cloudflare導入 - 実行チェックリスト

## フェーズ 1: 準備（所要時間: 30分）

### タスク 1-1: Cloudflareアカウント作成
- [ ] https://www.cloudflare.com にアクセス
- [ ] メールアドレスで登録
- [ ] メール認証完了
- [ ] Cloudflareダッシュボードにログイン可能

### タスク 1-2: ドメイン準備
- [ ] ドメイン所有確認
- [ ] ドメインレジストラー情報確認（お名前.com, Namecheap等）
- [ ] レジストラーコントロールパネルへのログイン確認

### タスク 1-3: PythonAnywhereの確認
- [ ] PythonAnywhereにログイン
- [ ] Web タブで現在のIPアドレスを確認/メモ
  ```
  IP: _________________________
  ```
- [ ] `1kzma1.pythonanywhere.com` のDNS設定確認

---

## フェーズ 2: Cloudflareにドメイン追加（所要時間: 10分）

### タスク 2-1: Cloudflareでサイト追加
- [ ] Cloudflareダッシュボード → 「サイトを追加」
- [ ] ドメイン名入力（例: `example.com`）
- [ ] 「プランの選択」→ **無料** を選択
- [ ] ネームサーバーが表示される

### タスク 2-2: ネームサーバーをメモ
- [ ] 第1ネームサーバー: _________________________
- [ ] 第2ネームサーバー: _________________________

---

## フェーズ 3: DNS設定変更（所要時間: 5分）

### タスク 3-1: ドメインレジストラーでネームサーバー変更
1. ドメインレジストラーにログイン
   ```
   サービス: _________________________
   ユーザー名: _________________________
   ```

2. ネームサーバー設定を見つける
   ```
   場所: _________________________
   ```

3. 現在のネームサーバーを削除
   ```
   削除したネームサーバー 1: _________________________
   削除したネームサーバー 2: _________________________
   ```

4. Cloudflareのネームサーバーを追加
   ```
   追加したネームサーバー 1: _________________________
   追加したネームサーバー 2: _________________________
   ```

5. 設定保存
   - [ ] 「保存」または「確定」をクリック
   - [ ] 確認メール受信

### ⏳ 反映待ち（24時間以内、通常数分）
```
変更実施時刻: __________
反映完了予定時刻: __________
```

---

## フェーズ 4: Cloudflare DNS設定（所要時間: 15分）

### タスク 4-1: ネームサーバー反映確認

ネームサーバーが反映されるまで待つ方法：
```bash
# Windows PowerShell で実行
nslookup example.com
```

実行結果:
```
Server: ___________________
Address: ___________________

Non-authoritative answer:
Name: ___________________
Address: ___________________
```

**確認: Cloudflareのネームサーバー表示があればOK** ✅

### タスク 4-2: CloudflareでDNS設定

Cloudflareダッシュボード → DNS → DNS records:

#### レコード 1: A レコード
```
Type: A
Name: @ (またはルート)
IPv4 address: [PythonAnywhereのIP]
TTL: 自動
Proxy status: ⭐ オン（オレンジ雲）
```
- [ ] 設定保存

#### レコード 2: CNAME レコード (www用)
```
Type: CNAME
Name: www
Target: 1kzma1.pythonanywhere.com
TTL: 自動
Proxy status: ⭐ オン（オレンジ雲）
```
- [ ] 設定保存

**DNSレコード確認:**
```
記録されたA レコード: _________________________
記録されたCNAME レコード: _________________________
```

---

## フェーズ 5: SSL/TLS設定（所要時間: 10分）

### タスク 5-1: SSL/TLS設定
Cloudflareダッシュボード → SSL/TLS

1. 暗号化モード
   - [ ] 「フル（厳密）」を選択

2. 自動HTTPSリダイレクト
   - [ ] 「ON」に設定

3. 最小TLSバージョン
   - [ ] 「TLS 1.2」を推奨

**確認:**
```
暗号化モード: _________________________
HTTPSリダイレクト: _________________________
```

---

## フェーズ 6: キャッシング設定（所要時間: 15分）

### タスク 6-1: キャッシング基本設定
Cloudflareダッシュボード → キャッシング

- [ ] キャッシュレベル: **キャッシュエブリシング** に変更
- [ ] ブラウザキャッシュTTL: **4時間** に設定

### タスク 6-2: ルール設定
Cloudflareダッシュボード → ルール → キャッシュルール

以下のルールを作成:

**ルール 1: 静的ファイルキャッシュ**
- [ ] URL パス: `/static/*`
- [ ] キャッシュレベル: キャッシュエブリシング
- [ ] 保存

**ルール 2: メディアファイルキャッシュ**
- [ ] URL パス: `/media/*`
- [ ] キャッシュレベル: キャッシュエブリシング
- [ ] 保存

**ルール 3: 管理画面はキャッシュなし**
- [ ] URL パス: `/admin/*`
- [ ] キャッシュレベル: キャッシュなし
- [ ] 保存

**ルール 4: API はキャッシュなし**
- [ ] URL パス: `/api/*`
- [ ] キャッシュレベル: キャッシュなし
- [ ] 保存

---

## フェーズ 7: Django設定更新（所要時間: 10分）

### タスク 7-1: settings.py 確認
[workpro/settings.py](workpro/settings.py)

以下の設定が追加されているか確認:
```python
# Cloudflare設定
CLOUDFLARE_ENABLED = os.environ.get('CLOUDFLARE_ENABLED', 'False') == 'True'
if CLOUDFLARE_ENABLED:
    SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
```

- [ ] 確認済み

### タスク 7-2: キャッシングユーティリティ確認
[intro/cache_utils.py](intro/cache_utils.py)
- [ ] ファイル存在確認

### タスク 7-3: Views キャッシング確認
[intro/views.py](intro/views.py)
- [ ] `@cache_page` デコレータが index, about に適用済み確認

### タスク 7-4: 変更をコミット
```bash
cd c:\web_work\Scripts\workpro
git add -A
git commit -m "Add Cloudflare support and caching optimization"
git push origin main
```
- [ ] 完了

---

## フェーズ 8: PythonAnywhere環境変数設定（所要時間: 5分）

### タスク 8-1: PythonAnywhereで環境変数設定
1. PythonAnywhere → Web タブ
2. 現在のWebアプリ設定を開く
3. 「Edit」をクリック
4. 環境変数追加:

```
ALLOWED_HOSTS=example.com,www.example.com,1kzma1.pythonanywhere.com
CLOUDFLARE_ENABLED=True
```

- [ ] 設定保存
- [ ] Webアプリをリロード

**入力内容:**
```
ALLOWED_HOSTS: _________________________
CLOUDFLARE_ENABLED: True
```

---

## フェーズ 9: 動作確認（所要時間: 10分）

### タスク 9-1: HTTPS アクセス確認
```
1. ブラウザで https://example.com にアクセス
2. 鍵アイコン ✅ 表示確認
```
- [ ] HTTPSで正常アクセス

### タスク 9-2: キャッシング確認
```
ブラウザ開発者ツール (F12) → Network タブ

以下を確認:
Response Headers:
- CF-Ray: XXXXXXX_XXXXXXX_XXXXX_JP
- Server: cloudflare
- Cache-Control: public, max-age=...
```

**結果:**
```
CF-Ray: _________________________
Server: _________________________
Cache-Control: _________________________
```

### タスク 9-3: 複数ブラウザテスト
- [ ] Chrome でアクセス確認
- [ ] Firefox でアクセス確認
- [ ] Edge でアクセス確認
- [ ] スマートフォンブラウザで確認

### タスク 9-4: パフォーマンス比較
Cloudflare前後のパフォーマンス測定:

```
テスト URL: https://example.com

1回目 (キャッシュなし): _____ ms
2回目 (キャッシュあり): _____ ms
3回目 (キャッシュあり): _____ ms

改善率: _____ %
```

---

## フェーズ 10: トラブルシューティング

### 問題: 403 Forbidden エラー

**原因:** `ALLOWED_HOSTS` に Cloudflare ドメインが含まれていない

**解決:**
```python
# settings.py で以下を確認
ALLOWED_HOSTS = [
    'example.com',
    'www.example.com',
    '1kzma1.pythonanywhere.com',
]

# または environment variable で設定
ALLOWED_HOSTS=example.com,www.example.com
```

- [ ] 確認済み

### 問題: SSL証明書エラー

**原因:** Cloudflare の暗号化モードが「完全」以下

**解決:**
```
Cloudflare → SSL/TLS → 暗号化モード
→ 「フル（厳密）」に変更
```

- [ ] 確認済み

### 問題: キャッシュされない

**原因:** ルール設定が正しくない

**解決:**
```bash
# ブラウザで確認
F12 → Network → Response Headers
CF-Cache-Status: HIT (キャッシュ命中)
CF-Cache-Status: MISS (キャッシュなし)
```

- [ ] 確認済み

### 問題: ネームサーバーが反映されない

**原因:** 反映待ちまたはレジストラー設定ミス

**確認コマンド:**
```bash
# Windows PowerShell
nslookup -type=NS example.com
```

実行結果:
```
_________________________________
```

- [ ] 確認済み

---

## フェーズ 11: 最終最適化（所要時間: 20分）

### タスク 11-1: Brotli圧縮有効化
Cloudflareダッシュボード → Speed → 圧縮
- [ ] 圧縮: **Brotli** に設定

### タスク 11-2: 画像最適化有効化
Cloudflareダッシュボード → Speed → 画像最適化
- [ ] Polished: **ON**
- [ ] WebP: **ON**

### タスク 11-3: HTTP/2 確認
Cloudflareダッシュボード → Speed
- [ ] HTTP/2: 自動有効（確認）

### タスク 11-4: ページルール設定（オプション）
Cloudflareダッシュボード → ルール → ページルール

ブロックする URL パターン:
```
/admin* → セキュリティレベル: 高
/api* → キャッシュなし
```

- [ ] 設定完了

---

## フェーズ 12: 完了チェック

- [ ] Cloudflareアカウント作成
- [ ] ドメイン追加
- [ ] ネームサーバー変更
- [ ] DNS レコード設定
- [ ] SSL/TLS 設定 = フル（厳密）
- [ ] キャッシング有効化
- [ ] Django settings.py 更新
- [ ] PythonAnywhere 環境変数設定
- [ ] HTTPS アクセス確認
- [ ] キャッシング動作確認
- [ ] パフォーマンス測定

**完了日時: ___________________**

---

## サポート情報

### Cloudflare サポート
- [Cloudflare ドキュメント](https://developers.cloudflare.com/)
- [DNS管理ガイド](https://support.cloudflare.com/hc/ja/articles/200166926)

### Django キャッシング
- [Django キャッシング ドキュメント](https://docs.djangoproject.com/ja/4.2/topics/cache/)

### PythonAnywhere
- [PythonAnywhere ドキュメント](https://help.pythonanywhere.com/)

