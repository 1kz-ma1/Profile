# Railway Logs 確認チェックリスト

## 🔍 **確認すべき項目**

現在、Railway で Procfile 修正（`DJANGO_SETTINGS_MODULE=workpro.settings` 追加）がデプロイされている状態です。

以下を Railway Dashboard で確認してください：

### Railway Dashboard での確認手順

1. **Railway.app にログイン**
2. **Project 選択**
3. **Deployments タブ** を開く
4. **Latest（最新）のデプロイ** をクリック
5. **Logs** タブで以下を検索

---

## ✅ **成功の目印（以下が出ていたら解決）**

```
Running release command...
Operations to perform:
  Apply all migrations: ...
Applying admin.0001_initial... OK
Applying auth.0001_initial... OK
Applying contenttypes.0001_initial... OK
...
Applying intro.0001_initial... OK
...
Running migrations:
  ...
Collecting static files...
151 static files copied to '...staticfiles'

Starting gunicorn 21.2.0
Listening on 0.0.0.0:8000
Worker spawned (pid: 1234)
Worker spawned (pid: 5678)
```

この場合 → **502 は解決、本番環境テストへ進む** ✅

---

## ⚠️ **まだエラーが出ている場合（以下を探してください）**

### パターン 1: ImproperlyConfigured エラー

```
django.core.exceptions.ImproperlyConfigured: Requested setting DEBUG, 
but settings are not configured. You must either define the environment 
variable DJANGO_SETTINGS_MODULE or call settings.configure()
```

→ **原因**: Procfile の修正がまだ反映されていない、または環境変数が上書きされている

**対策**:
```
Railway Dashboard → Deployments → Re-run を クリック（再デプロイ）
```

---

### パターン 2: ImportError / ModuleNotFoundError

```
ModuleNotFoundError: No module named 'workpro'
ImportError: cannot import name 'application' from 'workpro.wsgi'
```

→ **原因**: Python パスの問題、または wsgi.py にバグ

**対策**:
1. `workpro/wsgi.py` の末尾に `application = get_wsgi_application()` があるか確認
2. Procfile に `cd` が残っていないか確認
3. Root Directory が空（= repo root）か確認

---

### パターン 3: connection dial timeout（502 が続く）

```
upstreamErrors: [
  {"error":"connection dial timeout", "duration":5000} × 3
]
```

→ **原因**: gunicorn が起動する前にクラッシュしている、または timeout 時間が短すぎる

**対策**:
- Procfile に `--timeout 60` が含まれているか確認
- `DJANGO_SETTINGS_MODULE=workpro.settings` が含まれているか確認

---

### パターン 4: Worker timeout / Worker failed to boot

```
Worker failed to boot: ...
Worker timeout (pid: 1234) ...
```

→ **原因**: release フェーズ（migrate）が長すぎてタイムアウト

**対策**:
- `--timeout` を 120 に増やす
- Railway で直接 Shell で `python manage.py migrate` を実行（Pre-deploy Command を使う）

---

## 📋 **Logs を見る手順（画面遷移）**

1. Railway.app → Project 選択
2. 「Deployments」タブ
3. リスト一番上の Latest deployment をクリック
4. 「Logs」を選択
5. ページ上部から下部へスクロール

---

## 🎯 **いますぐやること**

**以下のスクリーンショットまたはテキストを報告してください:**

```
Railway Dashboard → Deployments → Latest → Logs
↓
以下の部分を全部コピペ：

[スクロール一番上から]
...
[スクロール一番下まで]
```

または、以下の短い質問に答えてください：

- [ ] `Listening on 0.0.0.0:8000` が出ている？ (はい / いいえ)
- [ ] `Traceback` エラーが出ている？ (はい / いいえ)
- [ ] 502 がまだ出ている？ (はい / いいえ)
- [ ] ページが 200/404 で返るようになった？ (はい / いいえ)

---
