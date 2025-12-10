# SAP Evernote to GitHub Sync

Evernoteの「SAP」タグ付きノートを自動的にMarkdown形式に変換し、GitHubで管理するシステム。

## 📋 概要

- **目的**: EvernoteノートをGitHubでバージョン管理・検索可能にする
- **変換形式**: ENEX → Markdown
- **自動化**: GitHub Actionsによる自動変換
- **タグ別整理**: タグに応じてフォルダに自動振り分け

## 📁 フォルダ構造
```
SAP/
├── input_sap/              # ENEXファイルアップロード先
├── SAP_Materials/          # 変換後のMarkdownファイル
│   ├── (SAPのみ).md       # "SAP"タグのみのノート
│   ├── QM/                 # "SAP" + "QM"タグのノート
│   ├── IBP/                # "SAP" + "IBP"タグのノート
│   └── BTP/                # "SAP" + "BTP"タグのノート
├── scripts/                # 変換スクリプト
│   └── convert_enex.py
└── .github/workflows/      # 自動化設定
    └── convert.yml
```

## 🚀 使い方（週1回・約2分）

### Step 1: Evernoteからエクスポート

1. Evernoteアプリを起動
2. 左サイドバー「タグ」→「SAP」を選択
3. **Ctrl+A** で全選択
4. 右クリック→「ノートをエクスポート」
5. 形式：**ENEX形式（.enex）**
6. **「タグを含める」にチェック✓**
7. ファイル名：`sap_notes.enex`
8. 保存

### Step 2: GitHubにアップロード

#### 方法A: Web UI（簡単）

1. https://github.com/JinJin48/SAP にアクセス
2. `input_sap` フォルダをクリック
3. 「Add file」→「Upload files」
4. `sap_notes.enex` をドラッグ＆ドロップ
5. 「Commit changes」

#### 方法B: Git コマンド
```bash
cd /path/to/SAP
cp ~/Desktop/sap_notes.enex input_sap/
git add input_sap/sap_notes.enex
git commit -m "Update SAP notes"
git push origin main
```

### Step 3: 自動変換を確認

1. [Actions](https://github.com/JinJin48/SAP/actions) タブで実行状況を確認
2. 完了後、`SAP_Materials/` フォルダに変換結果が保存される

## ⚙️ システム仕様

### タグルール

| タグの組み合わせ | 保存先 |
|-----------------|--------|
| `["SAP"]` | `SAP_Materials/` |
| `["SAP", "QM"]` | `SAP_Materials/QM/` |
| `["SAP", "IBP"]` | `SAP_Materials/IBP/` |
| `["SAP", "BTP"]` | `SAP_Materials/BTP/` |

### エラー条件

- **タグが3つ以上**: エラーメッセージを出力してスキップ
```
  ノート上のタグが3つ以上あります。"SAP"タグを含め2つまでにして下さい。
```

### 添付ファイル

- PDF, Excel, PowerPoint等はそのまま保存
- `{ノート名}_attachments/` フォルダに格納
- Markdown内にリンク形式で記載

## 🔧 トラブルシューティング

### ワークフローが実行されない

**原因**: `.enex` ファイルが更新されていない

**対処法**: 
- Actions タブで手動実行
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
3. 再エクスポート

### 変換結果が表示されない

**原因**: ブラウザキャッシュ

**対処法**: ページをリロード（F5キー）

## 🛠️ 技術スタック

- **Python 3.11**: ENEX→Markdown変換
- **GitHub Actions**: 自動化ワークフロー
- **Git**: バージョン管理

## 📝 メンテナンス

### スクリプト更新

`scripts/convert_enex.py` を編集後：
```bash
git add scripts/convert_enex.py
git commit -m "Update conversion script"
git push origin main
```

### ワークフロー更新

`.github/workflows/convert.yml` を編集後：
```bash
git add .github/workflows/convert.yml
git commit -m "Update workflow"
git push origin main
```

## 📄 ライセンス

Private Repository - Personal Use Only

## 👤 作成者

JinJin48

---

**最終更新**: 2025-12-11
