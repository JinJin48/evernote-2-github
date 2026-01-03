# Evernote to GitHub Sync

EvernoteノートをMarkdown形式に変換し、GitHubで管理するシステム。

## 概要

### プロジェクトの目的

EvernoteでタグづけしたノートをGitHub上でバージョン管理・検索可能にする。

### 主な機能

- **ENEX→Markdown変換**: EvernoteのENEX形式をMarkdownに自動変換
- **タグベース振り分け**: タグに応じてフォルダへ自動整理
- **添付ファイル対応**: PDF, Excel, PowerPoint, 画像等をそのまま保存
- **GitHub Actions自動化**: ENEXファイルプッシュで自動変換・コミット

### 制約事項

- タグは最大2つまで（メインタグ + サブタグ）
- 3つ以上のタグがあるノートはスキップ
- ENEXファイルサイズ: 100MB以下（GitHub制限）

---

## ディレクトリ構造

```
evernote-2-github/
├── .github/
│   └── workflows/
│       └── convert.yml          # GitHub Actions設定
├── input_sap/
│   └── *.enex                   # 入力ENEXファイル
├── SAP_Materials/               # 変換後の出力先
│   ├── *.md                     # メインタグのみのノート
│   ├── *_attachments/           # 添付ファイル
│   └── {サブタグ名}/            # サブタグ付きノート
│       ├── *.md
│       └── *_attachments/
├── scripts/
│   └── convert_enex.py          # 変換スクリプト
├── .gitattributes
├── DESIGN.md                    # システム設計書
└── README.md
```

---

## 依存関係

### 実行環境

| 項目 | バージョン |
|------|-----------|
| Python | 3.11+ |
| Git | 2.0+ |

### Pythonライブラリ

すべてPython標準ライブラリのため、追加インストールは不要。

| ライブラリ | 用途 |
|-----------|------|
| `xml.etree.ElementTree` | ENEXファイル（XML）のパース |
| `base64` | 添付ファイルのデコード |
| `pathlib` | ファイルパス操作 |
| `re` | 正規表現処理 |
| `datetime` | 日時フォーマット |
| `hashlib` | ファイルハッシュ計算 |

---

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/JinJin48/evernote-2-github.git
cd evernote-2-github
```

### 2. 依存関係の確認

```bash
python --version  # Python 3.11以上を確認
```

---

## 使い方

### Step 1: Evernoteからエクスポート

1. Evernoteアプリを起動
2. 左サイドバー「タグ」→ 対象タグを選択
3. **Ctrl+A** で全選択
4. 右クリック → 「ノートをエクスポート」
5. 形式: **ENEX形式（.enex）**
6. **「タグを含める」にチェック**
7. ファイル保存

### Step 2: ENEXファイルをアップロード

#### 方法A: Web UI

1. GitHubリポジトリにアクセス
2. `input_sap` フォルダをクリック
3. 「Add file」→「Upload files」
4. ENEXファイルをドラッグ＆ドロップ
5. 「Commit changes」

#### 方法B: Git CLI

```bash
cp /path/to/notes.enex input_sap/
git add input_sap/
git commit -m "Add ENEX file"
git push origin main
```

### Step 3: 自動変換を確認

1. [Actions](../../actions) タブで実行状況を確認
2. 完了後、`SAP_Materials/` フォルダに変換結果が保存される

### ローカルで実行する場合

```bash
python scripts/convert_enex.py
```

---

## タグルール

| タグの組み合わせ | 保存先 |
|-----------------|--------|
| `["# SAP"]` | `SAP_Materials/` |
| `["# SAP", "# S4-QM"]` | `SAP_Materials/# S4-QM/` |
| `["# SAP", "# SAP-IBP"]` | `SAP_Materials/# SAP-IBP/` |
| `["# SAP", "# SAP-BTP"]` | `SAP_Materials/# SAP-BTP/` |

**注意**: タグが3つ以上の場合、以下のエラーメッセージが出力されスキップされます。

```
ノート上のタグが3つ以上あります。"# SAP"タグを含め2つまでにして下さい。
```

---

## システム仕様

### GitHub Actions トリガー

- `input_sap/*.enex` ファイルのプッシュ時に自動実行
- 手動実行も可能（workflow_dispatch）

### 変換処理

1. ENEXファイル検出
2. 各ノートを処理
   - タグ検証（2つ以下）
   - ENML→Markdown変換
   - 添付ファイル抽出
   - フォルダ振り分け
3. 自動コミット＆プッシュ

### 添付ファイル対応

| ファイル種別 | 拡張子 |
|-------------|--------|
| PDF | `.pdf` |
| Excel | `.xls`, `.xlsx` |
| PowerPoint | `.ppt`, `.pptx` |
| Word | `.doc`, `.docx` |
| 画像 | `.png`, `.jpg`, `.gif` |

---

## トラブルシューティング

### ワークフローが実行されない

**対処法**:
- Actionsタブで手動実行
- または空コミットでトリガー

```bash
git commit --allow-empty -m "Trigger workflow"
git push origin main
```

### タグエラーが出る

**原因**: ノートに3つ以上のタグが付いている

**対処法**:
1. Actions ログでエラーノートを確認
2. Evernoteで該当ノートのタグを2つ以下に修正
3. 再エクスポート＆アップロード

### 変換結果が表示されない

**対処法**: ページをリロード（F5キー）

---

## ライセンス

Private Repository - Personal Use Only

## 作成者

JinJin48

---

**最終更新**: 2026-01-04
