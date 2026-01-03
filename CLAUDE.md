# CLAUDE.md

このファイルはClaude Codeがこのリポジトリで作業する際のガイドです。

## プロジェクト概要

Evernoteノート（ENEX形式）をMarkdownに変換し、GitHubでバージョン管理するシステム。

### 主な機能

- ENEX→Markdown自動変換
- タグベースのフォルダ振り分け（最大2タグ）
- 添付ファイル（PDF, Excel, 画像等）の抽出・保存
- GitHub Actionsによる自動変換・コミット

### 制約事項

- タグは「# SAP」を含め最大2つまで
- 3つ以上のタグがあるノートはスキップ
- ENEXファイルサイズ: 100MB以下

## ディレクトリ構造

```
evernote-2-github/
├── .github/
│   └── workflows/
│       └── convert.yml          # GitHub Actions ワークフロー
├── input_sap/
│   └── .gitkeep                 # ENEXファイルアップロード先
├── SAP_Materials/
│   └── .gitkeep                 # 変換後Markdown出力先
├── scripts/
│   ├── .gitkeep
│   └── convert_enex.py          # ENEX→Markdown変換スクリプト
├── .gitattributes
├── CLAUDE.md                    # 本ファイル
├── DESIGN.md                    # システム設計書（詳細仕様）
└── README.md                    # ユーザー向けドキュメント
```

## 技術スタック

| 技術 | バージョン | 用途 |
|------|-----------|------|
| Python | 3.11+ | ENEX変換スクリプト |
| GitHub Actions | - | CI/CD自動化 |
| Git | 2.0+ | バージョン管理 |

### Pythonライブラリ（標準ライブラリのみ）

- `xml.etree.ElementTree` - ENEXパース
- `base64` - 添付ファイルデコード
- `pathlib` - パス操作
- `re` - 正規表現
- `datetime` - 日時処理
- `hashlib` - ハッシュ計算

## 現在の開発状況

### 完了済み

- 基本的なENEX→Markdown変換機能
- タグベースフォルダ振り分け（2タグまで）
- 添付ファイル抽出・保存
- GitHub Actions自動化ワークフロー
- エラーハンドリング（タグ数超過時のスキップ）

### 既知の課題

- タグ3つ以上は非対応（エラースキップ）
- 増分同期非対応（毎回全ノート処理）

## 今後の予定

### Phase 2: 機能拡張

| 機能 | 優先度 |
|------|--------|
| 全文検索機能 | 高 |
| 増分同期 | 高 |
| タグ3つ以上対応 | 中 |
| Slack通知 | 中 |

### Phase 3: 完全自動化

- Evernote OAuth API連携
- 手動エクスポート不要化
- リアルタイム同期

## 開発時の注意事項

### コマンド

```bash
# ローカルで変換実行
python scripts/convert_enex.py

# テスト用ENEXファイル配置
cp /path/to/notes.enex input_sap/
```

### タグ命名規則

- メインタグ: `# SAP`
- サブタグ例: `# S/4-QM`, `# SAP-IBP`, `# SAP-BTP`

### 変換フロー

1. `input_sap/` にENEXファイル配置
2. GitHub Actionsまたはローカルでスクリプト実行
3. `SAP_Materials/` に変換結果出力
