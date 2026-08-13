# MIT Scheme リファレンス・マニュアル 日本語訳

Chris Hanson、the MIT Scheme Team ほか著
『MIT Scheme Reference Manual』（Edition 1.94, for Scheme Release 7.5、2001年）の
日本語訳です。

原著 © 1988–2001 Massachusetts Institute of Technology
原著ライセンス: [GNU Free Documentation License, Version 1.1 以降](../GFDL-1.1.txt)
（Invariant Sections なし、Cover Texts なし）

本訳は原著を日本語に翻訳した改変著作物であり、同じ GFDL のもとで公開します。GFDL は
CC BY-SA と違い、ライセンス英語原文の同梱を義務づけます（第8節）。原文は
[GFDL-1.1.txt](../GFDL-1.1.txt) に収めています。翻訳と英語原文が食い違う場合は英語
原文が優先します。訳文の誤りは訳者に帰属し、原著者は責任を負いません。利用・改変・
再配布の条件は [LICENSE.md](../LICENSE.md) を見てください。

## 目次

| | 章 | 訳文 | エントリ |
|---|---|---:|---:|
| | [前付け（表題・許諾表示・謝辞）](00-front.md) | 56 | — |
| 1 | [概観](01-overview.md) | 670 | 3 |
| 2 | [特殊形式](02-special-forms.md) | 1110 | 33 |
| 3 | [同値述語](03-equivalence-predicates.md) | 200 | 3 |
| 4 | [数](04-numbers.md) | 996 | 140 |
| 5 | [文字](05-characters.md) | 424 | 58 |
| 6 | [文字列](06-strings.md) | 826 | 117 |
| 7 | [リスト](07-lists.md) | 800 | 103 |
| 8 | [ベクタ](08-vectors.md) | 223 | 30 |
| 9 | [ビット列](09-bit-strings.md) | 221 | 30 |
| 10 | [その他のデータ型](10-misc-datatypes.md) | 672 | 61 |
| 11 | [連想](11-associations.md) | 1311 | 131 |
| 12 | [手続き](12-procedures.md) | 346 | 29 |
| 13 | [環境](13-environments.md) | 152 | 17 |
| 14 | [入出力](14-io.md) | 1357 | 152 |
| 15 | [オペレーティングシステムインタフェース](15-os-interface.md) | 1993 | 188 |
| 16 | [エラーシステム](16-error-system.md) | 1168 | 89 |
| 17 | [グラフィックス](17-graphics.md) | 1051 | 110 |
| 18 | [Win32 パッケージリファレンス](18-win32.md) | 466 | 47 |

計 14,042行、エントリ約1,341項目、脚注22本。

## この底本について

この訳の底本は **Edition 1.94（Scheme Release 7.5 対応、2001年）** です。現行の
MIT/GNU Scheme（12.x 系）のマニュアルではありません。『Software Design for
Flexibility』が読者に薦めるのは現行版ですが、手元にあるのがこの版なので、この版を
訳しています。したがって、現行の処理系では動作や名前が異なる項目がありえます。

## この訳文の約束事

**エントリはシグネチャを訳さず、分類を〔〕で添えています。** このマニュアルの中心は、
手続き・特殊形式・変数の項目（原著の Texinfo `@deffn` 由来）です。訳では各項目を
見出しにし、シグネチャをコードスパンに入れて訳さず、分類を〔〕で示します。分類の
末尾の `＋` は **MIT Scheme の拡張**（R4RS にない）の印です。詳しくは第1章 1.1.3 と
[用語集](../TRANSLATION-GLOSSARY.md)を見てください。

**例の記号。** 評価の値は `⇒`、表示（出力）は `-|`、エラーは `error>` で示します
（原著はそれぞれ専用の記号を使っています）。REPL のエラーメッセージの例（`;The
object ...` の行）は、コードの出力例として訳さず原文のまま残しています。

**訳さない部分。** コード・識別子・手続き名・型名・出力例は訳しません。索引（Binding
Index / Concept Index）も訳しません。手続き名は原文のままなので、原著の束縛索引が
そのまま使えます。

**訳語は[用語集](../TRANSLATION-GLOSSARY.md)で担保しています。** 訳語のゆれに気づい
たら、まず用語集を見てください。

## 文体

- 本文・説明文は敬体（です・ます調）
- 脚注は常体（〜である）
- 「function」ではなく「手続き（procedure）」。Scheme の用語法に従います
