# デプロイ手順（PythonAnywhere - 無料プラン）

## 1. PythonAnywhereアカウント作成
1. https://www.pythonanywhere.com/ にアクセス
2. 「Start running Python online in less than a minute!」から無料アカウント作成
3. メール認証を完了

## 2. GitHubからコードを取得
PythonAnywhereのBashコンソールで:
```bash
git clone https://github.com/1kz-ma1/Profile.git
cd Profile
```

## 3. 仮想環境の作成とパッケージインストール
```bash
mkvirtualenv --python=/usr/bin/python3.10 mysite
pip install -r requirements.txt
```

## 4. 環境変数の設定
Bashコンソールで `.env` ファイルを作成:
```bash
nano .env
```

以下を入力（Ctrl+O で保存、Ctrl+X で終了）:
```
DEBUG=False
SECRET_KEY=新しいランダムな文字列を生成
EMAIL_HOST_USER=kazuma012023@gmail.com
EMAIL_HOST_PASSWORD=wewy yegw eqbs kyhc
ALLOWED_HOSTS=ユーザー名.pythonanywhere.com
```

SECRET_KEYの生成:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 5. データベースのセットアップ
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 6. Web アプリの設定
1. PythonAnywhere ダッシュボードの「Web」タブをクリック
2. 「Add a new web app」をクリック
3. 「Manual configuration」を選択（Python 3.10）
4. 「Code」セクション:
   - Source code: `/home/ユーザー名/Profile`
   - Working directory: `/home/ユーザー名/Profile`
5. 「Virtualenv」セクション:
   - `/home/ユーザー名/.virtualenvs/mysite`

## 7. WSGI設定ファイルの編集
WSGIファイル（リンクをクリック）を以下のように編集:

```python
import os
import sys

path = '/home/ユーザー名/Profile'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'workpro.settings'

# 環境変数の読み込み
from pathlib import Path
env_file = Path(path) / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ.setdefault(key, value)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 8. 静的ファイルの設定
「Web」タブの「Static files」セクション:
- URL: `/static/`  Path: `/home/ユーザー名/Profile/staticfiles`
- URL: `/media/`  Path: `/home/ユーザー名/Profile/media`

## 9. リロードして完了
「Reload」ボタンをクリック

サイトURL: `https://ユーザー名.pythonanywhere.com`

---

## トラブルシューティング
- エラーログ: 「Web」タブの「Log files」から確認
- Bashコンソールで `python manage.py check --deploy` を実行して問題をチェック

## その他の選択肢
- **Render**: https://render.com/ （PostgreSQL使用、自動デプロイ）
- **Railway**: https://railway.app/ （簡単デプロイ、クレジット制）
