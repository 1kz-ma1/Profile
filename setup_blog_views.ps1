# ブログビュー切り替え機能 セットアップスクリプト

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "ブログビュー切り替え機能 セットアップ" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Python環境の確認
$pythonCmd = "C:/web_work/Scripts/python.exe"
Write-Host "[1/4] Python環境を確認中..." -ForegroundColor Yellow
if (Test-Path $pythonCmd) {
    Write-Host "✓ Python環境が見つかりました" -ForegroundColor Green
} else {
    Write-Host "✗ Python環境が見つかりません" -ForegroundColor Red
    exit 1
}

# 必要なパッケージのインストール
Write-Host ""
Write-Host "[2/4] 必要なパッケージをインストール中..." -ForegroundColor Yellow
Write-Host "注意: インストールには数分かかる場合があります" -ForegroundColor Gray

try {
    & $pythonCmd -m pip install --quiet --upgrade pip
    & $pythonCmd -m pip install --quiet -r requirements.txt
    Write-Host "✓ パッケージのインストールが完了しました" -ForegroundColor Green
} catch {
    Write-Host "✗ パッケージのインストールに失敗しました" -ForegroundColor Red
    Write-Host "手動でインストールしてください: $pythonCmd -m pip install -r requirements.txt" -ForegroundColor Yellow
}

# マイグレーションの実行
Write-Host ""
Write-Host "[3/4] データベースマイグレーションを実行中..." -ForegroundColor Yellow

try {
    & $pythonCmd manage.py makemigrations intro
    & $pythonCmd manage.py migrate
    Write-Host "✓ マイグレーションが完了しました" -ForegroundColor Green
} catch {
    Write-Host "✗ マイグレーションに失敗しました" -ForegroundColor Red
    Write-Host "手動で実行してください: $pythonCmd manage.py migrate" -ForegroundColor Yellow
}

# 静的ファイルの収集（本番環境用）
Write-Host ""
Write-Host "[4/4] 静的ファイルを収集中（スキップ可）..." -ForegroundColor Yellow
$collectStatic = Read-Host "静的ファイルを収集しますか？ (y/N)"
if ($collectStatic -eq "y" -or $collectStatic -eq "Y") {
    try {
        & $pythonCmd manage.py collectstatic --noinput
        Write-Host "✓ 静的ファイルの収集が完了しました" -ForegroundColor Green
    } catch {
        Write-Host "⚠ 静的ファイルの収集をスキップしました" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ 静的ファイルの収集をスキップしました" -ForegroundColor Yellow
}

# 完了メッセージ
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "セットアップが完了しました！" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "1. 開発サーバーを起動: $pythonCmd manage.py runserver" -ForegroundColor White
Write-Host "2. ブラウザでアクセス: http://localhost:8000/blog/" -ForegroundColor White
Write-Host "3. 管理画面で記事を編集: http://localhost:8000/admin/" -ForegroundColor White
Write-Host "   - セクション名（例: 資格、技術、プロジェクトなど）を自由に入力できます" -ForegroundColor Cyan
Write-Host ""
Write-Host "詳細は BLOG_VIEW_SWITCHER_GUIDE.md を参照してください" -ForegroundColor Gray
Write-Host ""

# サーバー起動の確認
$runServer = Read-Host "開発サーバーを起動しますか？ (y/N)"
if ($runServer -eq "y" -or $runServer -eq "Y") {
    Write-Host ""
    Write-Host "開発サーバーを起動しています..." -ForegroundColor Green
    Write-Host "終了するには Ctrl+C を押してください" -ForegroundColor Gray
    Write-Host ""
    & $pythonCmd manage.py runserver
}
