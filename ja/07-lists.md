<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 7 リスト

**ペア（pair）**（ドット対（dotted pair）と呼ばれることもあります）とは、（歴史的な
理由から）car フィールドと cdr フィールドと呼ばれる2つのフィールドを持つデータ構造
です。ペアは手続き `cons` で作られます。car フィールドと cdr フィールドは、手続き `car`
と `cdr` でアクセスされます。car フィールドと cdr フィールドは、手続き `set-car!` と
`set-cdr!` で代入されます。

ペアはおもにリストを表すのに使われます。**リスト（list）**は、空リストか、cdr がリスト
であるようなペアのどちらか、と再帰的に定義できます。より正確には、リストの集合は、次を
満たす最小の集合 X と定義されます。

- 空リストが X に含まれる。
- `list` が X に含まれるなら、cdr フィールドに `list` を含む任意のペアも X に含まれる。

リストの連続するペアの car フィールドにあるオブジェクトが、リストの**要素**です。たと
えば、2要素のリストは、car が最初の要素で、cdr が、car が2番目の要素で cdr が空リスト
であるようなペアであるようなペアです。リストの**長さ**は要素の数で、これはペアの数と
同じです。空リストは、それ自身の型の特別なオブジェクトです（ペアではありません）。
要素を持たず、その長さは 0 です[^1]。

Scheme のペアのもっとも一般的な記法（外部表現）は、「ドット」記法 `(c1 . c2)` です。
`c1` は car フィールドの値、`c2` は cdr フィールドの値です。たとえば `(4 . 5)` は、
car が 4 で cdr が 5 であるペアです。`(4 . 5)` はペアの外部表現であって、ペアに評価
される式ではないことに注意してください。

リストにはより簡潔な記法が使えます。リストの要素を単に括弧で囲み、スペースで区切ります。
空リストは `()` と書きます。たとえば、次はシンボルのリストの等価な記法です。

```scheme
(a b c d e)
(a . (b . (c . (d . (e . ())))))
```

あるペアがリストかどうかは、cdr フィールドに何が格納されているかによります。`set-cdr!`
手続きが使われると、あるオブジェクトはある瞬間はリストで、次の瞬間はそうでない、という
ことがありえます。

```scheme
(define x (list 'a 'b 'c))
(define y x)
y                                                  ⇒ (a b c)
(list? y)                                          ⇒ #t
(set-cdr! x 4)                                     ⇒ unspecified
x                                                  ⇒ (a . 4)
(eqv? x y)                                         ⇒ #t
y                                                  ⇒ (a . 4)
(list? y)                                          ⇒ #f
(set-cdr! x x)                                     ⇒ unspecified
(list? y)                                          ⇒ #f
```

空リストで終わらないペアの連鎖を、**非真正リスト（improper list）**と呼びます。非真正
リストはリストではないことに注意してください。リスト記法とドット記法は組み合わせて
非真正リストを表せます。次の等価な記法が示すとおりです。

```scheme
(a b c . d)
(a . (b . (c . d)))
```

リテラルの式や、`read` 手続きが読むオブジェクトの表現の中では、`'datum`、`` `datum ``、
`,datum`、`,@datum` のフォームは、最初の要素がそれぞれシンボル `quote`、`quasiquote`、
`unquote`、`unquote-splicing` である2要素のリストを表します。それぞれの場合の2番目の
要素は `datum` です。この慣習は、任意の Scheme プログラムをリストとして表せるように
サポートされています。とりわけこれは、`read` 手続きを使って Scheme プログラムを構文解析
することを可能にします。

## 7.1 ペア

この節では、ペアから構築された任意のグラフを構築・操作するために使える単純な演算を説明
します。

#### `pair? object` 〔手続き〕

`object` がペアなら `#t` を、そうでなければ `#f` を返します。

```scheme
(pair? '(a . b))                                   ⇒ #t
(pair? '(a b c))                                   ⇒ #t
(pair? '())                                        ⇒ #f
(pair? '#(a b))                                    ⇒ #f
```

#### `cons obj1 obj2` 〔手続き〕

car が `obj1` で cdr が `obj2` である、新しく割り当てられたペアを返します。このペアは、
以前から存在するすべてのオブジェクトと（`eqv?` の意味で）異なることが保証されます。

```scheme
(cons 'a '())                                   ⇒ (a)
(cons '(a) '(b c d))                            ⇒ ((a) b c d)
(cons "a" '(b c))                               ⇒ ("a" b c)
(cons 'a 3)                                     ⇒ (a . 3)
(cons '(a b) 'c)                                ⇒ ((a b) . c)
```

#### `car pair` 〔手続き〕

`pair` の car フィールドの内容を返します。空リストの car を取るのはエラーであることに
注意してください。

```scheme
(car '(a b c))                                   ⇒ a
(car '((a) b c d))                               ⇒ (a)
(car '(1 . 2))                                   ⇒ 1
(car '())                                         error> Illegal datum
```

#### `cdr pair` 〔手続き〕

`pair` の cdr フィールドの内容を返します。空リストの cdr を取るのはエラーであることに
注意してください。

```scheme
(cdr '((a) b c d))                               ⇒ (b c d)
(cdr '(1 . 2))                                   ⇒ 2
(cdr '())                                         error> Illegal datum
```

#### `set-car! pair object` 〔手続き〕

`object` を `pair` の car フィールドに格納します。`set-car!` が返す値は未規定です。

```scheme
(define (f) (list 'not-a-constant-list))
(define (g) '(constant-list))
(set-car! (f) 3)                                  ⇒ unspecified
(set-car! (g) 3)                                   error> Illegal datum
```

#### `set-cdr! pair object` 〔手続き〕

`object` を `pair` の cdr フィールドに格納します。`set-cdr!` が返す値は未規定です。

#### `caar pair` 〔手続き〕
#### `cadr pair` 〔手続き〕
#### `cdar pair` 〔手続き〕
#### `cddr pair` 〔手続き〕
#### `caaar pair` 〔手続き〕
#### `caadr pair` 〔手続き〕
#### `cadar pair` 〔手続き〕
#### `caddr pair` 〔手続き〕
#### `cdaar pair` 〔手続き〕
#### `cdadr pair` 〔手続き〕
#### `cddar pair` 〔手続き〕
#### `cdddr pair` 〔手続き〕
#### `caaaar pair` 〔手続き〕
#### `caaadr pair` 〔手続き〕
#### `caadar pair` 〔手続き〕
#### `caaddr pair` 〔手続き〕
#### `cadaar pair` 〔手続き〕
#### `cadadr pair` 〔手続き〕
#### `caddar pair` 〔手続き〕
#### `cadddr pair` 〔手続き〕
#### `cdaaar pair` 〔手続き〕
#### `cdaadr pair` 〔手続き〕
#### `cdadar pair` 〔手続き〕
#### `cdaddr pair` 〔手続き〕
#### `cddaar pair` 〔手続き〕
#### `cddadr pair` 〔手続き〕
#### `cdddar pair` 〔手続き〕
#### `cddddr pair` 〔手続き〕

これらの手続きは `car` と `cdr` の合成です。たとえば `caddr` は次のように定義できたはず
です。

```scheme
(define caddr (lambda (x) (car (cdr (cdr x)))))
```

#### `general-car-cdr object path` 〔手続き＋〕

この手続きは `car` と `cdr` の一般化です。`path` は `car` と `cdr` の演算の特定の並びを
符号化し、`general-car-cdr` はそれを `object` に対して実行します。`path` は、演算を
ビットごとに符号化する正確な非負整数です。0 ビットは `cdr` 演算を、1 ビットは `car` を
表します。ビットは LSB から MSB へ実行され、もっとも上位の 1 ビットは、演算として解釈
される代わりに、並びの終わりを知らせます[^2]。

たとえば、次は等価です。

```scheme
(general-car-cdr object #b1011)
(cdr (car (car object)))
```

`path` と演算の対応の一部を挙げます。

```text
#b10     cdr
#b11     car
#b100    cddr
#b101    cdar
#b110    cadr
#b111    caar
#b1000   cdddr
```

#### `tree-copy tree` 〔手続き＋〕

これは、ペアから構築された任意の木を、すべてのペアの car 要素と cdr 要素の両方を複製
しながら複製します。次のように定義できたはずです。

```scheme
(define (tree-copy tree)
  (let loop ((tree tree))
    (if (pair? tree)
        (cons (loop (car tree)) (loop (cdr tree)))
        tree)))
```

## 7.2 リストの構築

#### `list object …` 〔手続き〕

引数のリストを返します。

```scheme
(list 'a (+ 3 4) 'c)                              ⇒ (a 7 c)
(list)                                            ⇒ ()
```

次の式は等価です。

```scheme
(list obj1 obj2 ... objN)
(cons obj1 (cons obj2 ... (cons objN '()) ...))
```

#### `make-list k [element]` 〔手続き＋〕

この手続きは、要素がすべて `element` である、長さ `k` の新しく割り当てられたリストを
返します。`element` が与えられなければ、既定で空リストです。

#### `cons* object object …` 〔手続き＋〕

`cons*` は `list` に似ていますが、最後の引数を空リストと cons するのではなく、最後の
2つの引数を cons する点が異なります。最後の引数がリストでなければ、結果は非真正リスト
です。最後の引数がリストなら、結果は最初のほうの引数と、最後の引数のすべての項目から
なるリストです。引数が1つだけなら、結果はその引数です。

```scheme
(cons* 'a 'b 'c)                                   ⇒ (a b . c)
(cons* 'a 'b '(c d))                               ⇒ (a b c d)
(cons* 'a)                                         ⇒ a
```

次の式は等価です。

```scheme
(cons* obj1 obj2 ... objN-1 objN)
(cons obj1 (cons obj2 ... (cons objN-1 objN) ...))
```

#### `list-copy list` 〔手続き＋〕

`list` の新しく割り当てられた複製を返します。これは `list` を構成する各ペアを複製します。
次のように定義できたはずです。

```scheme
(define (list-copy list)
  (if (null? list)
       '()
       (cons (car list)
              (list-copy (cdr list)))))
```

#### `vector->list vector` 〔手続き〕
#### `subvector->list vector start end` 〔手続き＋〕

`vector->list` は `vector` の要素の、新しく割り当てられたリストを返します。
`subvector->list` は与えられた部分ベクタの要素の、新しく割り当てられたリストを返し
ます。`vector->list` の逆は `list->vector` です。

```scheme
(vector->list '#(dah dah didah))                 ⇒ (dah dah didah)
```

#### `string->list string` 〔手続き〕
#### `substring->list string start end` 〔手続き〕

`string->list` は `string` の文字要素の、新しく割り当てられたリストを返します。
`substring->list` は与えられた部分文字列の文字要素の、新しく割り当てられたリストを
返します。`string->list` の逆は `list->string` です。

```scheme
(string->list "abcd")                           ⇒ (#\a #\b #\c #\d)
(substring->list "abcdef" 1 3)                  ⇒ (#\b #\c)
```

## 7.3 リストの成分の選択

#### `list? object` 〔手続き＋〕

`object` がリストなら `#t` を、そうでなければ `#f` を返します。定義により、すべての
リストは有限の長さを持ち、空リストで終わります。この手続きは循環構造についても答えを
返します。この述語を満たすオブジェクトは、`pair?` か `null?` のどちらかちょうど1つも
満たします。

```scheme
(list? '(a b c))                                   ⇒ #t
(list? '())                                        ⇒ #t
(list? '(a . b))                                   ⇒ #f
(let ((x (list 'a)))
  (set-cdr! x x)
  (list? x))                                       ⇒ #f
```

#### `length list` 〔手続き〕

`list` の長さを返します。

```scheme
(length '(a b c))                                  ⇒ 3
(length '(a (b) (c d e)))                          ⇒ 3
(length '())                                       ⇒ 0
```

#### `null? object` 〔手続き〕

`object` が空リストなら `#t` を、そうでなければ `#f` を返します（ただし1.2.5節「真と偽」
を見よ）。

```scheme
(null? '(a . b))                                   ⇒ #f
(null? '(a b c))                                   ⇒ #f
(null? '())                                        ⇒ #t
```

#### `list-ref list k` 〔手続き〕

`list` の `k` 番目の要素を、0 起点の添字で返します。リストの妥当な添字は、リストの長さ
より小さい正確な非負整数です。リストの最初の要素は添字 0 を、2番目は添字 1 を、以下
同様に持ちます。

```scheme
(list-ref '(a b c d) 2)                 ⇒ c
(list-ref '(a b c d)
          (inexact->exact (round 1.8)))
     ⇒ c
```

`(list-ref list k)` は `(car (list-tail list k))` と等価です。

#### `first list` 〔手続き＋〕
#### `second list` 〔手続き＋〕
#### `third list` 〔手続き＋〕
#### `fourth list` 〔手続き＋〕
#### `fifth list` 〔手続き＋〕
#### `sixth list` 〔手続き＋〕
#### `seventh list` 〔手続き＋〕
#### `eighth list` 〔手続き＋〕
#### `ninth list` 〔手続き＋〕
#### `tenth list` 〔手続き＋〕

`list` の指定された要素を返します。`list` が指定された要素を含むほど長くなければエラー
です（たとえば `seventh` への引数が6要素しか含まないリストの場合）。

## 7.4 リストの切り貼り

#### `sublist list start end` 〔手続き＋〕

`start` と `end` は次を満たす正確な整数でなければなりません。

```text
0 ≤ start ≤ end ≤ (length list)
```

`sublist` は、添字 `start`（を含む）から始まり `end`（を含まない）で終わる `list` の
要素から作られた、新しく割り当てられたリストを返します。

#### `list-head list k` 〔手続き＋〕

`list` の最初の `k` 要素からなる、新しく割り当てられたリストを返します。`k` は `list`
の長さより大きくてはなりません。`list-head` は次のように定義できたはずです。

```scheme
(define (list-head list k)
  (sublist list 0 k))
```

#### `list-tail list k` 〔手続き〕

最初の `k` 要素を省いて得られる `list` の部分リストを返します。結果は、空リストでなけれ
ば、`list` と構造を共有します。`k` は `list` の長さより大きくてはなりません。

#### `append list …` 〔手続き〕

最初のリストの要素に、他のリストの要素が続くリストを返します。

```scheme
(append '(x) '(y))                                ⇒ (x y)
(append '(a) '(b c d))                            ⇒ (a b c d)
(append '(a (b)) '((c)))                          ⇒ (a (b) (c))
(append)                                          ⇒ ()
```

結果のリストは、最後のリスト引数と構造を共有する点を除いて、つねに新しく割り当てられ
ます。最後の引数は実は任意のオブジェクトでよく、最後の引数が真正リストでなければ非真正
リストになります。

```scheme
(append '(a b) '(c . d))                          ⇒ (a b c . d)
(append '() 'a)                                   ⇒ a
```

#### `append! list …` 〔手続き＋〕

引数のリストを連結したリストを返します。引数は複製されるのではなく変更されます。
（引数を破壊せず複製する `append` と比べてください。）たとえば、

```scheme
(define x '(a b c))
(define y '(d e f))
(define z '(g h))
(append! x y z)                                 ⇒ (a b c d e f g h)
x                                               ⇒ (a b c d e f g h)
y                                               ⇒ (d e f g h)
z                                               ⇒ (g h)
```

#### `last-pair list` 〔手続き＋〕

`list` の最後のペアを返します。`list` は非真正リストでもよいです。`last-pair` は次の
ように定義できたはずです。

```scheme
(define last-pair
  (lambda (x)
    (if (pair? (cdr x))
        (last-pair (cdr x))
        x)))
```

#### `except-last-pair list` 〔手続き＋〕
#### `except-last-pair! list` 〔手続き＋〕

これらの手続きは `list` から最後のペアを取り除きます。`list` は非真正リストでもよい
ですが、少なくとも1つのペアからならなければなりません。`except-last-pair` は最後の
ペアを省いた `list` の新しく割り当てられた複製を返します。`except-last-pair!` は
`list` から最後のペアを破壊的に取り除き、`list` を返します。`list` の cdr がペアでなけ
れば、どちらの手続きも空リストを返します。

## 7.5 リストのフィルタリング

#### `list-transform-positive list predicate` 〔手続き＋〕
#### `list-transform-negative list predicate` 〔手続き＋〕

これらの手続きは、`predicate` が（それぞれ）真または偽である要素だけを含む、`list` の
新しく割り当てられた複製を返します。`predicate` は1引数の手続きでなければなりません。

```scheme
(list-transform-positive '(1 2 3 4 5) odd?) ⇒ (1 3 5)
(list-transform-negative '(1 2 3 4 5) odd?) ⇒ (2 4)
```

#### `delq element list` 〔手続き＋〕
#### `delv element list` 〔手続き＋〕
#### `delete element list` 〔手続き＋〕

`element` に等しいすべての項目を取り除いた、`list` の新しく割り当てられた複製を返し
ます。`delq` は `element` を `list` の項目と比較するのに `eq?` を、`delv` は `eqv?` を、
`delete` は `equal?` を使います。

#### `delq! element list` 〔手続き＋〕
#### `delv! element list` 〔手続き＋〕
#### `delete! element list` 〔手続き＋〕

`element` に等しいすべての項目を取り除いた、`list` のトップレベルの要素からなるリストを
返します。これらの手続きは `delq`、`delv`、`delete` に似ていますが、`list` を破壊的に
書き換える点が異なります。`delq!` は `element` を `list` の項目と比較するのに `eq?` を、
`delv!` は `eqv?` を、`delete!` は `equal?` を使います。結果が `list` に `eq?` でない
かもしれないので、`(set! x (delete! x))` のようにするのが望ましいです。

```scheme
(define x '(a b c b))
(delete 'b x)                                    ⇒ (a c)
x                                                ⇒ (a b c b)

(define x '(a b c b))
(delete! 'b x)                                   ⇒ (a c)
x                                                ⇒ (a c)
;; 正しい結果を返す:
(delete! 'a x)                                   ⇒ (c)

;; x が指すものは書き換えなかった:
x                                                ⇒ (a c)
```

#### `delete-member-procedure deletor predicate` 〔手続き＋〕

`delv` や `delete!` に似た削除手続きを返します。`deletor` は手続き `list-deletor` か
`list-deletor!` のどちらかであるべきです。`predicate` は同値述語でなければなりません。
返される手続きはちょうど2つの引数を受け取ります。1つ目は削除されるオブジェクト、2つ目
はそれを削除する元となるオブジェクトのリストです。`deletor` が `list-deletor` なら、
手続きは、与えられたオブジェクトに等しいすべての項目を取り除いた、与えられたリストの
新しく割り当てられた複製を返します。`deletor` が `list-deletor!` なら、手続きは、
与えられたオブジェクトに等しいすべての項目を取り除いた、与えられたリストのトップレベル
の要素からなるリストを返します。与えられたリストは結果を作るために破壊的に書き換えられ
ます。どちらの場合も、`predicate` が、与えられたオブジェクトを与えられたリストの要素と
比較するのに使われます。

`delete-member-procedure` を使って `delv` と `delete!` を実装できたはずの例をいくつか
挙げます。

```scheme
(define delv
  (delete-member-procedure list-deletor eqv?))
(define delete!
  (delete-member-procedure list-deletor! equal?))
```

#### `list-deletor predicate` 〔手続き＋〕
#### `list-deletor! predicate` 〔手続き＋〕

これらの手続きは、それぞれリストから要素を削除する手続きを返します。`predicate` は1引数
の手続きでなければなりません。返される手続きはちょうど1つの引数を受け取り、それは真正
リストでなければなりません。手続きは引数の各要素に `predicate` を適用し、それが真である
ものを削除します。`list-deletor` が返す手続きは、適切な要素を取り除いた引数の新しく
割り当てられた複製を返すことで、非破壊的に削除します。`list-deletor!` が返す手続きは、
破壊的な削除を行います。

## 7.6 リストの検索

#### `list-search-positive list predicate` 〔手続き＋〕
#### `list-search-negative list predicate` 〔手続き＋〕

`predicate` が（それぞれ）真または偽である `list` の最初の要素を返します。そのような
要素が見つからなければ `#f` を返します。（これは、`predicate` が `#f` について真（偽）
なら、成功した結果と失敗した結果を区別できないかもしれないことを意味します。）
`predicate` は1引数の手続きでなければなりません。

#### `memq object list` 〔手続き〕
#### `memv object list` 〔手続き〕
#### `member object list` 〔手続き〕

これらの手続きは、car が `object` である `list` の最初のペアを返します。返されるペアは
つねに `list` を構成するもののうちの1つです。`object` が `list` に現れなければ、`#f`
（念のため: 空リストではありません）が返されます。`memq` は `object` を `list` の要素と
比較するのに `eq?` を、`memv` は `eqv?` を、`member` は `equal?` を使います[^3]。

```scheme
(memq 'a '(a b c))                            ⇒ (a b c)
(memq 'b '(a b c))                            ⇒ (b c)
(memq 'a '(b c d))                            ⇒ #f
(memq (list 'a) '(b (a) c))                   ⇒ #f
(member (list 'a) '(b (a) c))                 ⇒ ((a) c)
(memq 101 '(100 101 102))                     ⇒ unspecified
(memv 101 '(100 101 102))                     ⇒ (101 102)
```

#### `member-procedure predicate` 〔手続き＋〕

`memq` に似た手続きを返しますが、`eq?` の代わりに、同値述語でなければならない `predicate`
が使われる点が異なります。これを使って `memv` を次のように定義できます。

```scheme
(define memv (member-procedure eqv?))
```

## 7.7 リストの写像

#### `map procedure list list …` 〔手続き〕

`procedure` は、リストの数だけの引数を取る手続きでなければなりません。2つ以上のリストが
与えられれば、それらはすべて同じ長さでなければなりません。`map` は `procedure` をリスト
の要素に要素ごとに適用し、結果のリストを左から右への順で返します。`procedure` がリストの
要素に適用される動的な順序は未規定です。副作用を順に並べるには `for-each` を使います。

```scheme
(map cadr '((a b) (d e) (g h)))                     ⇒ (b e h)
(map (lambda (n) (expt n n)) '(1 2 3 4)) ⇒ (1 4 27 256)
(map + '(1 2 3) '(4 5 6))                           ⇒ (5 7 9)
(let ((count 0))
  (map (lambda (ignored)
           (set! count (+ count 1))
           count)
        '(a b c)))                                  ⇒ unspecified
```

#### `map* initial-value procedure list1 list2 …` 〔手続き＋〕

`map` に似ていますが、結果のリストが空リストではなく `initial-value` で終わる点が異なり
ます。次は等価です。

```scheme
(map procedure list list ...)
(map* '() procedure list list ...)
```

#### `append-map procedure list list …` 〔手続き＋〕
#### `append-map* initial-value procedure list list …` 〔手続き＋〕

それぞれ `map` と `map*` に似ていますが、`procedure` をリストの要素に適用した結果が、
`cons` ではなく `append` で連結される点が異なります。次は等価ですが、前者のほうが効率
的です。

```scheme
(append-map procedure list list ...)
(apply append (map procedure list list ...))
```

#### `append-map! procedure list list …` 〔手続き＋〕
#### `append-map*! initial-value procedure list list …` 〔手続き＋〕

それぞれ `map` と `map*` に似ていますが、`procedure` をリストの要素に適用した結果が、
`cons` ではなく `append!` で連結される点が異なります。次は等価ですが、前者のほうが効率
的です。

```scheme
(append-map! procedure list list ...)
(apply append! (map procedure list list ...))
```

#### `for-each procedure list list …` 〔手続き〕

`for-each` への引数は `map` への引数と同じですが、`for-each` は `procedure` をその値の
ためではなく副作用のために呼びます。`map` と違って、`for-each` はリストの要素に対して
最初の要素から最後まで順に `procedure` を呼ぶことが保証され、`for-each` が返す値は未規定
です。

```scheme
(let ((v (make-vector 5)))
  (for-each (lambda (i)
              (vector-set! v i (* i i)))
            '(0 1 2 3 4))
  v)                            ⇒ #(0 1 4 9 16)
```

## 7.8 リストの畳み込み

#### `reduce procedure initial list` 〔手続き＋〕

二項演算 `procedure` を使って `list` のすべての要素をまとめます。たとえば `+` を使えば、
すべての要素を足し合わせられます。

```scheme
(reduce + 0 list-of-numbers)
```

引数 `initial` は `list` が空のときにのみ使われます。この場合 `initial` が `reduce` の
呼び出しの結果です。`list` が引数を1つ持てば、それが返されます。そうでなければ、引数は
左結合の形で畳み込まれます。たとえば、

```scheme
(reduce + 0 '(1 2 3 4))                           ⇒ 10
(reduce + 0 '(1 2))                               ⇒ 3
(reduce + 0 '(1))                                 ⇒ 1
(reduce + 0 '())                                  ⇒ 0
(reduce + 0 '(foo))                               ⇒ foo
(reduce list '() '(1 2 3 4))                      ⇒ (((1 2) 3) 4)
```

#### `reduce-right procedure initial list` 〔手続き＋〕

`reduce` に似ていますが、右結合である点が異なります。

```scheme
(reduce-right list '() '(1 2 3 4))                ⇒ (1 (2 (3 4)))
```

#### `fold-right procedure initial list` 〔手続き＋〕

二項演算 `procedure` を使って `list` のすべての要素をまとめます。`reduce` や
`reduce-right` と違って、`initial` はつねに使われます。

```scheme
(fold-right + 0 '(1 2 3 4))                      ⇒ 10
(fold-right + 0 '(foo))                           error> Illegal datum
(fold-right list '() '(1 2 3 4))                 ⇒ (1 (2 (3 (4 ()))))
```

`fold-right` は、`(cons, ())` と `(procedure, initial)` のあいだの準同型を確立するので、
興味深い性質を持ちます。リストの背骨のペアを `procedure` に置き換え、末尾の `()` を
`initial` に置き換える、と考えられます。古典的なリスト処理手続きの多くは、少なくとも
固定数の引数を取る単純な版については、`fold-right` を使って表せます。

```scheme
(define (copy-list list)
  (fold-right cons '() list))

(define (append list1 list2)
  (fold-right cons list2 list1))

(define (map p list)
  (fold-right (lambda (x r) (cons (p x) r)) '() list))

(define (reverse items)
  (fold-right (lambda (x r) (append r (list x))) '() items))
```

#### `fold-left procedure initial list` 〔手続き＋〕

二項演算 `procedure` を使って `list` のすべての要素をまとめます。要素は、`initial` から
始め、次に `list` の要素を左から右へ、という順でまとめられます。`fold-right` が本質的に
再帰的で、リストを cdr でたどってから結果を計算する本質をとらえるのに対し、`fold-left`
は本質的に反復的で、リストをたどりながら要素をまとめます。

```scheme
(fold-left list '() '(1 2 3 4))                  ⇒ ((((() 1) 2) 3) 4)

(define (length list)
  (fold-left (lambda (sum element) (+ sum 1)) 0 list))

(define (reverse items)
  (fold-left (lambda (x y) (cons y x)) () items))
```

#### `there-exists? list predicate` 〔手続き＋〕

`predicate` は1引数の手続きでなければなりません。`list` の各要素に、左から右への順で
`predicate` を適用します。`predicate` が `list` のいずれかの要素について真なら、
`predicate` が生む値がただちに `there-exists?` の値として返されます。`predicate` は
`list` の残りの要素には適用されません。`predicate` が `list` のすべての要素について `#f`
を返せば、`#f` が返されます。

#### `for-all? list predicate` 〔手続き＋〕

`predicate` は1引数の手続きでなければなりません。`list` の各要素に、左から右への順で
`predicate` を適用します。`predicate` が `list` のいずれかの要素について `#f` を返せば、
`#f` がただちに `for-all?` の値として返されます。`predicate` は `list` の残りの要素には
適用されません。`predicate` が `list` のすべての要素について真なら、`#t` が返されます。

## 7.9 その他のリスト操作

#### `circular-list object …` 〔手続き＋〕
#### `make-circular-list k [element]` 〔手続き＋〕

これらの手続きは、それぞれ `list` と `make-list` に似ていますが、返されるリストが循環
する点が異なります。`circular-list` は次のように定義できたはずです。

```scheme
(define (circular-list . objects)
   (append! objects objects))
```

#### `reverse list` 〔手続き〕

`list` のトップレベルの要素を逆順にした、新しく割り当てられたリストを返します。

```scheme
(reverse '(a b c))                        ⇒ (c b a)
(reverse '(a (b c) d (e (f))))            ⇒ ((e (f)) d (b c) a)
```

#### `reverse! list` 〔手続き＋〕

`list` のトップレベルの要素を逆順にしたリストを返します。`reverse!` は `reverse` に似て
いますが、`list` を破壊的に書き換える点が異なります。結果が `list` に `eqv?` でないかも
しれないので、`(set! x (reverse! x))` のようにするのが望ましいです。

#### `sort sequence procedure` 〔手続き＋〕
#### `merge-sort sequence procedure` 〔手続き＋〕
#### `quick-sort sequence procedure` 〔手続き＋〕

`sequence` はリストかベクタのどちらかでなければなりません。`procedure` は、`sequence` の
要素に全順序を定める2引数の手続きでなければなりません。言い換えると、`x` と `y` が
`sequence` の2つの異なる要素なら、次が成り立たなければなりません。

```scheme
(and (procedure x y)
     (procedure y x))
     ⇒ #f
```

`sequence` がリスト（ベクタ）なら、`sort` は、要素が `sequence` のものであるが `procedure`
の定める順序でソートされるよう並べ替えられた、新しく割り当てられたリスト（ベクタ）を
返します。したがって、たとえば `sequence` の要素が数で `procedure` が `<` なら、結果の
要素は単調非減少の順にソートされます。同様に `procedure` が `>` なら、結果の要素は単調
非増加の順にソートされます。正確には、`x` と `y` が結果の中の隣り合う2つの要素で `x` が
`y` に先立つなら、次が成り立ちます。

```scheme
(procedure y x)
     ⇒ #f
```

2つのソートアルゴリズムが実装されています。`merge-sort` と `quick-sort` です。手続き
`sort` は `merge-sort` の別名です。`sort!` の定義も見よ。

---

[^1]: 上の定義は、すべてのリストが有限の長さを持ち、空リストで終わることを含意する。

[^2]: `path` は機械依存の範囲、ふつう機械のワードの大きさに制限されることに注意せよ。
    多くの機械では、これは `path` の最大長が30演算になることを意味する（32ビットから
    符号ビットと「並びの終わり」ビットを引いたもの）。

[^3]: `memq`、`memv`、`member` はしばしば述語として使われるが、名前に疑問符を持たない。
    単なる `#t` や `#f` ではなく有用な値を返すからである。
