<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 5 文字

**文字（character）**とは、文字（レター）や数字のような、印刷される文字を表すオブジェクト
です[^1]。

## 5.1 文字の外部表現

文字は、記法 `#\character` または `#\character-name` を使って書きます。たとえば、

```scheme
#\a                           ; 小文字
#\A                           ; 大文字
#\(                           ; 左括弧
#\space                       ; スペース文字
#\newline                     ; 改行文字
```

`#\character` では大文字小文字が意味を持ちますが、`#\character-name` では持ちません。
`#\character` の `character` が文字（レター）なら、`character` の後ろにはスペースや
括弧のような区切り文字が続かなければなりません。`#\` 記法で書かれた文字は自己評価的
です。クォートする必要はありません。

文字名には、その文字がキーボードのシフトキー Control、Meta、Super、Hyper、Top の1つ
以上を含むことを示す、1つ以上の bucky ビット接頭辞を含められます（Control の bucky
ビット接頭辞は、ASCII の control キーとは同じではないことに注意してください）。bucky
ビット接頭辞とその意味は次のとおりです（大文字小文字は意味を持ちません）。

| キー | bucky ビット接頭辞 | bucky ビット |
|---|---|---|
| Meta | `M-` または `Meta-` | 1 |
| Control | `C-` または `Control-` | 2 |
| Super | `S-` または `Super-` | 4 |
| Hyper | `H-` または `Hyper-` | 8 |
| Top | `T-` または `Top-` | 16 |

たとえば、

```scheme
#\c-a                         ; Control-a
#\meta-b                      ; Meta-b
#\c-s-m-h-a                   ; Control-Meta-Super-Hyper-A
```

次の文字名がサポートされています。ここでは ASCII の等価物とともに示します。

| 文字名 | ASCII 名 |
|---|---|
| `altmode` | ESC |
| `backnext` | US |
| `backspace` | BS |
| `call` | SUB |
| `linefeed` | LF |
| `page` | FF |
| `return` | CR |
| `rubout` | DEL |
| `space` | |
| `tab` | HT |

加えて、`#\newline` は `#\linefeed` と同じです（ただしこれは将来変わるかもしれないので、
依存すべきではありません）。非印字文字の標準的な ASCII 名はすべてサポートされています。

```text
NUL       SOH       STX        ETX       EOT        ENQ       ACK        BEL
BS        HT        LF         VT        FF         CR        SO         SI
DLE       DC1       DC2        DC3       DC4        NAK       SYN        ETB
CAN       EM        SUB        ESC       FS         GS        RS         US
DEL
```

#### `char->name char [slashify?]` 〔手続き＋〕

`char` の表示表現に対応する文字列を返します。これは外部表現の `character` または
`character-name` の成分に、適切な bucky ビット接頭辞を組み合わせたものです。

```scheme
(char->name #\a)                                    ⇒ "a"
(char->name #\space)                                ⇒ "Space"
(char->name #\c-a)                                  ⇒ "C-a"
(char->name #\control-a)                            ⇒ "C-a"
```

`slashify?` が指定され真なら、`read` が正しく構文解析できるように、結果に必要な
バックスラッシュ文字を挿入することを指示します。言い換えると、次は `char` の外部表現を
生成します。

```scheme
(string-append "#\\" (char->name char #t))
```

`slashify?` が指定されなければ、既定で `#f` です。

#### `name->char string` 〔手続き＋〕

文字を名指す文字列を、指定された文字に変換します。`string` がどの文字も名指さなければ、
`name->char` はエラーを通知します。

```scheme
(name->char "a")                                    ⇒ #\a
(name->char "space")                                ⇒ #\Space
(name->char "c-a")                                  ⇒ #\C-a
(name->char "control-a")                            ⇒ #\C-a
```

## 5.2 文字の比較

#### `char=? char1 char2` 〔手続き〕
#### `char<? char1 char2` 〔手続き〕
#### `char>? char1 char2` 〔手続き〕
#### `char<=? char1 char2` 〔手続き〕
#### `char>=? char1 char2` 〔手続き〕
#### `char-ci=? char1 char2` 〔手続き〕
#### `char-ci<? char1 char2` 〔手続き〕
#### `char-ci>? char1 char2` 〔手続き〕
#### `char-ci<=? char1 char2` 〔手続き〕
#### `char-ci>=? char1 char2` 〔手続き〕

指定された文字が互いに適切な順序関係を持つなら `#t` を、そうでなければ `#f` を返し
ます。`-ci` の手続きは大文字と小文字を区別しません。

文字の順序は次の規則に従います。

- 数字は順に並んでいます。たとえば `(char<? #\0 #\9)` は `#t` を返します。
- 大文字は順に並んでいます。たとえば `(char<? #\A #\B)` は `#t` を返します。
- 小文字は順に並んでいます。たとえば `(char<? #\a #\b)` は `#t` を返します。

加えて、MIT Scheme は `char-standard?` を満たす文字を ASCII と同じように順序づけます。
具体的には、すべての数字がすべての大文字に先立ち、すべての大文字がすべての小文字に
先立ちます。

文字は、まず bucky ビットの部分を比較し、次にコードの部分を比較して順序づけられます。
とくに、bucky ビットのない文字が bucky ビットのある文字より前に来ます。

## 5.3 その他の文字操作

#### `char? object` 〔手続き〕

`object` が文字なら `#t` を、そうでなければ `#f` を返します。

#### `char-upcase char` 〔手続き〕
#### `char-downcase char` 〔手続き〕

`char` が文字（レター）なら、その大文字または小文字の等価物を返します。そうでなければ
`char` を返します。これらの手続きは、`(char-ci=? char char2)` となる文字 `char2` を
返します。

#### `char->digit char [radix]` 〔手続き＋〕

`char` が与えられた基数で数字を表す文字なら、対応する整数の値を返します。`radix`（2 以上
36 以下の正確な整数でなければなりません）を指定すれば、変換はその基数で行われ、そうで
なければ 10 進で行われます。`char` が基数 `radix` で数字を表さなければ、`char->digit`
は `#f` を返します。この手続きは `char` の大文字小文字を区別しないことに注意してください。

```scheme
(char->digit #\8)                                   ⇒ 8
(char->digit #\e 16)                                ⇒ 14
(char->digit #\e)                                   ⇒ #f
```

#### `digit->char digit [radix]` 〔手続き＋〕

`radix` で与えられた基数で `digit` を表す文字を返します。`radix` は 2 以上 36 以下の
正確な整数でなければならず、既定で 10 です。`digit` は正確な非負整数でなければならず、
`radix` より小さくあるべきです。`digit` が `radix` 以上なら、`digit->char` は `#f` を
返します。

```scheme
(digit->char 8)                                  ⇒ #\8
(digit->char 14 16)                              ⇒ #\E
```

## 5.4 文字の内部表現

MIT Scheme の文字は、コードの部分と bucky ビットの部分からなります。MIT Scheme の文字の
集合は、ASCII が表せるより多くの文字を表せます。Control と Meta のほか、Super、Hyper、
Top の bucky ビットを持つ文字を含みます。どの ASCII 文字も何らかの MIT Scheme 文字に
対応しますが、逆は成り立ちません[^2]。

MIT Scheme は、5 bucky ビットを持つ16ビットの文字コードを使います。ふつう Scheme は、
文字コードの最下位7ビットを使って、その文字の ASCII 表現を保持します。この表現は、
将来の国際文字集合への対応を見越して拡張されています。

#### `make-char code bucky-bits` 〔手続き＋〕

`code` と `bucky-bits` から文字を組み立てます。`code` と `bucky-bits` はどちらも適切な
範囲の正確な非負整数でなければなりません。文字からコードと bucky ビットを取り出すには
`char-code` と `char-bits` を使います。`bucky-bits` に 0 を指定すると、`make-char` は
ふつうの文字を作ります。そうでなければ、次のように適切なビットがオンになります。

```text
1                  Meta
2                  Control
4                  Super
8                  Hyper
16                 Top
```

たとえば、

```scheme
(make-char 97 0)                                  ⇒ #\a
(make-char 97 1)                                  ⇒ #\M-a
(make-char 97 2)                                  ⇒ #\C-a
(make-char 97 3)                                  ⇒ #\C-M-a
```

#### `char-bits char` 〔手続き＋〕

`char` の bucky ビットの正確な整数表現を返します。たとえば、

```scheme
(char-bits #\a)                                  ⇒ 0
(char-bits #\m-a)                                ⇒ 1
(char-bits #\c-a)                                ⇒ 2
(char-bits #\c-m-a)                              ⇒ 3
```

#### `char-code char` 〔手続き＋〕

`char` の文字コード、すなわち正確な整数を返します。たとえば、

```scheme
(char-code #\a)                                  ⇒ 97
(char-code #\c-a)                                ⇒ 97
```

#### `char-code-limit` 〔変数＋〕
#### `char-bits-limit` 〔変数＋〕

これらの変数は、文字コードと bucky ビットの（それぞれの）上限（を含まない）を定めます。
文字コードと bucky ビットはつねに正確な非負整数であり、それぞれの上限の変数の値より
厳密に小さいです。

#### `char->integer char` 〔手続き〕
#### `integer->char k` 〔手続き〕

`char->integer` は `char` の文字コード表現を返します。`integer->char` は文字コード表現
が `k` である文字を返します。

MIT Scheme では、`(char-ascii? char)` が真なら、次が成り立ちます。

```scheme
(eqv? (char->ascii char) (char->integer char))
```

ただし、このふるまいは Scheme 標準が求めるものではなく、これに依存するコードは他の
実装に移植できません。

これらの手続きは、`char<=?` の順序のもとでの文字の集合と、`<=` の順序のもとでの整数の
ある部分集合とのあいだの、順序同型を実装します。すなわち、

```scheme
(char<=? a b) ⇒ #t              かつ      (<= x y) ⇒ #t
```

で、`x` と `y` が `char->integer` の範囲にあるなら、

```scheme
(<= (char->integer a)
     (char->integer b))                           ⇒ #t
(char<=? (integer->char x)
           (integer->char y))                     ⇒ #t
```

注意: `char->integer` や `integer->char` への引数が定数なら、コンパイラはその呼び出し
を定数畳み込みし、対応する結果に置き換えます。これは、めずらしい文字定数や ASCII
コードを表すのにとても役立つ方法です。

#### `char-integer-limit` 〔変数＋〕

`char->integer` の範囲は、この変数の値より小さい（を含まない）正確な非負整数と定義され
ます。

## 5.5 ASCII 文字

MIT Scheme は、入出力に内部で ASCII コードを使い、ASCII コードと文字のあいだの変換が
便利になるように文字オブジェクトを格納します。また、文字列は要素が ASCII コードである
バイトベクタとして実装されます。これらのコードは、アクセスされるときに文字オブジェクト
に変換されます。こうした理由から、ASCII コードと文字のあいだを変換できると望ましいこと
があります。

すべての文字が ASCII コードとして表現できるわけではありません。等価な ASCII 表現を
持つ文字を **ASCII 文字**と呼びます。

#### `char-ascii? char` 〔手続き＋〕

`char` が ASCII 表現を持つなら `char` の ASCII コードを、そうでなければ `#f` を返し
ます。現在の実装では、この述語を満たす文字は、Control、Super、Hyper、Top の bucky
ビットがオフのものです。`char-bits` 手続きが 0 または 1 を返す（すなわち bucky ビット
なし、または Meta だけの）すべての文字が、合法な ASCII 文字として数えられます。

#### `char->ascii char` 〔手続き＋〕

`char` の ASCII コードを返します。`char` が ASCII 表現を持たなければ、エラー
`condition-type:bad-range-argument` が通知されます。

#### `ascii->char code` 〔手続き＋〕

`code` は ASCII コードの正確な整数表現でなければなりません。この手続きは `code` に
対応する文字を返します。

## 5.6 文字集合

MIT Scheme の文字集合（character-set）の抽象は、文字（レター）や数字のような、文字の
グループを表すのに使われます。文字集合は ASCII 文字だけを含められます。将来、これは
文字の全範囲を許すよう変わるかもしれません。

文字集合に意味のある外部表現はありません。その内容を調べるには `char-set-members` を
使います。（今のところ）文字集合に固有の同値述語はありません。この目的には `equal?` を
使います。

#### `char-set? object` 〔手続き＋〕

`object` が文字集合なら `#t` を、そうでなければ `#f` を返します。

#### `char-set:upper-case` 〔変数＋〕
#### `char-set:lower-case` 〔変数＋〕
#### `char-set:alphabetic` 〔変数＋〕
#### `char-set:numeric` 〔変数＋〕
#### `char-set:alphanumeric` 〔変数＋〕
#### `char-set:whitespace` 〔変数＋〕
#### `char-set:not-whitespace` 〔変数＋〕
#### `char-set:graphic` 〔変数＋〕
#### `char-set:not-graphic` 〔変数＋〕
#### `char-set:standard` 〔変数＋〕

これらの変数は、あらかじめ定義された文字集合を保持します。これらの集合の1つの内容を
見るには、`char-set-members` を使います。

英字（alphabetic）は大文字と小文字の52文字です。数字（numeric）は10個の10進数字です。
英数字（alphanumeric）はこの2つの集合の和集合にあるものです。空白（whitespace）は
`#\space`、`#\tab`、`#\page`、`#\linefeed`、`#\return` です。図形文字（graphic）は
印字文字と `#\space` です。標準文字（standard）は印字文字、`#\space`、`#\newline`
です。印字文字は次のものです。

```text
! " # $ % & ' ( ) * + , - . /
0 1 2 3 4 5 6 7 8 9
: ; < = > ? @
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
[ \ ] ^ _ `
a b c d e f g h i j k l m n o p q r s t u v w x y z
{ | } ~
```

#### `char-upper-case? char` 〔手続き〕
#### `char-lower-case? char` 〔手続き〕
#### `char-alphabetic? char` 〔手続き〕
#### `char-numeric? char` 〔手続き〕
#### `char-alphanumeric? char` 〔手続き＋〕
#### `char-whitespace? char` 〔手続き〕
#### `char-graphic? char` 〔手続き＋〕
#### `char-standard? object` 〔手続き＋〕

これらの述語は、上で定義したそれぞれの文字集合を用いて定義されます。

#### `char-set-members char-set` 〔手続き＋〕

`char-set` の中の文字からなる、新しく割り当てられたリストを返します。

#### `char-set-member? char-set char` 〔手続き＋〕

`char` が `char-set` の中にあれば `#t` を、そうでなければ `#f` を返します。

#### `char-set char …` 〔手続き＋〕

指定された ASCII 文字からなる文字集合を返します。引数がなければ、`char-set` は空の
文字集合を返します。

#### `chars->char-set chars` 〔手続き＋〕

`chars`（ASCII 文字のリストでなければなりません）からなる文字集合を返します。これは
`(apply char-set chars)` と等価です。

#### `string->char-set string` 〔手続き＋〕

`string` に現れるすべての文字からなる文字集合を返します。

#### `ascii-range->char-set lower upper` 〔手続き＋〕

`lower` と `upper` は ASCII 文字コードを表す正確な非負整数でなければならず、`lower` は
`upper` 以下でなければなりません。この手続きは、ASCII コードが `lower`（を含む）から
`upper`（を含まない）のあいだにある文字からなる、新しい文字集合を作って返します。

#### `predicate->char-set predicate` 〔手続き＋〕

`predicate` は1引数の手続きでなければなりません。`predicate->char-set` は、`predicate`
が真となる ASCII 文字からなる文字集合を作って返します。

#### `char-set-difference char-set1 char-set2` 〔手続き＋〕

`char-set1` にあって `char-set2` にない文字からなる文字集合を返します。

#### `char-set-intersection char-set …` 〔手続き＋〕

すべての `char-set` にある文字からなる文字集合を返します。

#### `char-set-union char-set …` 〔手続き＋〕

少なくとも1つの `char-set` にある文字からなる文字集合を返します。

#### `char-set-invert char-set` 〔手続き＋〕

`char-set` にない ASCII 文字からなる文字集合を返します。

---

[^1]: この節の細部のいくつかは、基礎となるオペレーティングシステムが ASCII 文字集合を
    使うという事実に依存している。誰かが MIT Scheme を非 ASCII のオペレーティング
    システムに移植すると、これは変わるかもしれない。

[^2]: Control の bucky ビットは ASCII の control キーとは異なることに注意せよ。これは、
    `#\SOH`（ASCII の ctrl-A）が `#\C-A` とは異なることを意味する。実際、Control の
    bucky ビットは ASCII の control キーと完全に直交しており、`#\C-SOH` のような文字を
    可能にする。
