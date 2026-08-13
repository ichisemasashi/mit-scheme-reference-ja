# MIT Scheme リファレンス・マニュアル — 日本語訳

Chris Hanson、the MIT Scheme Team ほか著
*MIT Scheme Reference Manual*（Edition 1.94, for Scheme Release 7.5、2001年）の
日本語訳です。

**→ [目次と読む順は `ja/README.md`](ja/README.md)**

## 原著

- **書名**: MIT Scheme Reference Manual
- **版**: Edition 1.94, for Scheme Release 7.5, 16 July 2001
- **著者**: Chris Hanson, the MIT Scheme Team, and a cast of thousands
- **著作権**: Copyright © 1988–2001 Massachusetts Institute of Technology
- **ライセンス**: GNU Free Documentation License, Version 1.1 以降
  （Invariant Sections なし、Cover Texts なし）

この底本は2001年の版であり、現行の MIT/GNU Scheme（12.x 系）のマニュアルでは
ありません。『Software Design for Flexibility』が読者に薦めるのは現行版ですが、
手元にあるのがこの版なので、この版を訳しています。

## このリポジトリについて

**これは原著の翻訳であり、改変された著作物です。** 原著者は本翻訳の内容に
責任を負いません。訳文の誤りはすべて訳者に帰属します。

原著が GFDL で公開されているため、本翻訳も**同じ GFDL（Version 1.1 以降）で
公開します**。GFDL の第8節（Translation）は翻訳を改変の一種と定め、第4節
（Modifications）の条件のもとで翻訳版を配布してよいとしています。

GFDL は CC BY-SA と違い、**ライセンス英語原文の同梱を義務づけます**。本リポジトリ
では [GFDL-1.1.txt](GFDL-1.1.txt) にその全文を収めています。利用・改変・再配布の
条件は [LICENSE.md](LICENSE.md) を見てください。

## 構成

| ディレクトリ／ファイル | 内容 |
|---|---|
| `ja/` | 日本語訳 |
| [`GFDL-1.1.txt`](GFDL-1.1.txt) | GNU Free Documentation License 1.1 の英語原文（GFDL が同梱を要求） |
| [`LICENSE.md`](LICENSE.md) | ライセンスの説明（日本語） |
| [`TRANSLATION-GLOSSARY.md`](TRANSLATION-GLOSSARY.md) | 用語集と翻訳方針 |
| `tools/` | 構造検証・訳文走査・底本分割のスクリプト |
| `src/` | 原著PDFから抽出した英語テキスト（**リポジトリに含めない**。下記参照） |

原著の章立ては次のとおりです。

| 章 | 原題 | 訳題 | 状態 |
|---|---|---|---|
| — | Acknowledgements ほか前付け | 前付け | 完了 |
| 1 | Overview | 概観 | 完了 |
| 2 | Special Forms | 特殊形式 | 完了 |
| 3 | Equivalence Predicates | 同値述語 | 完了 |
| 4 | Numbers | 数 | 完了 |
| 5 | Characters | 文字 | 完了 |
| 6 | Strings | 文字列 | 完了 |
| 7 | Lists | リスト | 完了 |
| 8 | Vectors | ベクタ | 完了 |
| 9 | Bit Strings | ビット列 | 完了 |
| 10 | Miscellaneous Datatypes | その他のデータ型 | 完了 |
| 11 | Associations | 連想 | 完了 |
| 12 | Procedures | 手続き | 完了 |
| 13 | Environments | 環境 | 完了 |
| 14 | Input/Output | 入出力 | 完了 |
| 15 | Operating-System Interface | オペレーティングシステムインタフェース | 完了 |
| 16 | Error System | エラーシステム | 完了 |
| 17 | Graphics | グラフィックス | 完了 |
| 18 | Win32 Package Reference | Win32 パッケージリファレンス | 完了 |
| — | GNU Free Documentation License | （英語原文を [GFDL-1.1.txt](GFDL-1.1.txt) に同梱） | 完了 |
| — | Binding Index / Concept Index | 束縛索引／概念索引 | 訳出しない |

### 訳出しない部分

**索引（Binding Index / Concept Index）**は訳出しません。ページ番号の一覧であり、
訳文とページが対応しないためです。手続き名は原文のままなので、束縛索引の値は原著の
索引がそのまま使えます。

## 底本の作り方

**`src/` はこのリポジトリに含めていません。** 機械抽出のため劣化しており、原著を
誤って伝えかねないからです。原著PDFを用意すれば、次の手順で再生成できます。

```bash
pdftotext -layout "MIT Scheme Reference Manual.pdf" src/full.txt
python3 tools/split.py
```

`tools/split.py` はページの柱を除き、章ごとに `src/NN-slug.txt` へ分けます。

## 翻訳の方針

詳細は [TRANSLATION-GLOSSARY.md](TRANSLATION-GLOSSARY.md) にあります。

- 本文は敬体（です・ます調）
- コード、識別子、手続き名、特殊形式名、出力例、型名は訳さない
- エントリ（`@deffn` 由来）はシグネチャを訳さず、分類を〔〕で添えて説明を訳す
- 索引は訳さない
