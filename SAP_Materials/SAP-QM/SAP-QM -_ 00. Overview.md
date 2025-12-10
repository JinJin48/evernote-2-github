# SAP-QM -_ 00. Overview

**タグ:** SAP, SAP-QM

---


## **Overview**
SAP QM(Quality Management)は、SAP ERPの品質管理モジュールで、製品やサービスの品質を計画・管理・保証するための統合システムです。調達、製造、販売の各プロセスで品質検査を実施し、品質データを一元管理します。### 主な特徴
- 
他モジュール(MM、PP、SD等)との統合- 
リアルタイムな品質情報の可視化- 
検査計画 (Inspection Plan) から結果記録まで一貫管理- 
品質証明書 (Quality Certificate) の自動発行
### 重要な概念
- 
**検査ロット (Inspection Lot)**: 品質検査の単位となるロット- 
**検査特性 (Inspection Characteristic)**: 検査する項目・特性- 
**使用決定 (Usage Decision)**: 検査結果に基づく在庫の可否判定- 
**品質通知 (Quality Notification)**: 不適合・クレーム管理の文書- 
**マスタ検査特性 (Master Inspection Characteristic, MIC)**: 検査特性のマスタデータ
## Businee Process

Category
Object
Master
Tran.
Table
Master Data
(マスタデータ)
Material Master
(品目マスタ)
MM01
MM02
MM03
-
MARA
MARC
Inspection Plan
(検査計画)
QP01
QP02
QP03
-
PLKO
PLPO
MAPL
Master Inspection Characteristic
(検査特性マスタ)
QS21
QS22
QS23
-
QMAT
QMTB
Vendor Master
(仕入先マスタ)
XK01
XK02
XK03
-
LFA1
LFM1
Inspection Execution
(検査実行)
Inspection Lot
(検査ロット)
-
QA01
QA02
QA03
QALS
QAVE
Sample
(サンプル)
-
QA01
QAPP
Inspection Result
(検査結果記録)
-
QE51
QE51N
QAER
QAMR
Inspection Resolution
(品質の判定)
Quality Notification
(品質通知)
-
QM01
QM02
QM03
QMEL
VIQMEL
Task
(タスク)
-
QM01
QMSM
Usage Decision
(使用判定)
-
QA11
QA12
QALS
QAVE
Stock Status
(在庫ステータス)
-
MMBE
MARD
MSKU
Analysis
(分析)
SPC Chart
(統計的工程管理図)
-
QGR1
QGR2
QPRS
QPRH
Certificate
(品質証明書)
-
QC01
QC02
QC03
QCPR
**## 他モジュールと連携した業務フロー**
購買発注 → 入荷 → 検査ロット作成→ 検査実施→ 結果記録→ 使用決定→ 在庫登録
製造指図 → 生産 → 工程検査→ 結果記録→ 最終検査→ 完成品在庫
販売指図 → 出荷検査→ 品質証明書発行→ 出荷
　※ 黄色の背景がQM関連プロセス


## 添付ファイル

- 🖼️ [SAP-QM_Visual Guide.png](./SAP-QM -_ 00. Overview_attachments/SAP-QM_Visual Guide.png)
- 📄 [SAP-QM_Object Relations.pdf](./SAP-QM -_ 00. Overview_attachments/SAP-QM_Object Relations.pdf)
