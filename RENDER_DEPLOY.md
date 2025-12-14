# Render自動デプロイ手順（完全無料）

## 1. GitHubにプッシュ

```powershell
cd c:\web_work\Scripts\workpro
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

## 2. Renderアカウント作成（30秒）

1. https://render.com/ にアクセス
2. 「Get Started for Free」をクリック
3. **「Continue with GitHub」を選択**（最も簡単）
4. GitHubアカウントで認証

## 3. 自動デプロイ開始（2クリック）

1. Renderダッシュボードで「New +」→「Blueprint」を選択
2. GitHubリポジトリ「Profile」を選択
3. **自動的にデプロイが開始されます！**

## 4. 環境変数の設定（必須）

デプロイ中に「Environment」タブで以下を追加:

- `EMAIL_HOST_USER`: `kazuma012023@gmail.com`
- `EMAIL_HOST_PASSWORD`: `wewy yegw eqbs kyhc`

## 5. 完了！

- デプロイには約5-10分かかります
- 完了すると `https://あなたのアプリ名.onrender.com` でアクセス可能
- 管理画面: `https://あなたのアプリ名.onrender.com/admin/`

## 管理者アカウント作成

デプロイ後、Renderの「Shell」タブで実行:
```bash
python manage.py createsuperuser
```

---

## 注意事項

- **無料プランの制限**: 15分間アクセスがないとスリープします（初回アクセス時に数秒待ちます）
- **データベース**: 無料のPostgreSQLが自動で作成されます
- **更新**: GitHubにpushするだけで自動再デプロイされます

## トラブルシューティング

ログは Renderダッシュボードの「Logs」タブで確認できます。
