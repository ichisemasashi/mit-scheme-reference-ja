# ライセンス

## 原著

*MIT Scheme Reference Manual*, Edition 1.94, for Scheme Release 7.5,
16 July 2001.

by Chris Hanson, the MIT Scheme Team, and a cast of thousands.

Copyright © 1988–2001 Massachusetts Institute of Technology

原著の許諾表示（原文）は次のとおりです。

> Permission is granted to copy, distribute and/or modify this document
> under the terms of the GNU Free Documentation License, Version 1.1 or
> any later version published by the Free Software Foundation; with no
> Invariant Sections, with no Front-Cover Texts, and with no Back-Cover
> Texts. A copy of the license is included in the section entitled "GNU
> Free Documentation License".

すなわち原著は **GNU Free Documentation License, Version 1.1** またはそれ以降の
版のもとで公開されています。不変のセクション（Invariant Sections）はなく、
表紙のテキスト（Front-Cover / Back-Cover Texts）もありません。

## この日本語訳

GFDL の**第8節（Translation）**は、翻訳を改変（modification）の一種と定め、
**第4節（Modifications）**の条件のもとで翻訳を配布してよいとしています。
本訳はこれに従い、原著と同じ **GNU Free Documentation License, Version 1.1
以降**のもとで公開します。

GFDL 第4節・第8節が翻訳版に求める事項を、本リポジトリは次のように満たします。

1. **原著と区別できる表題**（第4節A）— 表題を「MIT Scheme リファレンス・
   マニュアル（日本語訳）」とし、原著の翻訳であることを明示します。
2. **原著者の表示**（第4節B）— 原著者 Chris Hanson および the MIT Scheme Team を
   表示します。
3. **原著の著作権表示の保全**（第4節D）— 上記 © 1988–2001 MIT を保ちます。
4. **改変（翻訳）の告知と訳者の表示**（第4節E・I）— 日本語への翻訳という改変を
   加えたことを示します。訳文の各ファイル冒頭にも、この告知を置いています。
5. **ライセンス表示の同梱**（第4節F）— 本ファイルがそれにあたります。
6. **英語原文のライセンス全文の同梱**（第8節）— [GFDL-1.1.txt](GFDL-1.1.txt) に、
   Free Software Foundation が公開する GNU Free Documentation License,
   Version 1.1 の英語原文をそのまま収めています。

> 翻訳と英語原文とのあいだに食い違いがある場合は、GFDL 第8節により**英語原文が
> 優先します**。ライセンスの正文は [GFDL-1.1.txt](GFDL-1.1.txt) です。

### 利用にあたって

本訳文を複製・改変・再配布する際は、GFDL の条件に従ってください。おもな義務は
次のとおりです（正確には [GFDL-1.1.txt](GFDL-1.1.txt) を参照してください）。

- **同一ライセンスでの継承** — 改変版も GFDL のもとで公開すること（第4節）
- **著作権表示とライセンス表示の保全** — 原著の © 表示、本ライセンス表示、および
  英語原文のライセンス全文を同梱すること（第4節D・F、第8節）
- **改変の告知** — 加えた変更（日本語への翻訳を含む）を示すこと（第4節）
- **透過的な複製（Transparent Copy）の提供**（第3節）— 大量に配布する場合の条件

### 免責

訳文の誤りは訳者に帰属します。原著者、the MIT Scheme Team、および Massachusetts
Institute of Technology は、本訳文についていかなる責任も負いません。原著の内容を
正確に知る必要がある場合は、原著（英語）を参照してください。GFDL は文書を
「保証なし」で提供するものです。

## `src/` について

翻訳の底本は、原著PDF（`MIT Scheme Reference Manual.pdf`）から `pdftotext` で
抽出した英語テキストです。機械抽出のため劣化しており（ページの柱の混入、行末の
ハイフン分割、記号の化けなど）、原著を正確に伝えるものではありません。このため
**`src/` はこのリポジトリに含めていません**（`.gitignore` で除外）。再生成の手順は
[README](README.md) にあります。

## `tools/` について

`tools/` の Python スクリプトは訳者が書いたものです。GFDL のもとで公開します。
