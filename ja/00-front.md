<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。

原著: Copyright © 1988–2001 Massachusetts Institute of Technology
      by Chris Hanson, the MIT Scheme Team, and a cast of thousands.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降
      （Invariant Sections なし、Cover Texts なし）

本訳も同じ GNU Free Documentation License, Version 1.1 以降のもとで公開します。
GFDL 英語原文はリポジトリの GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。
翻訳と英語原文が食い違う場合は英語原文が優先します（GFDL 第8節）。
改変の告知: 原著（英語）を日本語に翻訳しました。訳文の誤りは訳者に帰属します。
-->

# MIT Scheme リファレンス・マニュアル

Edition 1.94 / Scheme Release 7.5 対応 / 2001年7月16日

Chris Hanson、the MIT Scheme Team、および大勢の人々による

Copyright © 1988–2001 Massachusetts Institute of Technology

> Permission is granted to copy, distribute and/or modify this document
> under the terms of the GNU Free Documentation License, Version 1.1 or
> any later version published by the Free Software Foundation; with no
> Invariant Sections, with no Front-Cover Texts, and with no Back-Cover
> Texts. A copy of the license is included in the section entitled "GNU
> Free Documentation License".

（訳）本文書は、Free Software Foundation が公開する GNU Free Documentation
License のバージョン1.1、またはそれ以降の版の条件のもとで、複製・配布・改変する
ことが許可されています。不変のセクションはなく、表紙のテキスト（表・裏）もありま
せん。ライセンスの複製は「GNU Free Documentation License」の節に収められています。

> **ライセンスの正文は英語原文（[GFDL-1.1.txt](../GFDL-1.1.txt)）です。** 上の訳は
> 便宜のためのもので、GFDL 第8節により、食い違いがあれば英語原文が優先します。

## 謝辞

「大勢の人々（a cast of thousands）」は大げさかもしれませんが、本文書が多くの人の
仕事の上に成り立っていることは確かです。まず第一に、Revised⁴ Report on the
Algorithmic Language Scheme（R4RS）の著者たちに感謝します。本文書の多くはそこから
導かれています。また、Butterfly Scheme Reference の一部を使わせてくれた BBN
Advanced Computers Inc. と、それを BBN のテキスト整形言語から私たちの言語へ移して
くれた Margaret O'Connell にも感謝します。

本文書を書くのに使った Texinfo 整形言語を作り、保守してきた、いずれも Free
Software Foundation の Richard Stallman、Bob Chassell、Brian Fox に、特別の感謝を
捧げます。

本報告は、Massachusetts Institute of Technology の人工知能研究所（Artificial
Intelligence Laboratory）と計算機科学研究所（Laboratory for Computer Science）で
行われた研究について述べたものです。この研究は、その一部を国防総省の高等研究計画局
（Advanced Research Projects Agency of the Department of Defense）と全米科学財団
（National Science Foundation）から支援を受けています。
