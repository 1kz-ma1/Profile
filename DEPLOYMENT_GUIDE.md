# Vercel + Railway デプロイメント手順

## バックエンド（Django / Railway）

### 1. Railway プロジェクト作成

1. [Railway.app](https://railway.app) にアクセス
2. GitHub 認証でログイン
3. 「New Project」 → 「Deploy from GitHub」 を選択
4. このリポジトリを選択
5. Environment variables を設定

### 2. 環境変数設定（Railway Dashboard）

```
DATABASE_URL=postgresql://username:password@host:port/dbname
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**注意**: `DEBUG=False` は本番環境では必須です。

### 3. データベース接続

1. Railway Dashboard で「PostgreSQL」サービスを追加
2. `DATABASE_URL` は自動的に環境変数に設定されます

## フロント（Next.js / Vercel）

### 1. Vercel プロジェクト作成

1. [Vercel](https://vercel.com) にアクセス
2. GitHub 認証でログイン
3. 「Add New」 → 「Project」 を選択
4. このリポジトリを選択
5. Root Directory を `frontend` に設定
6. Environment variables を設定

### 2. 環境変数設定（Vercel Dashboard）

```
NEXT_PUBLIC_API_URL=https://your-domain.railway.app
```

### 3. デプロイメント

自動: GitHub にプッシュすると自動デプロイ

## CORS設定

Django バックエンド（settings.py）に以下が設定済み：

```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.vercel.app',
]
```

フロント側でAPIリクエストを送る場合：

```javascript
// frontend/lib/api.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchFromAPI(endpoint) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    credentials: 'include', // CSRF トークン対応
  });
  return response.json();
}
```

## トラブルシューティング

### CORS エラーが出る場合
- Railway の環境変数 `ALLOWED_HOSTS` を確認
- Vercel の環境変数 `NEXT_PUBLIC_API_URL` を確認

### データベース接続エラー
- Railway の PostgreSQL が起動しているか確認
- `DATABASE_URL` が正しく設定されているか確認

### 静的ファイルが読み込まれない
- Django で `python manage.py collectstatic` を実行
- Railway の Procfile に release コマンドが含まれているか確認

## ローカル開発

### バックエンド
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### フロント
```bash
cd frontend
npm install
npm run dev
```

アクセス:
- バックエンド API: http://localhost:8000
- フロント: http://localhost:3000
