<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 10 その他のデータ型

## 10.1 真偽値

**真偽値（boolean）**のオブジェクトは真と偽です。真偽値の定数の真は `#t` と書き、偽は
`#f` と書きます。

真偽値のオブジェクトのおもな用途は、条件式 `if`、`cond`、`and`、`or` です。これらの式の
ふるまいは、オブジェクトが真か偽かによって決まります。これらの式は `#f` だけを偽として
数えます。それ以外はすべて、`#t`、ペア、シンボル、数、文字列、ベクタ、手続きを含めて、
真として数えます（ただし1.2.5節「真と偽」を見よ）。

ほかの Lisp 方言に慣れたプログラマは、Scheme が `#f` と空リストをシンボル `nil` と区別
することに注意すべきです。同様に、`#t` はシンボル `t` と区別されます。実際、真偽値の
オブジェクト（と空リスト）はまったくシンボルではありません。

真偽値の定数はそれ自身に評価されるので、クォートする必要はありません。

```scheme
#t                                              ⇒ #t
#f                                              ⇒ #f
'#f                                             ⇒ #f
t                                                error> Unbound variable
```

#### `false` 〔変数＋〕
#### `true` 〔変数＋〕

これらの変数は、それぞれオブジェクト `#f` と `#t` に束縛されています。コンパイラは、
ふつうの `usual-integrations` 宣言が与えられると、これらの変数への参照をそれぞれの値に
置き換えます。

シンボル `true` は `#t` と等価ではなく、シンボル `false` は `#f` と等価ではないことに
注意してください。

#### `boolean? object` 〔手続き〕

`object` が `#t` か `#f` のどちらかなら `#t` を、そうでなければ `#f` を返します。

```scheme
(boolean? #f)                                     ⇒ #t
(boolean? 0)                                      ⇒ #f
```

#### `not object` 〔手続き〕
#### `false? object` 〔手続き＋〕

これらの手続きは、`object` が偽なら `#t` を、そうでなければ `#f` を返します。言い換えると、
真偽値を反転します。この2つの手続きは同一の意味論を持ちます。名前が違うのは、検査に
異なる含みを与えるためです。

```scheme
(not #t)                                          ⇒ #f
(not 3)                                           ⇒ #f
(not (list 3))                                    ⇒ #f
(not #f)                                          ⇒ #t
```

#### `boolean=? obj1 obj2` 〔手続き＋〕

この述語は、`obj1` と `obj2` がともに真であるか、ともに偽であるとき、かつそのときに
かぎり真です。

#### `boolean/and object …` 〔手続き＋〕

この手続きは、引数のどれも `#f` でなければ `#t` を返します。そうでなければ `#f` を返し
ます。

#### `boolean/or object …` 〔手続き＋〕

この手続きは、引数のすべてが `#f` なら `#f` を返します。そうでなければ `#t` を返します。

## 10.2 シンボル

MIT Scheme は2種類のシンボルを提供します。インターンされたもの（interned）と、インターン
されていないもの（uninterned）です。インターンされたシンボルは、インターンされていない
シンボルよりずっとよく使われ、作る方法も多いです。インターンされたシンボルは、手続き
`read` が認識する外部表現を持ちますが、インターンされていないシンボルは持ちません[^1]。

インターンされたシンボルは、きわめて有用な性質を持ちます。名前が `string=?` の意味で同じ
であるインターンされたシンボルは、どの2つも同じオブジェクトです（すなわち互いに `eq?`
です）。**インターン（interned）**という語は、これを成し遂げるインターンの過程を指します。
インターンされていないシンボルはこの性質を共有しません。

インターンされたシンボルの名前は、その大文字小文字で区別されません。このため、MIT
Scheme は、シンボルが作られるとき、インターンされたシンボルの名前のすべての英字を特定の
大文字小文字（小文字）に変換します。インターンされたシンボルの名前が（`symbol->string`
を使って）参照されたり、（`write` を使って）書き出されたりするとき、この大文字小文字で
現れます。名前が小文字であることに依存するのはよくない考えです。実際、これをもう一歩
進めるほうがよいです。シンボルの名前が一様な大文字小文字であることに依存しないでください。

インターンされたシンボルを書く規則は、識別子を書く規則と同じです（1.3.3節「識別子」を
見よ）。リテラルの式の一部として返されたか、`read` 手続きで読まれ、その後 `write` 手続き
で書き出された、インターンされたシンボルは、（`eq?` の意味で）同一のシンボルとして読み
戻されます。

ふつう、以前に書き出されたインターンされたシンボルを読み込むと、同じシンボルが得られる
ことも成り立ちます。例外は、手続き `string->symbol` と `intern` が作るシンボルです。
これらは、シンボルの名前が特殊文字や非標準の大文字小文字の文字を含むために、この write/
read の不変性が成り立たないかもしれないシンボルを作れます[^2]。

インターンされていないシンボルの外部表現は特別です。インターンされたシンボルと区別し、
`read` 手続きに認識されないようにするためです。

```scheme
(string->uninterned-symbol "foo")
     ⇒ #[uninterned-symbol 30 foo]
```

この節で、シンボルを値として返す手続きは、つねにインターンされたシンボルを返すか、つねに
インターンされていないシンボルを返します。シンボルを引数として受け取る手続きは、つねに
インターンされたシンボルとインターンされていないシンボルのどちらも受け取り、両者を区別
しません。

#### `symbol? object` 〔手続き〕

`object` がシンボルなら `#t` を、そうでなければ `#f` を返します。

```scheme
(symbol? 'foo)                                              ⇒ #t
(symbol? (car '(a b)))                                      ⇒ #t
(symbol? "bar")                                             ⇒ #f
```

#### `symbol->string symbol` 〔手続き〕

`symbol` の名前を文字列として返します。`symbol` が `string->symbol` によって返された
ものなら、この手続きの値は、`string->symbol` に渡された文字列と（`string=?` の意味で）
同一です。この手続きが返す文字列に `string-set!` のような変更手続きを適用するのは
エラーです。

```scheme
(symbol->string 'flying-fish)           ⇒ "flying-fish"
(symbol->string 'Martin)                ⇒ "martin"
(symbol->string (string->symbol "Malvina"))
                                        ⇒ "Malvina"
```

インターンされていない2つの異なるシンボルが同じ名前を持ちうることに注意してください。

#### `intern string` 〔手続き＋〕

名前が `string` であるインターンされたシンボルを返します。シンボルを生成する前に、
`string` を標準の大文字小文字に変換します。これはインターンされたシンボルを作る好ましい
方法です。実装がシンボルの名前にどの大文字小文字を使うかにかかわらず、次を保証するから
です。

```scheme
(eq? 'bitBlt (intern "bitBlt")) ⇒ #t
```

ユーザは `string` が識別子の規則（1.3.3節「識別子」を見よ）に従うよう気をつけるべきです。
そうでなければ、結果のシンボルはそれ自身として読めません。

#### `intern-soft string` 〔手続き＋〕

名前が `string` であるインターンされたシンボルを返します。シンボルを生成する前に、
`string` を標準の大文字小文字に変換します。そのようなインターンされたシンボルが存在
しなければ、`#f` を返します。

これは `intern` とまったく同じですが、インターンされたシンボルを作らず、すでに存在する
シンボルだけを返す点が異なります。

#### `string->symbol string` 〔手続き〕

名前が `string` であるインターンされたシンボルを返します。この手続きを使って、特殊文字
や小文字を含む名前のシンボルを作れますが、そのようなシンボルはそれ自身として読めない
ので、作るのはふつうよくない考えです。`symbol->string` を見よ。

```scheme
(eq? 'mISSISSIppi 'mississippi)         ⇒ #t
(string->symbol "mISSISSIppi")
     ⇒ 名前が "mISSISSIppi" であるシンボル
(eq? 'bitBlt (string->symbol "bitBlt")) ⇒ #f
(eq? 'JollyWog
      (string->symbol
        (symbol->string 'JollyWog)))    ⇒ #t
(string=? "K. Harper, M.D."
           (symbol->string
             (string->symbol
               "K. Harper, M.D.")))     ⇒ #t
```

#### `string->uninterned-symbol string` 〔手続き＋〕

名前が `string` である、新しく割り当てられたインターンされていないシンボルを返します。
`string` にどの大文字小文字や文字を使うかは重要ではありません。注意: これはシンボルを
作るもっとも速い方法です。

#### `generate-uninterned-symbol [object]` 〔手続き＋〕

他のどのオブジェクトとも異なることが保証された、新しく割り当てられたインターンされて
いないシンボルを返します。シンボルの名前は、接頭辞の文字列に、内部カウンタの（正確な
非負整数の）値を続けたものからなります。カウンタははじめ 0 で、この手続きを呼ぶたびに
増えます。

省略可能引数 `object` は、シンボルがどう生成されるかを制御するのに使われます。次の値の
いずれかをとれます。

- `object` が省かれるか `#f` なら、接頭辞は `"G"` です。
- `object` が正確な非負整数なら、結果を生成する前に内部カウンタがその整数に設定され
  ます。
- `object` が文字列なら、それが接頭辞として使われます。
- `object` がシンボルなら、その名前が接頭辞として使われます。

```scheme
(generate-uninterned-symbol)
     ⇒ #[uninterned-symbol 31 G0]
(generate-uninterned-symbol)
     ⇒ #[uninterned-symbol 32 G1]
(generate-uninterned-symbol 'this)
     ⇒ #[uninterned-symbol 33 this2]
(generate-uninterned-symbol)
     ⇒ #[uninterned-symbol 34 G3]
(generate-uninterned-symbol 100)
     ⇒ #[uninterned-symbol 35 G100]
(generate-uninterned-symbol)
     ⇒ #[uninterned-symbol 36 G101]
```

#### `symbol-append symbol …` 〔手続き＋〕

与えられたシンボルの名前を連結して作った名前を持つ、インターンされたシンボルを返します。
この手続きは引数の名前の大文字小文字を保つので、引数の1つ以上の名前が非標準の大文字
小文字なら、結果も非標準の大文字小文字になります。

```scheme
(symbol-append 'foo- 'bar)                      ⇒ foo-bar
;; 引数はインターンされていなくてもよい:
(symbol-append 'foo- (string->uninterned-symbol "baz"))
                                                ⇒ foo-baz
;; 結果は引数と同じ大文字小文字を持つ:
(symbol-append 'foo- (string->symbol "BAZ"))           ⇒ foo-BAZ
```

#### `symbol-hash symbol` 〔手続き＋〕

`symbol` のハッシュ番号を返します。これは `symbol` の名前に `string-hash` を呼んで計算
されます。ハッシュ番号は正確な非負整数です。

#### `symbol-hash-mod symbol modulus` 〔手続き＋〕

`modulus` は正確な正整数でなければなりません。次と等価です。

```scheme
(modulo (symbol-hash symbol) modulus)
```

この手続きはハッシュ表を構築する便宜のために提供されています。ただし、シンボルをキーと
するハッシュ表を作るには、ふつう `make-eq-hash-table` を使うほうが好ましいです。`eq?`
ハッシュ表のほうがずっと速いからです。

#### `symbol<? symbol1 symbol2` 〔手続き＋〕

この手続きはシンボルに全順序を計算します。次と等価です。

```scheme
(string<? (symbol->string symbol1)
           (symbol->string symbol2))
```

## 10.3 セル

**セル（cell）**は、要素が1つだけである点を除いてペアに似たデータ構造です。状態を管理
するのに役立ちます。

#### `cell? object` 〔手続き＋〕

`object` がセルなら `#t` を、そうでなければ `#f` を返します。

#### `make-cell object` 〔手続き＋〕

内容が `object` である、新しく割り当てられたセルを返します。

#### `cell-contents cell` 〔手続き＋〕

`cell` の現在の内容を返します。

#### `set-cell-contents! cell object` 〔手続き＋〕

`cell` の内容を `object` に変えます。未規定の値を返します。

#### `bind-cell-contents! cell object thunk` 〔手続き＋〕

`cell` の内容を `object` に変え、`thunk` を引数なしで呼び、それから `cell` のもとの内容を
復元し、`thunk` が返した値を返します。これは、継続が使われたときのふるまいを含めて、
変数の動的束縛と完全に等価です（2.3節「動的束縛」を見よ）。

## 10.4 レコード

MIT Scheme は**レコード（record）**の抽象を提供します。これは、名前の付いた成分を持つ
構造を組み立てる、単純で柔軟な仕組みです。レコードは、この節で定義する手続きを使って
定義・アクセスできます。柔軟性は劣るがより簡潔なレコードの操作方法は、`define-structure`
特殊形式を使うことです（2.10節「構造体定義」を見よ）。

#### `make-record-type type-name field-names` 〔手続き＋〕

レコード型記述子（record-type descriptor）、すなわち他のすべてから互いに素な新しい
データ型を表す値を返します。`type-name` 引数は文字列でなければなりませんが、デバッグの
目的（新しい型のレコードの表示表現など）にのみ使われます。`field-names` 引数は、新しい
型のレコードのフィールドを名指すシンボルのリストです。リストに重複があればエラーです。
レコード型記述子がどう表現されるかは未規定です。

#### `record-constructor record-type [field-names]` 〔手続き＋〕

`record-type` が表す型の新しいメンバーを構築する手続きを返します。返される手続きは、
与えられたリスト `field-names` のシンボルの数とちょうど同じ数の引数を受け取ります。
これらは、順に、新しいレコードのそれらのフィールドの初期値として使われ、そのレコードが
コンストラクタ手続きによって返されます。`field-names` のリストに名指されないフィールド
の値は未規定です。`field-names` 引数は、既定で、`record-type` が表す型を作った
`make-record-type` の呼び出しでの `field-names` のリストです。`field-names` 引数が
与えられれば、それが重複や、既定のリストにないシンボルを含めばエラーです。

#### `record-predicate record-type` 〔手続き＋〕

`record-type` が表す型のメンバーシップを検査する手続きを返します。返される手続きは
ちょうど1つの引数を受け取り、引数が示されたレコード型のメンバーなら `#t` を、そうでなけ
れば `#f` を返します。

#### `record-accessor record-type field-name` 〔手続き＋〕

`record-type` が表す型のメンバーの特定のフィールドの値を読む手続きを返します。返される
手続きはちょうど1つの引数を受け取り、それは適切な型のレコードでなければなりません。手続き
はそのレコードのシンボル `field-name` が名指すフィールドの現在の値を返します。シンボル
`field-name` は、`record-type` が表す型を作った `make-record-type` の呼び出しでの
フィールド名のリストのメンバーでなければなりません。

#### `record-modifier record-type field-name` 〔手続き＋〕

`record-type` が表す型のメンバーの特定のフィールドの値を書く手続きを返します。返される
手続きはちょうど2つの引数を受け取ります。1つ目は適切な型のレコード、2つ目は任意の
Scheme の値です。手続きはそのレコードのシンボル `field-name` が名指すフィールドを、
与えられた値を含むよう変更します。変更子手続きの返す値は未規定です。シンボル `field-name`
は、`record-type` が表す型を作った `make-record-type` の呼び出しでのフィールド名の
リストのメンバーでなければなりません。

#### `record? object` 〔手続き＋〕

`object` が任意の型のレコードなら `#t` を、そうでなければ `#f` を返します。`record?` は
任意の Scheme の値について真でありうることに注意してください。もちろん、ある特定の値に
ついて `#t` を返すなら、`record-type-descriptor` がその値に適用でき、適切な記述子を
返します。

#### `record-type-descriptor record` 〔手続き＋〕

`record` の型を表すレコード型記述子を返します。すなわち、たとえば返された記述子を
`record-predicate` に渡すと、結果の述語は `record` を渡されたときに `#t` を返します。
返された記述子が、`record` を作ったコンストラクタ手続きを作った呼び出しで
`record-constructor` に渡されたものであるとはかぎらないことに注意してください。

#### `record-type? object` 〔手続き＋〕

`object` がレコード型記述子なら `#t` を、そうでなければ `#f` を返します。

#### `record-type-name record-type` 〔手続き＋〕

`record-type` が表す型に結びついた型名を返します。返される値は、`record-type` が表す型
を作った `make-record-type` の呼び出しで与えられた `type-name` 引数に `eqv?` です。

#### `record-type-field-names record-type` 〔手続き＋〕

`record-type` が表す型のメンバーのフィールドを名指すシンボルのリストを返します。返される
値は、`record-type` が表す型を作った `make-record-type` の呼び出しで与えられた
`field-names` 引数に `equal?` です[^3]。

## 10.5 約束

#### `delay expression` 〔特殊形式〕

`delay` 構文は、手続き `force` と一緒に使って、遅延評価（lazy evaluation）または必要
時呼び出し（call by need）を実装します。`(delay expression)` は、**約束（promise）**と
呼ばれるオブジェクトを返します。これは将来のある時点で、（`force` 手続きによって）
`expression` を評価し、結果の値を渡すよう求められるかもしれません。

#### `force promise` 〔手続き〕

`promise` の値を強制します。約束の値がまだ計算されていなければ、値が計算されて返され
ます。約束の値はキャッシュされます（「メモ化」されます）。2度目に強制されると、以前に
計算された値が、再計算なしに返されます。

```scheme
(force (delay (+ 1 2)))                             ⇒ 3

(let ((p (delay (+ 1 2))))
  (list (force p) (force p)))                     ⇒ (3 3)
(define head car)

(define tail
  (lambda (stream)
    (force (cdr stream))))
(define a-stream
  (letrec ((next
            (lambda (n)
              (cons n (delay (next (+ n 1)))))))
    (next 0)))

(head (tail (tail a-stream)))                     ⇒ 2
```

#### `promise? object` 〔手続き＋〕

`object` が約束なら `#t` を、そうでなければ `#f` を返します。

#### `promise-forced? promise` 〔手続き＋〕

`promise` が強制されてその値がキャッシュされていれば `#t` を、そうでなければ `#f` を
返します。

#### `promise-value promise` 〔手続き＋〕

`promise` が強制されてその値がキャッシュされていれば、この手続きはキャッシュされた値を
返します。そうでなければ、エラーが通知されます。

`force` と `delay` は、おもに関数的な様式で書かれたプログラムのためのものです。次の例は
よいプログラミングの様式を示すものとは考えるべきではありませんが、約束の値が高々1回しか
計算されないという性質を示しています。

```scheme
(define count 0)

(define p
  (delay
   (begin
     (set! count (+ count 1))
     (* x 3))))

(define x 5)
 count                                            ⇒ 0
 p                                                ⇒ #[promise 54]
 (force p)                                        ⇒ 15
 p                                                ⇒ #[promise 54]
 count                                            ⇒ 1
 (force p)                                        ⇒ 15
 count                                            ⇒ 1
```

`delay` と `force` のありうる実装を挙げます。式

```scheme
(delay expression)
```

が、手続き呼び出し

```scheme
(make-promise (lambda () expression))
```

と同じ意味を持つと定めます。ここで `make-promise` は次のように定義されます。

```scheme
(define make-promise
   (lambda (proc)
     (let ((already-run? #f)
            (result #f))
       (lambda ()
          (cond ((not already-run?)
                  (set! result (proc))
                  (set! already-run? #t)))
          result))))
```

ここでは約束は引数のない手続きとして実装され、`force` は単にその引数を呼びます。

```scheme
(define force
   (lambda (promise)
     (promise)))
```

`delay` と `force` のこの意味論のさまざまな拡張が、いくつかの実装でサポートされています
（これらのどれも、現在 MIT Scheme ではサポートされていません）。

- 約束でないオブジェクトに `force` を呼ぶと、単にそのオブジェクトを返すかもしれません。
- 約束を、強制された値と操作的に区別する手段がまったくないこともありえます。すなわち、
  次のような式が、実装に応じて `#t` か `#f` のどちらかに評価されるかもしれません。

  ```scheme
  (eqv? (delay 1) 1)                      ⇒ unspecified
  (pair? (delay (cons 1 2)))              ⇒ unspecified
  ```

- 実装によっては「暗黙の強制（implicit forcing）」を実装します。約束の値が `car` や `+`
  のような基本手続きによって強制されます。

  ```scheme
  (+ (delay (* 3 7)) 13)                  ⇒ 34
  ```

## 10.6 ストリーム

約束に加えて、MIT Scheme は**ストリーム（stream）**と呼ばれるより高水準の抽象をサポート
します。ストリームはリストに似ていますが、ストリームの末尾は参照されるまで計算されない
点が異なります。これにより、ストリームを無限に長いリストを表すのに使えます。

#### `stream object …` 〔手続き＋〕

要素が引数である、新しく割り当てられたストリームを返します。式 `(stream)` は空ストリーム、
すなわちストリーム終端マーカーを返すことに注意してください。

#### `list->stream list` 〔手続き＋〕

要素が `list` の要素である、新しく割り当てられたストリームを返します。`(apply stream
list)` と等価です。

#### `stream->list stream` 〔手続き＋〕

要素が `stream` の要素である、新しく割り当てられたリストを返します。`stream` が無限の
長さを持てば、この手続きは終わりません。次のように定義できたはずです。

```scheme
(define (stream->list stream)
   (if (stream-null? stream)
         '()
         (cons (stream-car stream)
               (stream->list (stream-cdr stream)))))
```

#### `cons-stream object expression` 〔特殊形式＋〕

新しく割り当てられたストリームのペアを返します。`(cons object (delay expression))` と
等価です。

#### `stream-pair? object` 〔手続き＋〕

`object` が、cdr に約束を含むペアなら `#t` を、そうでなければ `#f` を返します。次のように
定義できたはずです。

```scheme
(define (stream-pair? object)
  (and (pair? object)
        (promise? (cdr object))))
```

#### `stream-car stream` 〔手続き＋〕
#### `stream-first stream` 〔手続き＋〕

`stream` の最初の要素を返します。`stream-car` は `car` と等価です。`stream-first` は
`stream-car` の同義語です。

#### `stream-cdr stream` 〔手続き＋〕
#### `stream-rest stream` 〔手続き＋〕

`stream` の最初の末尾を返します。`(force (cdr stream))` と等価です。`stream-rest` は
`stream-cdr` の同義語です。

#### `stream-null? stream` 〔手続き＋〕

`stream` がストリーム終端マーカーなら `#t` を、そうでなければ `#f` を返します。これは
`null?` と等価ですが、ストリームの終端を検査するときはつねにこちらを使うべきです。

#### `stream-length stream` 〔手続き＋〕

`stream` の要素の数を返します。`stream` が無限の数の要素を持てば、この手続きは終わり
ません。この手続きは `stream` を構成するすべての約束を強制することに注意してください。

#### `stream-ref stream k` 〔手続き＋〕

`k` で添字づけられる `stream` の要素、すなわち `k` 番目の要素を返します。`k` は `stream`
の長さより厳密に小さい正確な非負整数でなければなりません。

#### `stream-head stream k` 〔手続き＋〕

`stream` の最初の `k` 要素をリストとして返します。`k` は `stream` の長さより厳密に小さい
正確な非負整数でなければなりません。

#### `stream-tail stream k` 〔手続き＋〕

`k` で添字づけられる `stream` の末尾、すなわち `k` 番目の末尾を返します。これは
`stream-cdr` を `k` 回行うのと等価です。`k` は `stream` の長さより厳密に小さい正確な
非負整数でなければなりません。

#### `stream-map procedure stream stream …` 〔手続き＋〕

新しく割り当てられたストリームを返します。各要素は、ストリームの対応する要素を引数として
`procedure` を起動した結果です。

## 10.7 弱いペア

**弱いペア（weak pair）**は、オブジェクトをガベージコレクションから守らずにそれを指す
データ構造を組み立てる仕組みです。弱いペアの car はそのポインタを弱く保持し、cdr は
ふつうの形でポインタを保持します。弱いペアの car のオブジェクトが、他のどのデータ構造
からもふつうの形で保持されていなければ、それはガベージコレクションされます。

注意: 弱いペアはペアではありません。すなわち、述語 `pair?` を満たしません。

#### `weak-pair? object` 〔手続き＋〕

`object` が弱いペアなら `#t` を、そうでなければ `#f` を返します。

#### `weak-cons car cdr` 〔手続き＋〕

成分が `car` と `cdr` である、新しい弱いペアを割り当てて返します。car の成分は弱く保持
されます。

#### `weak-pair/car? weak-pair` 〔手続き＋〕

この述語は、`weak-pair` の car がガベージコレクションされていれば `#f` を、そうでなけ
れば `#t` を返します。言い換えると、`weak-pair` が妥当な car の成分を持てば真です。

#### `weak-car weak-pair` 〔手続き＋〕

`weak-pair` の car の成分を返します。car の成分がガベージコレクションされていれば、この
演算は `#f` を返しますが、それが car に格納されていた値であっても `#f` を返しえます。

ふつう、`weak-pair/car?` は、`weak-car` が妥当な値を返すかどうかを判定するのに使われ
ます。これを行う明らかな方法は次のようなものでしょう。

```scheme
(if (weak-pair/car? x)
     (weak-car x)
     ...)
```

しかし、`weak-pair/car?` の呼び出しと `weak-car` のあいだにガベージコレクションが起こり
うるので、これはつねに正しく働くとはかぎりません。かわりに、つねに働く次のものを使う
べきです。

```scheme
(or (weak-car x)
     (and (not (weak-pair/car? x))
           ...))
```

後者の式が働く理由は、`weak-car` が `#f` を返すのがちょうど2つの場合だからです。car の
成分が `#f` のときと、car の成分がガベージコレクションされているときです。前者の場合、
2つの呼び出しのあいだにガベージコレクションが起きても、`#f` は決してガベージコレクション
されないので、問題になりません。後者の場合も、car の成分がもはや存在せず、ガベージ
コレクタの影響を受けえないので、問題になりません。

#### `weak-set-car! weak-pair object` 〔手続き＋〕

`weak-pair` の car の成分を `object` に設定し、未規定の結果を返します。

#### `weak-cdr weak-pair` 〔手続き＋〕

`weak-pair` の cdr の成分を返します。

#### `weak-set-cdr! weak-pair object` 〔手続き＋〕

`weak-pair` の cdr の成分を `object` に設定し、未規定の結果を返します。

---

[^1]: 古い Lisp 方言では、インターンされていないシンボルはかなり重要だった。これは、
    シンボルが複雑なデータ構造だったからである。値セル（と、ときには関数セル）を持つほか、
    これらの構造は属性リストを含んでいた。このため、インターンされていないシンボルは
    しばしばその属性リストのためだけに使われた。こう使われるインターンされていない
    シンボルは、実体のない属性リスト（disembodied property list）と呼ばれることもあった。
    MIT Scheme では、シンボルは属性リストも、名前以外のどの成分も持たない。実体のない
    属性リストに似た別のデータ構造がある。1次元表（11.2節「1次元表」を見よ）である。
    こうした理由から、インターンされていないシンボルは MIT Scheme ではあまり役立たない。
    実際、そのおもな目的は、Scheme コードを生成するプログラムで一意な変数名の生成を
    単純にすることである。

[^2]: MIT Scheme は、特定のインターンされたシンボルの集合を自身の用途のために予約して
    いる。これらの予約シンボルを使うと、それらに依存する特定のソフトウェアを壊すことが
    ありえる。予約シンボルはすべて、文字 `#[` で始まり文字 `]` で終わる名前を持つ。
    したがってこれらのシンボルはどれも手続き `read` で読めず、それゆえ偶然に使われる
    ことはまずない。たとえば `(intern "#[unnamed-procedure]")` は予約シンボルを作る。

[^3]: MIT Scheme では、返されるリストはつねに新しく割り当てられる。
