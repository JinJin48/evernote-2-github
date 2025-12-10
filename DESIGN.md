# システム設計書
# Evernote to GitHub 自動同期システム

**作成日**: 2025-12-11  
**作成者**: JinJin48  
**バージョン**: 1.0

---

## 📑 目次

1. [システム概要](#システム概要)
2. [システムアーキテクチャ](#システムアーキテクチャ)
3. [技術仕様](#技術仕様)
4. [データフロー](#データフロー)
5. [実装詳細](#実装詳細)
6. [運用フロー](#運用フロー)
7. [エラーハンドリング](#エラーハンドリング)
8. [セキュリティ](#セキュリティ)
9. [今後の拡張](#今後の拡張)

---

## システム概要

### 目的

Evernoteで管理しているSAP関連ノートを、GitHubでバージョン管理・検索可能にする。

### 要件

| 項目 | 内容 |
|------|------|
| **入力** | Evernote ENEX形式ファイル |
| **出力** | Markdown + 添付ファイル |
| **頻度** | 週1回（手動トリガー） |
| **自動化** | GitHub Actions |
| **タグ対応** | 最大2タグ、フォルダ振り分け |

### 制約事項

- タグは2つまで（"SAP"含む）
- 3つ以上のタグはエラー
- ENEXファイルサイズ：GitHub制限（100MB）以下
- Private リポジトリ（機密情報保護）

---

## システムアーキテクチャ

### 全体構成図
```
┌─────────────┐
│  Evernote   │
│  (ローカル) │
└──────┬──────┘
       │ 手動エクスポート（週1回）
       │ .enex ファイル
       ↓
┌─────────────────────┐
│  GitHub Repository  │
│  input_sap/         │
└──────┬──────────────┘
       │ プッシュ検知
       │ Webhook トリガー
       ↓
┌─────────────────────┐
│  GitHub Actions     │
│  (Ubuntu Runner)    │
│  ┌─────────────┐    │
│  │ Python 3.11 │    │
│  │ convert_enex│    │
│  └─────────────┘    │
└──────┬──────────────┘
       │ 自動コミット
       ↓
┌─────────────────────┐
│  GitHub Repository  │
│  SAP_Materials/     │
│  ├─ *.md            │
│  └─ */attachments/  │
└─────────────────────┘
```

### コンポーネント構成

| コンポーネント | 役割 | 技術 |
|---------------|------|------|
| **入力層** | ENEXファイル受付 | GitHub Web UI / Git CLI |
| **処理層** | ENEX→Markdown変換 | Python 3.11 |
| **自動化層** | ワークフロー管理 | GitHub Actions |
| **出力層** | Markdown保存 | GitHub Repository |

---

## 技術仕様

### 使用技術

| 技術 | バージョン | 用途 |
|------|-----------|------|
| Python | 3.11 | ENEXパース・変換 |
| GitHub Actions | - | CI/CD自動化 |
| Git | 2.52+ | バージョン管理 |
| Markdown | CommonMark | 出力形式 |

### Pythonライブラリ

| ライブラリ | 用途 |
|-----------|------|
| `xml.etree.ElementTree` | ENEX（XML）パース |
| `pathlib` | ファイルパス操作 |
| `base64` | 添付ファイルデコード |
| `re` | 正規表現処理 |
| `datetime` | 日時フォーマット |
| `hashlib` | ファイルハッシュ（将来用） |

### GitHub Actions 設定

**トリガー条件**:
```yaml
on:
  push:
    paths:
      - 'input_sap/*.enex'
  workflow_dispatch:
```

**実行環境**:
- OS: Ubuntu Latest
- Python: 3.11
- 実行時間: 約15-20秒

---

## データフロー

### 処理フロー図
```
[1. ENEXアップロード]
        ↓
[2. GitHub Actions起動]
        ↓
[3. ENEXファイル検出]
        ↓
[4. ノート単位で処理]
        ↓
    ┌───┴───┐
    │       │
[タグ検証] [内容変換]
    │       │
    ↓       ↓
[OK?]   [ENML→MD]
    │       │
    NO      ↓
    │   [添付処理]
    │       │
    ↓       ↓
[エラー] [フォルダ]
[ログ]   [振り分け]
    │       │
    └───┬───┘
        ↓
[5. Git コミット]
        ↓
[6. GitHub プッシュ]
```

### データ変換詳細

#### 入力（ENEX）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<en-export>
  <note>
    <title>ノートタイトル</title>
    <content>
      <![CDATA[<?xml version="1.0"?>
      <en-note>内容</en-note>]]>
    </content>
    <created>20251210T120000Z</created>
    <tag>SAP</tag>
    <tag>QM</tag>
    <resource>
      <data encoding="base64">...</data>
      <mime>application/pdf</mime>
    </resource>
  </note>
</en-export>
```

#### 出力（Markdown）
```markdown
# ノートタイトル

**タグ:** SAP, QM

**作成日:** 2025-12-10 12:00:00

**更新日:** 2025-12-10 15:30:00

---

本文内容...

## 添付ファイル

- 📄 [資料.pdf](./ノートタイトル_attachments/資料.pdf)
```

---

## 実装詳細

### ディレクトリ構造
```
SAP/
├── .github/
│   └── workflows/
│       └── convert.yml          # GitHub Actions設定
├── input_sap/
│   └── *.enex                   # 入力ENEXファイル
├── SAP_Materials/               # 出力先
│   ├── *.md                     # SAPタグのみ
│   ├── *_attachments/           # 添付ファイル
│   ├── QM/                      # SAP+QMタグ
│   │   ├── *.md
│   │   └── *_attachments/
│   ├── IBP/                     # SAP+IBPタグ
│   └── BTP/                     # SAP+BTPタグ
├── scripts/
│   └── convert_enex.py          # 変換スクリプト
├── .gitattributes
├── README.md
└── DESIGN.md                    # 本ドキュメント
```

### convert_enex.py 主要クラス・メソッド

#### ENEXConverter クラス

| メソッド | 機能 | 入力 | 出力 |
|---------|------|------|------|
| `__init__` | 初期化 | input_dir, output_dir | - |
| `convert_all` | 全ENEXファイル処理 | - | - |
| `convert_enex` | 単一ENEX処理 | Path | - |
| `process_note` | 単一ノート処理 | Element | - |
| `get_output_folder` | フォルダパス決定 | List[str] | Path |
| `enml_to_markdown` | ENML変換 | str | str |
| `process_attachments` | 添付ファイル処理 | Element, Path, str | str |
| `create_metadata` | メタデータ生成 | 各種 | str |

#### タグ別フォルダ振り分けロジック
```python
def get_output_folder(self, tags):
    if len(tags) == 1:  # "SAP"のみ
        return self.output_dir
    else:  # "SAP" + その他1つ
        other_tag = [t for t in tags if t != "SAP"][0]
        return self.output_dir / other_tag
```

#### ENML→Markdown変換

**変換ルール**:

| ENML | Markdown |
|------|----------|
| `<h1>` | `# ` |
| `<h2>` | `## ` |
| `<h3>` | `### ` |
| `<b>`, `<strong>` | `**text**` |
| `<i>`, `<em>` | `*text*` |
| `<a href="">` | `[text](url)` |
| `<ul><li>` | `- item` |
| `<br/>` | 改行 |

---

## 運用フロー

### 週次同期フロー
```
[月曜朝 9:00]
     ↓
[Evernote起動]
     ↓
[タグ「SAP」選択]
     ↓
[Ctrl+A 全選択]
     ↓
[右クリック→エクスポート]
     ↓
[ENEX・タグ含める✓]
     ↓
[sap_notes.enex 保存]
     ↓
[GitHub input_sap/ アップロード]
     ↓
[Commit & Push]
     ↓
[GitHub Actions 自動実行]
 (約15-20秒)
     ↓
[SAP_Materials/ 更新完了]
     ↓
[完了通知確認]
```

### 所要時間

| 作業 | 時間 |
|------|------|
| Evernoteエクスポート | 1分 |
| GitHubアップロード | 30秒 |
| 自動変換（待機） | 20秒 |
| **合計** | **約2分** |

---

## エラーハンドリング

### エラー分類

| エラー種別 | 原因 | 対処法 |
|-----------|------|--------|
| **タグエラー** | タグ3つ以上 | Evernoteでタグを2つ以下に修正 |
| **ファイル名エラー** | 長すぎるファイル名 | 自動で200文字に切り詰め |
| **添付ファイルエラー** | デコード失敗 | ログ出力、処理継続 |
| **GitHub Actionsエラー** | 権限不足 | Settings→Actions→Write権限確認 |

### エラーログ出力

**GitHub Actions ログ**:
```
⚠️  ERRORS DETECTED:
❌ ノート"タイトル": タグが3つ以上あります。
   "SAP"タグを含め2つまでにして下さい。
   （現在のタグ: SAP, QM, IBP）
```

### リカバリー手順

1. **エラー確認**: GitHub Actions ログを確認
2. **原因特定**: エラーメッセージから原因を特定
3. **Evernote修正**: 該当ノートのタグを修正
4. **再エクスポート**: 修正後、再度エクスポート
5. **再実行**: GitHub にアップロード

---

## セキュリティ

### アクセス制御

| 項目 | 設定 |
|------|------|
| **リポジトリ** | Private |
| **Actions権限** | Read and write |
| **コラボレーター** | 個人のみ |
| **ブランチ保護** | なし（個人運用） |

### 機密情報管理

- **認証情報**: GitHub Secrets（不使用）
- **APIキー**: なし（OAuth不使用）
- **個人情報**: Private リポジトリで保護

### データ保護

- **バージョン管理**: Git履歴で全変更追跡
- **バックアップ**: GitHub上に永続保存
- **ローカルコピー**: `git clone` でいつでも復元可能

---

## 今後の拡張

### Phase 2: 機能拡張

| 機能 | 優先度 | 実装難易度 |
|------|--------|-----------|
| 全文検索機能 | 高 | 中 |
| タグ3つ以上対応 | 中 | 低 |
| 増分同期 | 高 | 高 |
| Web UI追加 | 低 | 高 |
| Slack通知 | 中 | 低 |

### Phase 3: 完全自動化

**OAuth実装によるAPI連携**:
- Evernote API直接アクセス
- 手動エクスポート不要
- リアルタイム同期

**実装コスト**:
- 開発時間: 6-8時間
- 学習コスト: OAuth 2.0
- メンテナンス: 定期的なトークン更新

---

## 付録

### 参考リンク

| 項目 | URL |
|------|-----|
| GitHub Actions公式 | https://docs.github.com/actions |
| Evernote API | https://dev.evernote.com/ |
| Markdown仕様 | https://commonmark.org/ |

### 用語集

| 用語 | 説明 |
|------|------|
| **ENEX** | Evernote Export形式（XML） |
| **ENML** | Evernote Markup Language（HTML類似） |
| **Webhook** | イベント駆動型HTTP通知 |
| **Runner** | GitHub Actions実行環境 |
| **Workflow** | 自動化処理の定義 |

### 変更履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2025-12-11 | 1.0 | 初版作成 |

---

**作成者**: JinJin48  
**最終更新**: 2025-12-11
