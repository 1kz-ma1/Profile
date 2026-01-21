# 502 connection dial timeout トラブルシューティング

## 🔍 **ログ確認フロー**

### Railway Logs で確認すべき内容

**Railway Dashboard → Project → Deployments → Latest → Logs**

以下を探して報告ください：

#### 1️⃣ **release フェーズの実行ログ**
```
Running release command...
Applying admin.0001_initial... OK
Applying auth.0001_initial... OK
...
Collecting static files...
```
↑ これが出ているか？

#### 2️⃣ **gunicorn 起動ログ**
```
Starting gunicorn 21.2.0
Listening on 0.0.0.0:8000
```
↑ これが出ているか？

#### 3️⃣ **Worker クラッシュ関連のエラー**
```
ModuleNotFoundError: No module named 'workpro'
ImportError: ...
AttributeError: ...
```
↑ これが出ていないか？

#### 4️⃣ **その他エラー**
```
Traceback (most recent call last):
...
```
↑ スタックトレースが出ていないか？

---

## 🛠️ **ローカルで再現テスト**

### テスト 1: gunicorn で起動してみる

```bash
cd c:\web_work\Scripts\workpro

# 簡易テスト（フォアグラウンド）
python -m gunicorn workpro.wsgi:application --bind 0.0.0.0:8000 --workers 1 --timeout 60 --log-level debug
```

**期待される出力:**
```
Starting gunicorn 21.2.0
Listening on 0.0.0.0:8000
Worker spawned (pid: xxxx)
```

### テスト 2: WSGI アプリケーションを直接実行

```bash
python -c "
from workpro.wsgi import application
print('✅ WSGI application imported successfully')
print('Application:', application)
"
```

**期待される出力:**
```
✅ WSGI application imported successfully
Application: <wsgiref.simple_server.WSGIApplication object at 0x...>
```

### テスト 3: settings.py をインポート

```bash
python -c "
from django.conf import settings
print('✅ Django settings loaded')
print('DEBUG:', settings.DEBUG)
print('DATABASES:', settings.DATABASES.keys())
"
```

**期待される出力:**
```
✅ Django settings loaded
DEBUG: True
DATABASES: dict_keys(['default'])
```

---

## ⚠️ **よくある原因と対策**

### 原因 A1: Python パスが通っていない

**症状:**
```
ModuleNotFoundError: No module named 'workpro'
```

**対策:**
```bash
# BASE_DIR を確認
python -c "
from pathlib import Path
print('Python path:', __file__)
print('CWD:', Path.cwd())
"

# workpro/ があるか確認
ls workpro/
```

### 原因 A2: `gunicorn workpro.wsgi` が間違っている

**症状:**
```
ImportError: cannot import name 'application' from 'workpro.wsgi'
```

**確認:**
```bash
cat workpro/wsgi.py
```

**必須:**
```python
# workpro/wsgi.py の末尾に以下があるか
application = get_wsgi_application()
```

### 原因 A3: 環境変数が設定されていない（ローカル）

**症状:**
```
KeyError: 'DATABASE_URL'
```

**対策（ローカル）:**
```bash
# .env に設定
cat > .env << EOF
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# 読み込み
$env:DEBUG="True"
$env:DATABASE_URL="sqlite:///db.sqlite3"
```

### 原因 A4: Procfile の `web:` コマンドが正しくない

**現在の Procfile:**
```
web: gunicorn workpro.wsgi --bind 0.0.0.0:$PORT
```

**確認:**
```bash
# $PORT が展開されているか
echo $PORT
```

**代替案（明示的にポート指定）:**
```
web: gunicorn workpro.wsgi --bind 0.0.0.0:8000
```

---

## 📋 **確認チェックリスト**

以下を順番に確認して、結果を報告してください：

- [ ] `python -m gunicorn workpro.wsgi:application --bind 0.0.0.0:8000` でエラーが出ないか
- [ ] Railway Logs の先頭に `Listening on 0.0.0.0:$PORT` が出ているか
- [ ] `ModuleNotFoundError` or `ImportError` が Logs に出ていないか
- [ ] `DJANGO_SETTINGS_MODULE=workpro.settings` が環境変数に設定されているか（Railway）
- [ ] Procfile の `web:` コマンドに `cd` が残っていないか

---

## 🔧 **よくある修正パターン**

### パターン A1-修正: Procfile に DJANGO_SETTINGS_MODULE を明示

```procfile
web: DJANGO_SETTINGS_MODULE=workpro.settings gunicorn workpro.wsgi --bind 0.0.0.0:$PORT --workers 2
release: python manage.py migrate && python manage.py collectstatic --noinput
```

### パターン A2-修正: wsgi.py を確認

```python
# workpro/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workpro.settings')
application = get_wsgi_application()
```

### パターン A3-修正: Root Directory を明確に

Railway Dashboard → Settings → Root Directory
```
(空白 = repo root)  ← これ推奨
```

---
