# 🔧 502 connection dial timeout 修正完了

## ✅ **根本原因**: `DJANGO_SETTINGS_MODULE` 未設定

### 問題点
Railway で gunicorn が起動した直後に Worker がクラッシュしていました。
原因は **`DJANGO_SETTINGS_MODULE` 環境変数が設定されていない** こと。

Django は import 時に `DJANGO_SETTINGS_MODULE` が必須で、
これが無いと `ImproperlyConfigured` エラーで起動に失敗します。

### 修正内容

**Procfile:**
```diff
- web: gunicorn workpro.wsgi --bind 0.0.0.0:$PORT
+ web: DJANGO_SETTINGS_MODULE=workpro.settings gunicorn workpro.wsgi --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

### 追加修正
- **--workers 2**: マルチプロセス化（負荷分散）
- **--timeout 60**: タイムアウト時間を60秒に延長（migrate 完了待ち）

---

## 🚀 **デプロイ手順**

### 1️⃣ ローカルテスト完了 ✅
```bash
# 既に確認済み
python -c "from workpro.wsgi import application; print('✅ OK')"
```

### 2️⃣ GitHub プッシュ
```bash
git add Procfile
git commit -m "Fix: Add DJANGO_SETTINGS_MODULE to Procfile to resolve 502 timeout"
git push origin main
```

### 3️⃣ Railway 自動デプロイ開始
- Deployment トリガー
- Logs で以下を確認:

```
Running release command...
Applying … OK
Collecting static files...

Listening on 0.0.0.0:8000
Worker spawned
```

### 4️⃣ 本番環境テスト
```
https://web-production-519fa.up.railway.app/
```

期待: HTTP 200 / HTTP 404（いずれでも OK、502 ではない）

---

## ✅ **チェックリスト**

- [ ] Procfile に `DJANGO_SETTINGS_MODULE=workpro.settings` が含まれている
- [ ] GitHub に commit & push 完了
- [ ] Railway Logs に `Listening on 0.0.0.0:$PORT` が出ている
- [ ] `ModuleNotFoundError` / `ImproperlyConfigured` が出ていない
- [ ] 502 エラーが消えて、200/404 になった

---

## 📞 もし 502 が続く場合

→ Railway Logs で以下を探してください:
```
ImproperlyConfigured
ModuleNotFoundError
ImportError
Traceback
```

見つかったら、エラーメッセージを全部報告してください。
