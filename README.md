# Django Portfolio Site

## ローカルでの起動方法

### 1. 環境変数の設定

`.env`ファイルを作成して、以下の内容を記述してください（`.env.example`を参考）:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### 2. PowerShellで環境変数を読み込んでサーバー起動

```powershell
# .env ファイルから環境変数を読み込む
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.+)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

# サーバー起動
python manage.py runserver
```

### 3. アクセス

ブラウザで `http://127.0.0.1:8000/` にアクセス

## 機能

- 動的ブログ（管理画面から投稿可能）
- お問い合わせフォーム（メール送信機能付き）
- ポートフォリオページ
- 自己紹介ページ

## 注意事項

- `.env`ファイルは`.gitignore`に含まれているため、GitHubにプッシュされません
- 本番環境では環境変数を別途設定してください
