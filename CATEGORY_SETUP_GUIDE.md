# カテゴリ機能拡張 - DXカテゴリとサブカテゴリ追加

## 実装内容

### 1. 新しいモデルの追加
- **Category**: メインカテゴリモデル
- **SubCategory**: サブカテゴリモデル（Categoryに紐づく）
- **BlogPost**: 既存モデルを拡張し、新しいカテゴリシステムに対応

### 2. 追加されたDXカテゴリとサブカテゴリ

**メインカテゴリ: DX**
- AI活用
- 医療DX
- 行政DX
- 教育DX
- 制度・マイナンバー
- 可視化モデル（Modeling）

### 3. 変更されたファイル

#### モデル (intro/models.py)
- `Category`: メインカテゴリを管理
- `SubCategory`: サブカテゴリを管理（親カテゴリとの紐づけ）
- `BlogPost`: 新しい`main_category`と`sub_category`フィールドを追加
  - 旧`category`フィールドは後方互換性のため保持

#### 管理画面 (intro/admin.py)
- CategoryAdmin: カテゴリの管理画面
- SubCategoryAdmin: サブカテゴリの管理画面
- BlogPostAdmin: サブカテゴリに対応した管理画面に更新

#### ビュー (intro/views.py)
- `blog`: メインカテゴリとサブカテゴリでのフィルタリングに対応

#### マイグレーション
- `0006_add_category_subcategory_models.py`: モデル変更のマイグレーション
- `0007_populate_dx_categories.py`: DXカテゴリとサブカテゴリのデータ作成

## セットアップ手順

### 1. 必要なパッケージのインストール（まだの場合）

```bash
cd c:\web_work\Scripts\workpro
C:/web_work/Scripts/python.exe -m pip install -r requirements.txt
```

### 2. マイグレーションの実行

```bash
cd c:\web_work\Scripts\workpro

# マイグレーションファイルの確認
C:/web_work/Scripts/python.exe manage.py showmigrations intro

# マイグレーションの適用
C:/web_work/Scripts/python.exe manage.py migrate intro

# または全体のマイグレーション
C:/web_work/Scripts/python.exe manage.py migrate
```

### 3. 管理画面での確認

1. サーバーを起動
```bash
C:/web_work/Scripts/python.exe manage.py runserver
```

2. 管理画面にアクセス: http://localhost:8000/admin/

3. 以下が追加されていることを確認:
   - **カテゴリ** セクション
   - **サブカテゴリ** セクション
   - **ブログ記事** のカテゴリフィールドが更新

## 使用方法

### 管理画面での記事作成

1. 管理画面で「ブログ記事」→「ブログ記事を追加」
2. 「メインカテゴリ」ドロップダウンから「DX」を選択
3. 「サブカテゴリ」ドロップダウンから該当するサブカテゴリを選択
   - AI活用
   - 医療DX
   - 行政DX
   - 教育DX
   - 制度・マイナンバー
   - 可視化モデル（Modeling）

### カテゴリフィルタリング（フロントエンド）

URLパラメータでフィルタリング可能:

```
# メインカテゴリでフィルタ
/blog/?main_category=dx

# サブカテゴリでフィルタ
/blog/?main_category=dx&sub_category=ai-utilization

# 旧カテゴリでフィルタ（後方互換性）
/blog/?category=tech
```

## データベースの後方互換性

- 既存のブログ記事は旧`category`フィールドを保持
- 新しい記事では`main_category`と`sub_category`を使用
- `get_category_display_name()`メソッドが自動的に適切なカテゴリ名を返す

## テンプレートでの使用

```django
<!-- カテゴリ表示 -->
{{ post.get_category_display_name }}

<!-- メインカテゴリへのリンク -->
<a href="{% url 'blog' %}?main_category={{ post.main_category.slug }}">
    {{ post.main_category.name }}
</a>

<!-- サブカテゴリへのリンク -->
{% if post.sub_category %}
<a href="{% url 'blog' %}?sub_category={{ post.sub_category.slug }}">
    {{ post.sub_category.name }}
</a>
{% endif %}
```

## 注意事項

1. **マイグレーションの実行**: 必ず`migrate`コマンドを実行してください
2. **既存データ**: 既存のブログ記事は影響を受けません
3. **カテゴリの管理**: 新しいカテゴリ/サブカテゴリは管理画面から追加可能
4. **テンプレート更新**: blog.htmlなどのテンプレートは必要に応じて更新してください

## トラブルシューティング

### マイグレーションエラーが発生する場合

```bash
# マイグレーションをリセット（注意: 開発環境のみ）
C:/web_work/Scripts/python.exe manage.py migrate intro zero
C:/web_work/Scripts/python.exe manage.py migrate intro
```

### カテゴリが表示されない場合

```bash
# 管理画面でカテゴリが作成されているか確認
# または手動でカテゴリを作成
```

## 今後の拡張

- サブカテゴリの動的フィルタリングUI
- カテゴリページの独立化
- カテゴリごとの記事数の表示
- サブカテゴリの階層化（必要に応じて）
