<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 13 環境

## 13.1 環境の演算

環境は MIT Scheme では第一級のオブジェクトです。**環境（environment）**は、いくつかの
束縛と、場合によっては親環境からなります。親環境からは他の束縛が継承されます。この節の
演算は、特定の環境の束縛をその親の束縛と分けて調べられるようにすることで、環境のフレーム
のような構造を明らかにします。

#### `environment? object` 〔手続き＋〕

`object` が環境なら `#t` を、そうでなければ `#f` を返します。

#### `environment-has-parent? environment` 〔手続き＋〕

`environment` が親環境を持てば `#t` を、そうでなければ `#f` を返します。

#### `environment-parent environment` 〔手続き＋〕

`environment` の親環境を返します。`environment` が親を持たなければエラーです。

#### `environment-bound-names environment` 〔手続き＋〕

`environment` によって束縛された名前（シンボル）の、新しく割り当てられたリストを返します。
これは `environment` の親環境によって束縛された名前を含みません。

#### `environment-bindings environment` 〔手続き＋〕

`environment` の束縛の、新しく割り当てられたリストを返します。親環境の束縛は含みません。
このリストの各要素は2つの形のいずれかをとります。`(name)` は `name` が束縛されているが
未代入であることを示し、`(name object)` は `name` が束縛されており、その値が `object`
であることを示します。

#### `environment-bound? environment symbol` 〔手続き＋〕

`symbol` が `environment` またはその祖先環境の1つで束縛されていれば `#t` を、そうでなけ
れば `#f` を返します。

#### `environment-lookup environment symbol` 〔手続き＋〕

`symbol` は `environment` またはその祖先環境の1つで束縛されていなければなりません。それが
束縛されている値を返します。

#### `environment-assignable? environment symbol` 〔手続き＋〕

`symbol` は `environment` またはその祖先環境の1つで束縛されていなければなりません。その
束縛が副作用で書き換えられるなら `#t` を返します。

#### `environment-assign! environment symbol object` 〔手続き＋〕

`symbol` は `environment` またはその祖先環境の1つで束縛されており、代入可能でなければなり
ません。その束縛が `object` を値として持つよう書き換え、未規定の結果を返します。

#### `eval expression environment` 〔手続き＋〕

`expression`、すなわち Scheme の式のリスト構造表現（S 式表現と呼ばれることもあります）を、
`environment` で評価します。ふつうのプログラムで `eval` が必要になることはめったにありま
せん。おもに、プログラムが「その場で」作った式を評価するのに役立ちます。`eval` は、
`expression` を実行する前に内部形式へ変換しなければならないので、比較的高くつきます。

```scheme
(define foo (list '+ 1 2))
(eval foo (the-environment))                    ⇒ 3
```

## 13.2 環境変数

`user-initial-environment` は、トップレベルの read-eval-print（rep）ループが式を評価し、
定義を格納する場所です。これは `system-global-environment` の子で、そこにはすべての
Scheme システムの定義が格納されています。現在環境が `user-initial-environment` のとき、
`system-global-environment` のすべての束縛が使えます。しかし、rep ループで（`define`
フォームで、あるいは `define` フォームを含むファイルを読み込んで）作る新しい束縛は、
`user-initial-environment` に生じます。

#### `system-global-environment` 〔変数＋〕

変数 `system-global-environment` は、`user-initial-environment` の親である環境に束縛
されています。基本手続きとシステム手続きは、この環境で束縛されます（ときには閉じられ
ます）。

#### `user-initial-environment` 〔変数＋〕

変数 `user-initial-environment` は、トップレベルの rep ループがタイプされた式を評価する
既定の環境に束縛されています。

`system-global-environment` のすべての束縛は rep ループから見えますが、rep ループで
タイプされた、あるいは rep ループが読み込んだ定義は、`user-initial-environment` に
生じます。これは一つには安全のための措置です。たまたま重要なシステム手続きと同じ名前の
定義を入力しても、あなたの定義は `user-initial-environment` で定義する手続きからしか
見えません。`system-global-environment` で定義される MIT Scheme のシステム手続きは、
もとの定義を見つづけます。

## 13.3 REPL 環境

#### `nearest-repl/environment` 〔手続き＋〕

現在の rep ループ環境（すなわち、もっとも近く囲む rep ループの現在環境）を返します。
Scheme が最初に起動したとき、これは `user-initial-environment` と同じです。

#### `ge environment` 〔手続き＋〕

現在の rep ループ環境を `environment` に変えます。`environment` は環境か手続きオブジェクト
のどちらかでよいです。手続きなら、その手続きが閉じられた環境が新しい環境になります。

## 13.4 インタプリタ環境

この節の演算は、インタプリタが構築する環境を返します。これらの演算はファイルのトップ
レベルでのみ使うべきで、他のどの場所でもサポートされていません。とくに、これらの演算は、
現在環境を、インタプリタが使うのに適した形で表現するよう強制します。これは、コンパイラが
そのような環境に対して多くの有用な最適化を行うのを妨げ、それらの環境での変数参照に
インタプリタの使用を強制します。ただし、（`user-initial-environment` のような）すべての
トップレベル環境はすでにインタプリタ環境なので、それらにこうした演算を使っても害はあり
ません。

警告: MIT Scheme の将来のリリースは衛生的マクロ（hygienic macros）をサポートします。これ
は `make-environment` と `the-environment` のトップレベルでないインスタンスと両立しま
せん。そのとき、これらの構文の他の使い方は許されなくなります。

#### `make-environment expression …` 〔特殊形式＋〕

それが実行される環境の子である新しい環境を作り、新しい環境で式を順に評価し、新しい環境
を返します。次に注意してください。

```scheme
(make-environment expression ...)
```

は次と等価です。

```scheme
(let ()
   expression ...
   (the-environment))
```

#### `the-environment` 〔特殊形式＋〕

現在環境を返します。

#### `interpreter-environment? object` 〔手続き＋〕

`object` がインタプリタ環境なら `#t` を、そうでなければ `#f` を返します。
