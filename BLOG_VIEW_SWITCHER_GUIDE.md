# ブログビュー切り替え機能 実装ガイド

## 概要

ブログ一覧ページに3つのビュー切り替え機能を追加しました：

1. **グリッド（⊞）**: 従来のカード型一覧表示
2. **章構成（☰）**: 章番号ごとにグループ化した構造的な表示
3. **相関図（∞）**: 記事間の関連性を視覚的に表現したマップ表示

## 実装内容

### 1. データベースモデルの拡張

**BlogPostモデルに追加されたフィールド** ([intro/models.py](intro/models.py))

```python
# 章番号（第1章、第2章など）
chapter_number = models.IntegerField(null=True, blank=True, verbose_name="章番号")

# 章内での表示順序
chapter_order = models.IntegerField(null=True, blank=True, verbose_name="章内順序")

# 分野タグ（カンマ区切り）
field_tags = models.CharField(max_length=200, blank=True, verbose_name="分野タグ")

# 関連記事（多対多）
related_posts = models.ManyToManyField('self', blank=True, symmetrical=True, verbose_name="関連記事")
```

### 2. ビュー機能

**変更されたファイル**: [intro/views.py](intro/views.py)

- `view_mode`パラメータでビューを切り替え
- 章構成ビューでは`chapter_number`と`chapter_order`でソート
- `related_posts`をprefetch_relatedで効率的に取得

### 3. テンプレート

**変更されたファイル**: [intro/templates/blog.html](intro/templates/blog.html)

#### 主要機能

##### ビュー切り替えボタン
```html
<button class="view-btn active" data-view="grid" role="tab" aria-selected="true">
    <span class="icon">⊞</span>
    <span>グリッド</span>
</button>
```

##### 状態管理（JavaScript）
- **URLクエリ**: `?view=grid|chapters|map`
- **localStorage**: `blog_view`キー
- **履歴管理**: ブラウザバック/フォワード対応

##### 遅延レンダリング
- グリッドビュー: 初期表示（即時）
- 章構成ビュー: 初回アクセス時に生成
- 相関図ビュー: 初回アクセス時にMermaid.jsで生成

### 4. 管理画面

**変更されたファイル**: [intro/admin.py](intro/admin.py)

新しいフィールドセット「ビュー切り替え用設定」を追加：
- 章番号・章内順序の設定
- 分野タグの入力
- 関連記事の選択（filter_horizontal）

## セットアップ手順

### 1. マイグレーションの実行

```bash
cd c:\web_work\Scripts\workpro
C:/web_work/Scripts/python.exe manage.py migrate
```

実行されるマイグレーション：
- `0006_add_category_subcategory_models.py`: カテゴリ/サブカテゴリモデル
- `0007_populate_dx_categories.py`: DXカテゴリとサブカテゴリのデータ
- `0008_add_view_switcher_fields.py`: ビュー切り替え用フィールド

### 2. 既存データの設定（オプション）

管理画面で既存の記事に以下を設定できます：
- 章番号を設定して章構成ビューで整理
- 関連記事を選択して相関図に表示
- 分野タグを追加してフィルタリング

### 3. サーバーの起動と確認

```bash
C:/web_work/Scripts/python.exe manage.py runserver
```

http://localhost:8000/blog/ にアクセス

## 使用方法

### ユーザー視点

#### グリッドビュー
- デフォルトのカード型表示
- カテゴリフィルター、並び替え、ページネーション対応
- モバイルフレンドリーなレスポンシブデザイン

#### 章構成ビュー
- 記事を章ごとにグループ化
- 各章内で順序付けられた表示
- 分野タグが表示される
- 長文コンテンツや連載記事に最適

#### 相関図ビュー
- Mermaid.jsによるインタラクティブな図
- 記事間の関連性を視覚化
- ノードクリックで記事詳細に遷移
- 関連記事が設定された記事のみ表示

### 管理者視点

#### 記事に章情報を設定

1. 管理画面でブログ記事を編集
2. 「ビュー切り替え用設定」セクションを展開
3. **章番号**を入力（例: 1 = 第1章）
4. **章内順序**を入力（例: 1, 2, 3...）
5. **分野タグ**をカンマ区切りで入力（例: `Python, Django, Web開発`）
6. **関連記事**を選択

#### 章構成の例

```
第1章: 基礎知識
  1. Pythonの基本（chapter_number=1, chapter_order=1）
  2. Django入門（chapter_number=1, chapter_order=2）
  3. データベース設計（chapter_number=1, chapter_order=3）

第2章: 実践編
  1. RESTful API作成（chapter_number=2, chapter_order=1）
  2. 認証機能の実装（chapter_number=2, chapter_order=2）
```

## 技術仕様

### アクセシビリティ

- **ARIA対応**: role="tab", aria-selected, aria-controls
- **キーボード操作**: Enter/Spaceキーでビュー切り替え
- **フォーカス管理**: outline表示で視覚的フィードバック
- **セマンティックHTML**: 適切なsection, article, nav要素

### パフォーマンス最適化

- **遅延レンダリング**: 初回アクセス時のみ描画
- **状態キャッシュ**: localStorageで設定を保持
- **効率的なクエリ**: prefetch_relatedで関連データを一括取得
- **CDN利用**: Mermaid.jsをCDNから読み込み

### レスポンシブデザイン

```css
/* モバイル（375px〜） */
@media (max-width: 768px) {
    .view-btn {
        padding: 10px 16px;
        font-size: 0.9rem;
    }
    
    .chapter-post-item {
        flex-direction: column;
    }
}
```

### ブラウザ対応

- **モダンブラウザ**: Chrome, Firefox, Safari, Edge（最新版）
- **必要な機能**: ES6+, localStorage, History API
- **フォールバック**: JavaScriptが無効でもグリッドビューは表示

## API/データ構造

### URLパラメータ

```
# グリッドビュー（デフォルト）
/blog/
/blog/?view=grid

# 章構成ビュー
/blog/?view=chapters

# 相関図ビュー
/blog/?view=map

# 組み合わせ可能
/blog/?view=grid&category=tech&sort=-post_date&page=2
```

### JavaScript データ構造

```javascript
const blogPosts = [
    {
        id: 1,
        title: "記事タイトル",
        url: "/blog/1/",
        category: "技術",
        date: "2025/02/02",
        chapter: 1,
        chapterOrder: 1,
        fieldTags: ["Python", "Django"],
        relatedIds: [2, 3],
        likesCount: 10,
        excerpt: "記事の抜粋..."
    }
];
```

## トラブルシューティング

### 相関図が表示されない

**原因**: Mermaid.jsの読み込みエラー

**解決策**:
1. ブラウザのコンソールでエラー確認
2. CDN接続を確認
3. 関連記事が設定されているか確認

### 章構成ビューが空

**原因**: 記事に`chapter_number`が設定されていない

**解決策**:
1. 管理画面で記事を編集
2. 「章番号」フィールドに数値を入力
3. 未設定の記事は「未分類」セクションに表示

### ビュー切り替えが動作しない

**原因**: JavaScriptエラー

**解決策**:
1. ブラウザコンソールでエラー確認
2. テンプレートの`blogPosts`配列が正しく生成されているか確認
3. jQueryが読み込まれているか確認

### localStorageが機能しない

**原因**: プライベートブラウジングモードまたはCookie無効

**解決策**:
- URLクエリが代替として機能するため、基本的な動作は可能
- 通常モードでの使用を推奨

## カスタマイズ

### 新しいビューの追加

1. **ボタン追加**:
```html
<button class="view-btn" data-view="custom" role="tab">
    カスタム
</button>
```

2. **コンテナ追加**:
```html
<div id="custom-view" class="custom-view" role="tabpanel">
    <!-- カスタムコンテンツ -->
</div>
```

3. **レンダリング関数追加**:
```javascript
function renderCustomView() {
    const container = document.getElementById('custom-view');
    // レンダリングロジック
}
```

### スタイルのカスタマイズ

主要なCSS変数：
```css
.view-btn {
    --btn-bg: rgba(255, 255, 255, 0.2);
    --btn-active-bg: #667eea;
    --btn-hover-bg: rgba(255, 255, 255, 0.3);
}
```

## 今後の拡張案

1. **タイムラインビュー**: 時系列での視覚的表示
2. **タグクラウド**: 分野タグの出現頻度を視覚化
3. **検索機能**: 各ビュー内での絞り込み
4. **エクスポート機能**: 章構成をMarkdownでエクスポート
5. **アニメーション**: ビュー切り替え時のトランジション
6. **ドラッグ&ドロップ**: 相関図ビューでノードの配置変更

## 関連ファイル

- **モデル**: [intro/models.py](intro/models.py)
- **ビュー**: [intro/views.py](intro/views.py)
- **テンプレート**: [intro/templates/blog.html](intro/templates/blog.html)
- **管理画面**: [intro/admin.py](intro/admin.py)
- **マイグレーション**:
  - [0006_add_category_subcategory_models.py](intro/migrations/0006_add_category_subcategory_models.py)
  - [0007_populate_dx_categories.py](intro/migrations/0007_populate_dx_categories.py)
  - [0008_add_view_switcher_fields.py](intro/migrations/0008_add_view_switcher_fields.py)

## ライセンス・依存関係

- **Mermaid.js**: MIT License
- **jQuery**: MIT License
- **Django**: BSD License

---

実装完了日: 2026年2月2日
バージョン: 1.0.0
