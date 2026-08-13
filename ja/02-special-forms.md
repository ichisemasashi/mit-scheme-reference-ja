<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 2 特殊形式

**特殊形式（special form）**とは、特別な評価規則に従う式です。この章では、基本的な
Scheme の特殊形式を説明します。

## 2.1 Lambda 式

#### `lambda formals expression expression …` 〔特殊形式〕

lambda 式は手続きに評価されます。lambda 式が評価されたときに有効な環境は、手続きの
一部として覚えられます。これを**閉包環境（closing environment）**と呼びます。あとで
その手続きが何らかの引数とともに呼ばれると、閉包環境が、仮引数リストの変数を新しい
場所に束縛して拡張され、それらの場所が、これから述べる規則に従って引数で埋められ
ます。この過程で作られる新しい環境を、**呼び出し環境（invocation environment）**と
呼びます。

呼び出し環境が構築されると、lambda 式の本体の式が、その中で順に評価されます。これは、
lambda 式が束縛する変数の領域が、本体のすべての式であることを意味します。本体の最後
の式を評価した結果が、手続き呼び出しの結果として返されます。

`formals`、すなわち仮引数リストは、しばしば**ラムダリスト（lambda list）**と呼ばれ
ます。

仮引数と引数を対応づける過程は、やや込み入っています。引数には3種類あり、対応づけは
それぞれを順に扱います。

**必須（Required）**
必須引数はすべて、まず引数と対応づけられます。引数が必須引数より少なければ、
`condition-type:wrong-number-of-arguments` 型のエラーが通知されます。引数が必須
引数より多く、それ以上の引数がなければ、このエラーが通知されます。

**省略可能（Optional）**
必須引数がすべて対応づけられると、省略可能引数が残りの引数と対応づけられます。引数が
省略可能引数より少なければ、対応づかなかった引数は**デフォルトオブジェクト（default
object）**と呼ばれる特別なオブジェクトに束縛されます。引数が省略可能引数より多く、
それ以上の引数がなければ、`condition-type:wrong-number-of-arguments` 型のエラーが
通知されます。デフォルトオブジェクトに対してのみ真となる述語 `default-object?` を
使えば、どの省略可能引数が与えられ、どれがデフォルトになったかを判定できます。

**残余（Rest）**
最後に、残余引数があれば（1つしか置けません）、残りの引数がリストにされ、そのリストが
残余引数に束縛されます。（残りの引数がなければ、残余引数は空リストに束縛されます。）

ほかのいくつかの Lisp 実装と違って、Scheme では、残余引数が束縛されるリストはつねに
新しく割り当てられます。それは無限の存続期間を持ち、手続きの呼び出し元に影響を与えず
に書き換えられます。

特別に認識されるキーワードが、`formals` の引数をこれら3つのクラスに分けます。ここで
使われるキーワードは `#!optional`、`.`、`#!rest` です。標準 Scheme が定めるのは `.`
だけで、ほかのキーワードは MIT Scheme の拡張であることに注意してください。`formals`
において `#!rest` は `.` と同じ意味を持ちます。

これらのキーワードの使い方は、例で説明するのがいちばんです。次に典型的なラムダリスト
を挙げ、どの引数が必須・省略可能・残余であるかの説明を添えます。例では `#!rest` を
使いますが、それが現れるところはどこでも `.` で置き換えられます。

`(a b c)`
`a`、`b`、`c` はすべて必須。手続きにはちょうど3つの引数を渡さなければなりません。

`(a b #!optional c)`
`a` と `b` は必須、`c` は省略可能。手続きには2つか3つの引数を渡せます。

`(#!optional a b c)`
`a`、`b`、`c` はすべて省略可能。手続きには0個から3個までの任意個の引数を渡せます。

`a`
`(#!rest a)`
この2つの例は等価です。`a` は残余引数です。手続きには任意個の引数を渡せます。注意:
これは `#!rest` の代わりに `.` を使えない唯一の場合です。

`(a b #!optional c d #!rest e)`
`a` と `b` は必須、`c` と `d` は省略可能、`e` は残余。手続きには2つ以上の引数を渡せ
ます。

lambda 式の例をいくつか挙げます。

```scheme
(lambda (x) (+ x x))                     ⇒ #[compound-procedure 53]

((lambda (x) (+ x x)) 4)                          ⇒ 8

(define reverse-subtract
  (lambda (x y)
    (- y x)))
(reverse-subtract 7 10)                           ⇒ 3

(define foo
  (let ((x 4))
    (lambda (y) (+ x y))))
(foo 6)                                           ⇒ 10
```

#### `named-lambda formals expression expression …` 〔特殊形式＋〕

`named-lambda` 特殊形式は `lambda` に似ていますが、`formals` の最初の「必須引数」が
引数ではなく、結果の手続きの名前である点が異なります。したがって `formals` は少なく
とも1つの必須引数を持たなければなりません。この名前には意味論上の意味はありませんが、
手続きの外部表現に含まれるので、デバッグに役立ちます。MIT Scheme では、`lambda` は、
「名前なし」を意味する特別な名前を持つ `named-lambda` として実装されています。

```scheme
(named-lambda (f x) (+ x x))     ⇒ #[compound-procedure 53 f]
((named-lambda (f x) (+ x x)) 4)                   ⇒ 8
```

## 2.2 字句束縛

3つの束縛構文 `let`、`let*`、`letrec` が、Scheme にブロック構造を与えます。3つの構文
の書き方は同じですが、変数束縛のために確立する領域が異なります。`let` 式では、初期値
はどの変数も束縛される前に計算されます。`let*` 式では、評価と束縛が順に交互に行われ
ます。`letrec` 式では、初期値が計算されているあいだ、すべての束縛が有効です（したがって
相互再帰的な定義が書けます）。

#### `let ((variable init) …) expression expression …` 〔特殊形式〕

`init` が現在環境で（何らかの未規定の順序で）評価され、変数がその結果を保持する新しい
場所に束縛され、式が拡張された環境で順に評価され、最後の式の値が返されます。変数の
それぞれの束縛は、式をその領域とします。

MIT Scheme では、どの `init` も省略でき、その場合、対応する変数は未代入になります。

次の2つが等価であることに注意してください。

```scheme
(let ((variable init) ...) expression expression ...)
((lambda (variable ...) expression expression ...) init ...)
```

例をいくつか挙げます。

```scheme
(let ((x 2) (y 3))
  (* x y))                                         ⇒ 6
(let ((x 2) (y 3))
  (let ((foo (lambda (z) (+ x y z)))
        (x 7))
    (foo 4)))                                      ⇒ 9
```

「名前付き let」については、2.9節「反復」を見よ。

#### `let* ((variable init) …) expression expression …` 〔特殊形式〕

`let*` は `let` に似ていますが、束縛が左から右へ順に行われ、ある束縛の領域が `let*`
式のその束縛より右の部分である点が異なります。したがって2番目の束縛は、1番目の束縛が
見える環境で行われ、以下同様です。

次の2つが等価であることに注意してください。

```scheme
(let* ((variable1 init1)
       (variable2 init2)
       ...
       (variableN initN))
   expression
   expression ...)
(let ((variable1 init1))
  (let ((variable2 init2))
    ...
       (let ((variableN initN))
         expression
         expression ...)
    ...))
```

例を挙げます。

```scheme
(let ((x 2) (y 3))
  (let* ((x 7)
          (z (+ x y)))
    (* z x)))                                      ⇒ 70
```

#### `letrec ((variable init) …) expression expression …` 〔特殊形式〕

変数が未代入の値を保持する新しい場所に束縛され、`init` が拡張された環境で（何らかの
未規定の順序で）評価され、各変数が対応する `init` の結果に代入され、式が拡張された
環境で順に評価され、最後の式の値が返されます。変数のそれぞれの束縛は、`letrec` 式の
全体を領域とするので、相互再帰的な手続きを定義できます。

MIT Scheme では、どの `init` も省略でき、その場合、対応する変数は未代入になります。

```scheme
(letrec ((even?
            (lambda (n)
               (if (zero? n)
                    #t
                    (odd? (- n 1)))))
           (odd?
            (lambda (n)
               (if (zero? n)
                    #f
                    (even? (- n 1))))))
   (even? 88))                                   ⇒ #t
```

`letrec` に対する1つの制限がとても重要です。どの `init` も、どの変数の値も代入したり
参照したりせずに評価できなければなりません。この制限を破ると、それはエラーです。この
制限が必要なのは、Scheme が引数を名前渡しではなく値渡しするからです。`letrec` の
もっともよくある使い方では、すべての `init` が `lambda` 式か `delay` 式であり、制限は
自動的に満たされます。

## 2.3 動的束縛

#### `fluid-let ((variable init) …) expression expression …` 〔特殊形式＋〕

`init` が現在環境で（何らかの未規定の順序で）評価され、変数の現在の値が保存され、その
結果が変数に代入され、式が現在環境で順に評価され、変数がもとの値に戻され、最後の式の
値が返されます。

この特殊形式の書き方は `let` のそれに似ていますが、`fluid-let` は既存の変数を一時的に
再束縛します。`let` と違って、`fluid-let` は新しい束縛を作りません。かわりに、各 `init`
の値を、対応する変数の（字句スコープの規則で決まる）束縛に代入します。

MIT Scheme では、どの `init` も省略でき、その場合、対応する変数は一時的に未代入に
なります。

変数のいずれかが未束縛なら、`condition-type:unbound-variable` 型のエラーが通知され
ます。ただし、`fluid-let` は副作用によって働くので、フォームに入るときにどの変数が
未代入であっても正当です。

`fluid-let` と `let` の違いを示す例を挙げます。まず、`let` が変数の束縛にどう影響する
かを見ます。

```scheme
(define variable #t)
(define (access-variable) variable)
variable                                         ⇒ #t
(let ((variable #f))
   (access-variable))                            ⇒ #t
variable                                         ⇒ #t
```

この場合 `access-variable` が `#t` を返すのは、それが `variable` を `#t` に束縛した
環境で定義されているからです。一方、`fluid-let` は既存の変数を一時的に再利用します。

```scheme
variable                                         ⇒ #t
(fluid-let ((variable #f))                       ;古い束縛を再利用する
   (access-variable))                            ⇒ #f
variable                                         ⇒ #t
```

動的束縛の**存続期間（extent）**は、変数が新しい値を保持している時間の区間と定義され
ます。ふつうこの区間は、本体に入ったときに始まり、本体を出たときに終わります。逐次的な
機械では、ふつう連続した区間です。しかし、Scheme は第一級の継続を持つので、本体を出て
から再び入る、ということを望むだけ何度でもできます。この状況では、存続期間は連続しなく
なります。

継続を起動して本体を出るとき、新しい値が保存され、変数が古い値に設定されます。その後、
継続を起動して本体に再び入ると、古い値が保存され、変数が新しい値に設定されます。加えて、
本体の内と外の両方で起こる変数への副作用は、本体を出たり入ったりするのに継続を繰り返し
使っても、保たれます。

動的束縛と継続の相互作用を示す、込み入った例を挙げます。

```scheme
(define (complicated-dynamic-binding)
   (let ((variable 1)
           (inside-continuation))
      (write-line variable)
      (call-with-current-continuation
       (lambda (outside-continuation)
         (fluid-let ((variable 2))
            (write-line variable)
            (set! variable 3)
            (call-with-current-continuation
             (lambda (k)
               (set! inside-continuation k)
               (outside-continuation #t)))
            (write-line variable)
            (set! inside-continuation #f))))
      (write-line variable)
      (if inside-continuation
           (begin
             (set! variable 4)
             (inside-continuation #f)))))
```

`(complicated-dynamic-binding)` を評価すると、コンソールに次が書き出されます。

```scheme
1
2
1
3
4
```

解説: 最初に書き出される2つの値は、`variable` の初期束縛と、`fluid-let` の本体に入った
あとの新しい束縛です。それらが書き出された直後、`variable` は `3` に設定され、続いて
`outside-continuation` が起動され、私たちは本体を出ます。この時点で `1` が書き出され、
本体を離れたので `variable` のもとの値が復元されたことを示します。次に `variable` を
`4` に設定し、`inside-continuation` を起動して本体に再び入ります。この時点で `3` が
書き出され、以前に本体の中で起こった副作用が保たれたことを示します。最後に、本体を
ふつうに出て `4` を書き出し、本体の外で起こった副作用も保たれたことを示します。

## 2.4 定義

#### `define variable [expression]` 〔特殊形式〕
#### `define formals expression expression …` 〔特殊形式〕

定義は、式が許される文脈のうち一部で有効ですが、すべてではありません。定義は、
プログラムのトップレベルと、lambda 本体の先頭（すなわち `lambda`、`let`、`let*`、
`letrec`、`fluid-let`、または「手続き define」式の本体）でのみ現れます。プログラムの
トップレベルに現れる定義を**トップレベル定義（top-level definition）**と呼び、本体の
先頭に現れる定義を**内部定義（internal definition）**と呼びます。

`define` の2つ目の形（「手続き define」と呼ばれます）では、構成要素 `formals` は
`named-lambda` 式の同名の構成要素と同じです。実際、この2つの式は等価です。

```scheme
(define (name1 name2 ...)
   expression
   expression ...)
(define name1
  (named-lambda (name1 name2 ...)
    expression
    expression ...))
```

### 2.4.1 トップレベル定義

トップレベル定義

```scheme
(define variable expression)
```

は、`variable` が束縛されていれば、本質的に次の代入式と同じ効果を持ちます。

```scheme
(set! variable expression)
```

しかし、`variable` が束縛されていなければ、`define` は代入を行う前に、現在環境の
新しい場所に `variable` を束縛します（束縛されていない変数への `set!` はエラーです）。
`expression` を省くと、変数は未代入になります。そのような変数を参照しようとするのは
エラーです。

```scheme
(define add3
    (lambda (x) (+ x 3)))                      ⇒ unspecified
(add3 3)                                       ⇒ 6

(define first car)                             ⇒ unspecified
(first '(1 2))                                 ⇒ 1

(define bar)                                   ⇒ unspecified
bar                                            error> Unassigned variable
```

### 2.4.2 内部定義

**内部定義**とは、プログラムのトップレベルではなく本体の先頭（すなわち `lambda`、
`let`、`let*`、`letrec`、`fluid-let`、または「手続き define」式の本体）に現れる定義
です。内部定義が定義する変数は本体に局所的です。すなわち、`variable` は代入ではなく
束縛され、束縛の領域は本体の全体です。たとえば、

```scheme
(let ((x 5))
  (define foo (lambda (y) (bar x y)))
  (define bar (lambda (a b) (+ (* a b) a)))
  (foo (+ x 3)))                                ⇒ 45
```

内部定義を含む本体は、つねに完全に等価な `letrec` 式に変換できます。たとえば、上の例
の `let` 式は次と等価です。

```scheme
(let ((x 5))
  (letrec ((foo (lambda (y) (bar x y)))
           (bar (lambda (a b) (+ (* a b) a))))
    (foo (+ x 3))))
```

## 2.5 代入

#### `set! variable [expression]` 〔特殊形式〕

`expression` が指定されていれば、それを評価し、その結果の値を `variable` が束縛されて
いる場所に格納します。`expression` が省かれていれば、`variable` は未代入に変えられ、
その後そのような変数を参照するのはエラーです。どちらの場合も、`set!` 式の値は未規定
です。

`variable` は、`set!` 式を囲む何らかの領域か、トップレベルで束縛されていなければなり
ません。ただし、`set!` フォームに入るときに `variable` が未代入であることは許され
ます。

```scheme
(define x 2)                                     ⇒ unspecified
(+ x 1)                                          ⇒ 3
(set! x 4)                                       ⇒ unspecified
(+ x 1)                                          ⇒ 5
```

`variable` は `access` 式でもよいです（第13章「環境」を見よ）。これにより、任意の環境
の変数に代入できます。たとえば、

```scheme
(define x (let ((y 0)) (the-environment)))
(define y 'a)
y                                                ⇒ a
(access y x)                                     ⇒ 0
(set! (access y x) 1)                            ⇒ unspecified
y                                                ⇒ a
(access y x)                                     ⇒ 1
```

## 2.6 クォート

この節では、オブジェクトの評価を変える、あるいは妨げるために使う式を説明します。

#### `quote datum` 〔特殊形式〕

`(quote datum)` は `datum` に評価されます。`datum` は Scheme オブジェクトの任意の
外部表現でよいです（1.2.6節「外部表現」を見よ）。リテラルの定数を Scheme コードに
含めるには `quote` を使います。

```scheme
(quote a)                                    ⇒ a
(quote #(a b c))                             ⇒ #(a b c)
(quote (+ 1 2))                              ⇒ (+ 1 2)
```

`(quote datum)` は `'datum` と略記できます。この2つの記法はあらゆる点で等価です。

```scheme
'a                                               ⇒ a
'#(a b c)                                         ⇒ #(a b c)
'(+ 1 2)                                          ⇒ (+ 1 2)
'(quote a)                                        ⇒ (quote a)
''a                                               ⇒ (quote a)
```

数の定数、文字列の定数、文字の定数、真偽値の定数はそれ自身に評価されるので、クォートを
必要としません。

```scheme
'"abc"                                            ⇒ "abc"
"abc"                                             ⇒ "abc"
'145932                                           ⇒ 145932
145932                                            ⇒ 145932
'#t                                               ⇒ #t
#t                                                ⇒ #t
'#\a                                              ⇒ #\a
#\a                                               ⇒ #\a
```

#### `quasiquote template` 〔特殊形式〕

「バッククォート」または「準クォート（quasiquote）」の式は、望むリストやベクタの構造
のほとんどは前もって分かっているが全部ではない、というときにその構造を組み立てるのに
役立ちます。`template` の中にコンマが現れなければ、`` `template `` を評価した結果は、
`'template` を評価した結果と（`equal?` の意味で）等価です。しかし `template` の中に
コンマが現れれば、コンマに続く式が評価され（「アンクォート」され）、その結果が、コンマ
とその式の代わりに構造に挿入されます。コンマの直後にアットマーク（`@`）が続けば、続く
式はリストに評価されなければならず、そのリストの開き括弧と閉じ括弧が「剥ぎ取られ」、
リストの要素が、そのコンマ・アットマーク式の並びの代わりに挿入されます。

```scheme
`(list ,(+ 1 2) 4)                                ⇒ (list 3 4)

(let ((name 'a)) `(list ,name ',name))            ⇒ (list a 'a)

`(a ,(+ 1 2) ,@(map abs '(4 -5 6)) b)             ⇒ (a 3 4 5 6 b)

`((foo ,(- 10 3)) ,@(cdr '(c)) . ,(car '(cons)))
                                         ⇒ ((foo 7) . cons)

`#(10 5 ,(sqrt 4) ,@(map sqrt '(16 9)) 8)
                                                  ⇒ #(10 5 2 4 3 8)

`,(+ 2 3)                                         ⇒ 5
```

準クォートのフォームは入れ子にできます。置き換えは、いちばん外側のバッククォートと
同じ入れ子のレベルに現れるアンクォートされた構成要素についてのみ行われます。入れ子の
レベルは、準クォートを1つ入れ子にするごとに1つ増え、アンクォートを1つ入れ子にする
ごとに1つ減ります。

```scheme
`(a `(b ,(+ 1 2) ,(foo ,(+ 1 3) d) e) f)
     ⇒ (a `(b ,(+ 1 2) ,(foo 4 d) e) f)

(let ((name1 'x)
        (name2 'y))
     `(a `(b ,,name1 ,',name2 d) e))
       ⇒ (a `(b ,x ,'y d) e)
```

記法 `` `template `` と `(quasiquote template)` は、あらゆる点で同じです。
`,expression` は `(unquote expression)` と同じで、`,@expression` は
`(unquote-splicing expression)` と同じです。

```scheme
(quasiquote (list (unquote (+ 1 2)) 4))
       ⇒ (list 3 4)

'(quasiquote (list (unquote (+ 1 2)) 4))
      ⇒ `(list ,(+ 1 2) 4)
      すなわち (quasiquote (list (unquote (+ 1 2)) 4))
```

シンボル `quasiquote`、`unquote`、`unquote-splicing` が、上で述べた以外の形で
`template` に現れると、予測できないふるまいになりえます。

## 2.7 条件式

条件式のふるまいは、オブジェクトが真か偽かによって決まります。条件式は `#f` だけを偽
として数えます。それ以外はすべて、`#t`、ペア、シンボル、数、文字列、ベクタ、手続きを
含めて、真として数えます（ただし1.2.5節「真と偽」を見よ）。

以下の説明では、条件式があるオブジェクトを真として扱うとき、そのオブジェクトが「真の値
を持つ」または「真である」といい、条件式があるオブジェクトを偽として扱うとき、その
オブジェクトが「偽の値を持つ」または「偽である」といいます。

#### `if predicate consequent [alternative]` 〔特殊形式〕

`predicate`、`consequent`、`alternative` は式です。`if` 式は次のように評価されます。
まず `predicate` が評価されます。それが真の値を返せば、`consequent` が評価され、その値
が返されます。そうでなければ `alternative` が評価され、その値が返されます。`predicate`
が偽の値を返し、`alternative` が指定されていなければ、式の結果は未規定です。

`if` 式は `consequent` か `alternative` のどちらか一方を評価し、両方を評価することは
決してありません。プログラムは、`alternative` のない `if` 式の値に依存すべきでは
ありません。

```scheme
(if (> 3 2) 'yes 'no)                              ⇒ yes
(if (> 2 3) 'yes 'no)                              ⇒ no
(if (> 3 2)
     (- 3 2)
     (+ 3 2))                                      ⇒ 1
```

#### `cond clause clause …` 〔特殊形式〕

各 `clause` は次の形をとります。

```scheme
(predicate expression ...)
```

ここで `predicate` は任意の式です。最後の `clause` は `else` 節でもよく、それは次の形
をとります。

```scheme
(else expression expression ...)
```

`cond` 式は次を行います。

1. 続く節の `predicate` 式を順に評価し、`predicate` の1つが真の値に評価されるまで続け
   ます。
2. `predicate` が真の値に評価されると、`cond` はその節の式を左から右へ評価し、節の
   最後の式を評価した結果を、`cond` 式全体の結果として返します。選ばれた節が
   `predicate` だけを含み式を含まなければ、`cond` は `predicate` の値を結果として返し
   ます。
3. すべての `predicate` が偽の値に評価され、`else` 節がなければ、条件式の結果は未規定
   です。`else` 節があれば、`cond` はその式を（左から右へ）評価し、最後のものの値を
   返します。

```scheme
(cond ((> 3 2) 'greater)
        ((< 3 2) 'less))                            ⇒ greater

(cond ((> 3 3) 'greater)
       ((< 3 3) 'less)
       (else 'equal))                            ⇒ equal
```

ふつう、プログラムは `else` 節のない `cond` 式の値に依存すべきではありません。しかし、
Scheme プログラマの中には、`predicate` の少なくとも1つがつねに真であるような `cond`
式を書くのを好む人もいます。この書き方では、最後の節が `else` 節と等価になります。

Scheme は別の節の構文をサポートします。

```scheme
(predicate => recipient)
```

ここで `recipient` は式です。`predicate` が真の値に評価されれば、`recipient` が評価
されます。その値は1引数の手続きでなければなりません。その手続きが `predicate` の値に
対して起動されます。

```scheme
(cond ((assv 'b '((a 1) (b 2))) => cadr)
       (else #f))                                ⇒ 2
```

#### `case key clause clause …` 〔特殊形式〕

`key` は任意の式でよいです。各 `clause` は次の形をとります。

```scheme
((object ...) expression expression ...)
```

`object` はどれも評価されず、すべての `object` は互いに異なっていなければなりません。
最後の `clause` は `else` 節でもよく、それは次の形をとります。

```scheme
(else expression expression ...)
```

`case` 式は次を行います。

1. `key` を評価し、その結果を各 `object` と比較します。
2. `key` を評価した結果がある `object` と（`eqv?` の意味で。第3章「同値述語」を見よ）
   等価なら、`case` は対応する節の式を左から右へ評価し、節の最後の式を評価した結果を、
   `case` 式の結果として返します。
3. `key` を評価した結果がどの `object` とも異なり、`else` 節があれば、`case` はその式
   を評価し、最後のものの結果を `case` 式の結果として返します。`else` 節がなければ、
   `case` は未規定の結果を返します。プログラムは、`else` 節のない `case` 式の値に依存
   すべきではありません。

たとえば、

```scheme
(case (* 2 3)
   ((2 3 5 7) 'prime)
   ((1 4 6 8 9) 'composite))                      ⇒ composite

(case (car '(c d))
   ((a) 'a)
   ((b) 'b))                                      ⇒ unspecified

(case (car '(c d))
   ((a e i o u) 'vowel)
   ((w y) 'semivowel)
   (else 'consonant))                             ⇒ consonant
```

#### `and expression …` 〔特殊形式〕

式が左から右へ評価され、偽の値に評価される最初の式の値が返されます。残りの式は評価
されません。すべての式が真の値に評価されれば、最後の式の値が返されます。式がなければ
`#t` が返されます。

```scheme
(and (= 2 2) (> 2 1))                              ⇒ #t
(and (= 2 2) (< 2 1))                              ⇒ #f
(and 1 2 'c '(f g))                                ⇒ (f g)
(and)                                              ⇒ #t
```

#### `or expression …` 〔特殊形式〕

式が左から右へ評価され、真の値に評価される最初の式の値が返されます。残りの式は評価
されません。すべての式が偽の値に評価されれば、最後の式の値が返されます。式がなければ
`#f` が返されます。

```scheme
(or (= 2 2) (> 2 1))                              ⇒ #t
(or (= 2 2) (< 2 1))                              ⇒ #t
(or #f #f #f)                                     ⇒ #f
(or (memq 'b '(a b c)) (/ 3 0))                   ⇒ (b c)
```

## 2.8 順次実行

`begin` 特殊形式は、式を特定の順序で評価するのに使います。

#### `begin expression expression …` 〔特殊形式〕

式が左から右へ順に評価され、最後の式の値が返されます。この種類の式は、入出力のような
副作用を順に並べるために使われます。

```scheme
(define x 0)
(begin (set! x 5)
         (+ x 1))                      ⇒ 6

(begin (display "4 plus 1 equals ")
        (display (+ 4 1)))
                                        -| 4 plus 1 equals 5
                                        ⇒ unspecified
```

`begin` を使う必要がないことはよくあります。多くの特殊形式がすでに式の並びをサポート
している（すなわち暗黙の `begin` を持つ）からです。そうした特殊形式には次があります。

```scheme
case
cond
define              ;「手続き define」のみ
do
fluid-let
lambda
let
let*
letrec
named-lambda
```

廃止された特殊形式 `sequence` は `begin` と同じです。新しいコードでは使うべきでは
ありません。

## 2.9 反復

反復の式は「名前付き let」と `do` です。これらは束縛の式でもありますが、より一般には
反復の式と呼ばれます。Scheme は適切に末尾再帰的なので、反復を表すのにこれらの特殊形式
を使う必要はありません。適切に書かれた「再帰的な」手続き呼び出しを使えば済みます。

#### `let name ((variable init) …) expression expression …` 〔特殊形式〕

MIT Scheme は、「名前付き let」と呼ばれる `let` の構文の変種を許します。これは `do`
より一般的なループ構文を提供し、再帰を表すのにも使えます。

名前付き let は、ふつうの `let` と同じ構文と意味論を持ちますが、`name` が式の中で、
仮引数が `variable` で本体が `expression` であるような手続きに束縛される点が異なり
ます。したがって、`name` が名指す手続きを起動することで、式の実行を繰り返せます。

MIT Scheme では、どの `init` も省略でき、その場合、対応する変数は未代入になります。

注意: 次の式は等価です。

```scheme
(let name ((variable init) ...)
  expression
  expression ...)

((letrec ((name
             (named-lambda (name variable ...)
               expression
               expression ...)))
    name)
 init ...)
```

例を挙げます。

```scheme
(let loop
      ((numbers '(3 -2 1 6 -5))
       (nonneg '())
       (neg '()))
   (cond ((null? numbers)
           (list nonneg neg))
         ((>= (car numbers) 0)
           (loop (cdr numbers)
                 (cons (car numbers) nonneg)
                 neg))
         (else
           (loop (cdr numbers)
                 nonneg
                 (cons (car numbers) neg)))))

       ⇒ ((6 1 3) (-5 -2))
```

#### `do ((variable init step) …) (test expression …) command …` 〔特殊形式〕

`do` は反復の構文です。束縛すべき変数の集合、それらを開始時にどう初期化するか、各反復
でどう更新するかを指定します。終了条件が満たされると、指定された結果の値でループを
抜けます。

`do` 式は次のように評価されます。`init` 式が（何らかの未規定の順序で）評価され、変数が
新しい場所に束縛され、`init` 式の結果が変数の束縛に格納され、それから反復のフェーズが
始まります。

各反復は `test` を評価することで始まります。結果が偽なら、`command` 式が順に効果のため
に評価され、`step` 式が何らかの未規定の順序で評価され、変数が新しい場所に束縛され、
`step` の結果が変数の束縛に格納され、次の反復が始まります。

`test` が真の値に評価されれば、`expression` が左から右へ評価され、最後の式の値が `do`
式の値として返されます。式がなければ、`do` 式の値は標準 Scheme では未規定です。MIT
Scheme では、`test` の値が返されます。

変数の束縛の領域は、`init` を除く `do` 式の全体からなります。変数が `do` 変数のリスト
に2回以上現れるのはエラーです。

`step` は省けます。その場合の効果は、`(variable init)` の代わりに `(variable init
variable)` と書いたのと同じです。

```scheme
(do ((vec (make-vector 5))
      (i 0 (+ i 1)))
    ((= i 5) vec)
   (vector-set! vec i i))                        ⇒ #(0 1 2 3 4)
(let ((x '(1 3 5 7 9)))
   (do ((x x (cdr x))
        (sum 0 (+ sum (car x))))
       ((null? x) sum)))                         ⇒ 25
```

## 2.10 構造体定義

この節では、`define-structure` の例を挙げ、そのオプションと構文を説明します。
`define-structure` は、Common Lisp の `defstruct` によく似た MIT Scheme のマクロです。
両者の違いはこの節の終わりにまとめます。より詳しくは Steele の Common Lisp の本を
見てください。

#### `define-structure (name structure-option …) slot-description …` 〔特殊形式＋〕

各 `slot-description` は次のいずれかの形をとります。

```scheme
slot-name
(slot-name default-init [slot-option value]*)
```

`name` と `slot-name` のフィールドはどちらもシンボルでなければなりません。`default-init`
のフィールドは、スロットの初期値のための式です。これは新しいインスタンスが構築される
たびに評価されます。指定されなければ、スロットの初期の内容は未定義です。

デフォルト値は、引数リスト付きの boa コンストラクタか、キーワードコンストラクタと
組み合わせたときにだけ役立ちます（後述）。

`define-structure` 式を評価すると、構造体記述子と、その構造体のインスタンスを操作する
一連の手続きが定義されます。これらのインスタンスは、既定ではレコードとして表現されます
が（10.4節「レコード」を見よ）、代わりにリストやベクタにもできます。アクセサと変更子
にはコンパイラ宣言の印が付くので、それらの呼び出しは適切な参照に自動的に変換されます。

多くの場合オプションは要らないので、`define-structure` の単純な呼び出しは次のように
なります。

```scheme
(define-structure foo a b c)
```

これは、型記述子 `foo`、コンストラクタ `make-foo`、述語 `foo?`、アクセサ `foo-a`・
`foo-b`・`foo-c`、変更子 `set-foo-a!`・`set-foo-b!`・`set-foo-c!` を定義します。

一般に、オプションが指定されなければ、`define-structure` は次を定義します（上の単純な
呼び出しを例に使います）。

**型記述子**
型記述子の名前は構造体の名前と同じ、たとえば `foo` です。型記述子は述語 `record-type?`
を満たします。

**コンストラクタ**
コンストラクタの名前は `"make-"` に構造体の名前を続けたもの、たとえば `make-foo` です。
コンストラクタが受け取る引数の数はスロットの数と同じです。引数はスロットの初期値であり、
引数の順序はスロット定義の順序に一致します。

**述語**
述語の名前は構造体の名前に `"?"` を続けたもの、たとえば `foo?` です。述語は1引数の
手続きで、引数がこの構造体定義で定義された型のレコードなら `#t` を、そうでなければ `#f`
を返します。

**アクセサ**
各スロットにアクセサが定義されます。アクセサの名前は、構造体の名前、ハイフン、スロット
の名前をつないで作られます。たとえば `foo-a` です。アクセサは1引数の手続きで、その引数
はこの構造体定義で定義された型のレコードでなければなりません。アクセサはそのレコードの
対応するスロットの内容を取り出して返します。

**変更子**
各スロットに変更子が定義されます。変更子の名前は、`"set-"`、アクセサの名前、`"!"` を
つないで作られます。たとえば `set-foo-a!` です。変更子は2引数の手続きで、1つ目はこの
構造体定義で定義された型のレコードでなければならず、2つ目は任意のオブジェクトでよいです。
変更子はそのレコードの対応するスロットの内容をそのオブジェクトに変更し、未規定の値を
返します。

オプションが与えられないとき、`(name)` は `name` に略記できます。この慣習は
`structure-option` と `slot-option` にも等しく当てはまります。したがって、次は等価
です。

```scheme
(define-structure foo a b c)
(define-structure (foo) (a) b (c))
```

また次も等価です。

```scheme
(define-structure (foo keyword-constructor) a b c)
(define-structure (foo (keyword-constructor)) a b c)
```

オプションの値として指定されたとき、`false` と `nil` は `#f` と等価であり、`true` と
`t` は `#t` と等価です。

指定できる `slot-option` は次のとおりです。

#### `read-only value` 〔スロットオプション〕

`#f` 以外の値が与えられると、このスロットに変更子を作らないことを指定します。

#### `type type-descriptor` 〔スロットオプション〕

これは受け付けられますが、現在は使われていません。

指定できる `structure-option` は次のとおりです。

#### `predicate [name]` 〔構造体オプション〕

このオプションは、構造体の述語手続きの定義を制御します。`name` が与えられなければ、
述語は既定の名前で定義されます（上記参照）。`name` が `#f` なら、述語はまったく定義
されません。そうでなければ、`name` はシンボルでなければならず、述語はそのシンボルを
名前として定義されます。

#### `copier [name]` 〔構造体オプション〕

このオプションは、構造体のインスタンスを複製する手続きの定義を制御します。これは1引数
（構造体のインスタンス）の手続きで、その構造体の新しく割り当てられた複製を作って返し
ます。`name` が与えられなければ、複製子が定義され、その名前は `"copy-"` に構造体名を
続けたもの（たとえば `copy-foo`）です。`name` が `#f` なら、複製子は定義されません。
そうでなければ、`name` はシンボルでなければならず、複製子はそのシンボルを名前として
定義されます。

#### `print-procedure expression` 〔構造体オプション〕

`expression` を評価すると、構造体のインスタンスを表示するのに使う2引数の手続きが得られ
なければなりません。この手続きは非構文解析器メソッド（unparser method）です（14.7節
「カスタム出力」を見よ）。構造体のインスタンスがレコードなら、このオプションは
`set-record-type-unparser-method!` を呼ぶのと同じ効果を持ちます。

#### `constructor [name [argument-list]]` 〔構造体オプション〕

このオプションは、コンストラクタ手続きの定義を制御します。これらのコンストラクタ手続き
は「boa コンストラクタ」と呼ばれます。「By Order of Arguments（引数の順序による）」の
略で、コンストラクタへの引数が、与えられた順序によって構造体のスロットの初期の内容を
指定するからです。これは、初期の内容をキーワードで指定し、引数の順序が関係ない
「キーワードコンストラクタ」に対するものです。

`name` が与えられなければ、コンストラクタは既定の名前と引数で定義されます（上記参照）。
`name` が `#f` なら、コンストラクタは定義されません。この場合 `argument-list` は指定
できません。そうでなければ、`name` はシンボルでなければならず、コンストラクタはその
シンボルを名前として定義されます。`name` がシンボルなら、`argument-list` は任意で
許されます。省かれると、コンストラクタは構造体定義の各スロットに対して1つの引数を、
スロットが定義に現れるのと同じ順序で受け取ります。そうでなければ、`argument-list` は
ラムダリスト（2.1節「Lambda 式」を見よ）でなければならず、ラムダリストの各引数は構造体
のスロットの名前でなければなりません。コンストラクタが受け取る引数はこのラムダリスト
で定義されます。ラムダリストで指定されないスロットは、上で指定した `default-init` に
初期化されます。省略可能引数として指定されたスロットで、対応する引数が与えられない
ときも同様です。

`constructor` オプションが指定されると、既定のコンストラクタは定義されません。加えて、
`constructor` オプションは複数回指定して、異なる名前と引数リストを持つ複数のコンストラ
クタを定義できます。

```scheme
(define-structure (foo
                       (constructor make-foo (#!optional a b)))
  (a 6 read-only #t)
  (b 9))
```

#### `keyword-constructor [name]` 〔構造体オプション〕

このオプションは、キーワードコンストラクタ手続きの定義を制御します。キーワードコンスト
ラクタは、スロット名と値を交互に並べた引数を受け取る手続きです。`name` が省かれると、
キーワードコンストラクタが定義され、その名前は `"make-"` に構造体の名前を続けたもの
（たとえば `make-foo`）です。そうでなければ、`name` はシンボルでなければならず、
キーワードコンストラクタはこのシンボルを名前として定義されます。

`keyword-constructor` オプションが指定されると、既定のコンストラクタは定義されません。
加えて、`keyword-constructor` オプションは複数回指定して複数のキーワードコンストラクタ
を定義できます。そのようなコンストラクタはすべて等価になるので、ふつうはしません。

```scheme
(define-structure (foo (keyword-constructor make-bar)) a b)
(foo-a (make-bar 'b 20 'a 19))                 ⇒ 19
```

#### `type-descriptor name` 〔構造体オプション〕

このオプションは `type` オプションや `named` オプションと一緒には使えません。

既定では、構造体はレコードとして実装されます。構造体の名前は、その構造体が定義する
レコードの型記述子を保持するよう定義されます。`type-descriptor` オプションは、型記述子
を保持する別の名前を指定します。

```scheme
(define-structure foo a b)
foo                 ⇒ #[record-type 18]

(define-structure (bar (type-descriptor bar-rtd)) a b)
bar              error> Unbound variable: bar
bar-rtd         ⇒ #[record-type 19]
```

#### `conc-name [name]` 〔構造体オプション〕

既定では、アクセサと変更子の名前を付ける接頭辞は、構造体の名前にハイフンを続けたもの
です。`conc-name` オプションで別のものを指定できます。`name` が与えられなければ、接頭辞
は構造体の名前にハイフンを続けたもの（既定）です。`name` が `#f` なら、スロット名が
接頭辞なしで直接使われます。そうでなければ、`name` はシンボルでなければならず、その
シンボルが接頭辞として使われます。

```scheme
(define-structure (foo (conc-name moby/)) a b)
```

はアクセサ `moby/a` と `moby/b`、変更子 `set-moby/a!` と `set-moby/b!` を定義します。

```scheme
(define-structure (foo (conc-name #f)) a b)
```

はアクセサ `a` と `b`、変更子 `set-a!` と `set-b!` を定義します。

#### `type representation-type` 〔構造体オプション〕

このオプションは `type-descriptor` オプションと一緒には使えません。

既定では、構造体はレコードとして実装されます。`type` オプションはこの既定を上書きし、
構造体を別のデータ型を使って実装するようプログラマが指定できるようにします。オプション
の値 `representation-type` が代わりのデータ型を指定します。これはシンボル `vector` か
`list` のどちらかでよく、使われるデータ型はそのシンボルに対応するものです。

```scheme
(define-structure (foo (type list)) a b)
(make-foo 1 2)                                  ⇒ (1 2)
```

#### `named [expression]` 〔構造体オプション〕

これは `type` オプションと組み合わせたときにのみ有効で、構造体のインスタンスに、この
構造体型のインスタンスと識別できるよう印を付けることを指定します。このオプションは
`type-descriptor` オプションと一緒には使えません。

`expression` が与えられないふつうの場合、`named` オプションは、構造体に型記述子と述語
を定義させ（`named` のない `type` オプションはそれらの定義を抑制することを思い出して
ください）、さらに構造体のインスタンスに既定の非構文解析器メソッドを定義します
（`print-procedure` オプションで上書きできます）。既定の非構文解析器メソッドが欲しく
なければ、`print-procedure` オプションを `#F` として指定すべきです。すると構造体は、
型記述子を含むそのままの表現、すなわちリストやベクタとして表示されます。型記述子は、
レコード型ではない一意なオブジェクトで、構造体のインスタンスを記述し、さらにそれらを
識別するために構造体のインスタンスに格納されます。表現の型が `vector` なら、型記述子は
ベクタの0番目のスロットに格納され、表現の型が `list` なら、リストの最初の要素として
格納されます。

```scheme
(define-structure (foo (type vector) named) a b c)
(vector-ref (make-foo 1 2 3) 0) ⇒ #[structure-type 52]
```

`expression` が指定されると、それはタグオブジェクトを得るために評価される式です。この
式は、構造体定義が評価されるときに（非構文解析器メソッドを指定するために）1回評価され、
述語やコンストラクタが呼ばれるたびにもう一度評価されます。このため、`expression` は
ふつう変数参照か定数です。`expression` が返す値は、どんなオブジェクトでもよいです。
そのオブジェクトは、上で述べたように、ふつう型記述子が格納されるのと同じ場所に、構造体
のインスタンスに格納されます。`expression` が指定されると、型記述子は定義されず、述語
だけが定義されます。

```scheme
(define-structure (foo (type vector) (named 'foo)) a b c)
(vector-ref (make-foo 1 2 3) 0) ⇒ foo
```

#### `safe-accessors [boolean]` 〔構造体オプション〕

このオプションは、`define-structure` が生成するスロットのアクセサ（と変更子）の安全性
を、プログラマがある程度制御できるようにします。`safe-accessors` が指定されないか、
`boolean` が `#f` なら、アクセサは安全性を犠牲にして速度に最適化されます。コンパイル
されると、アクセサはとても速いインラインの並び、ふつう1〜3個の機械命令の長さになります。
しかし、`safe-accessors` が指定され、`boolean` が省かれるか `#t` なら、アクセサは安全性
に最適化され、引数の型と構造を調べ、まとめてコード化されます。

```scheme
(define-structure (foo safe-accessors) a b c)
```

#### `initial-offset offset` 〔構造体オプション〕

これは `type` オプションと組み合わせたときにのみ有効です。`offset` は正確な非負整数で
なければならず、指定されたスロットが割り当てられる前に、構造体のインスタンスの先頭に
空けておくスロットの数を指定します。オフセットを0に指定するのは、`initial-offset`
オプションを省くのと等価です。

`named` オプションが指定されていれば、構造体のタグが最初のスロットに現れ、続いて
「オフセット」のスロット、それから通常のスロットが来ます。そうでなければ、「オフセット」
のスロットが最初に来て、続いて通常のスロットが来ます。

```scheme
(define-structure (foo (type vector) (initial-offset 3))
   a b c)
(make-foo 1 2 3)                      ⇒ #(() () () 1 2 3)
```

MIT Scheme の `define-structure` と Common Lisp の `defstruct` の本質的な違いは、次の
とおりです。

- 既定のコンストラクタ手続きは、構造体の定義で指定されたのと同じ順序で、位置引数を
  取ります。キーワードコンストラクタは、オプション `keyword-constructor` を与えて指定
  できます。
- boa コンストラクタは Scheme のラムダリストで記述されます。Scheme のラムダリストには
  `&aux` に対応するものがないので、この機能は実装されていません。
- 既定では、複製子手続きは定義されません。
- アクセサ `foo` に対応する副作用の手続きには、`set-foo!` という名前が与えられます。
- キーワードはふつうのシンボルです。`:foo` の代わりに `foo` を使います。
- オプションの値 `false`、`nil`、`true`、`t` は、代わりに適切な真偽値の定数が指定された
  かのように扱われます。
- `print-function` オプションは `print-procedure` という名前です。その引数は、Common
  Lisp のように3つではなく、2引数（非構文解析器の状態と構造体のインスタンス）の手続き
  です。
- 既定では、名前付きの構造体は、何らかの一意なオブジェクトで印を付けられます。Common
  Lisp では、構造体はシンボルで印を付けられます。これは一意なタグを生成するのに Common
  Lisp のパッケージシステムに頼ります。MIT Scheme には、そのような一意なシンボルを
  生成する方法がありません。
- `named` オプションは任意で引数を取れます。それはふつう変数の名前です（任意の式が
  使えますが、タグの名前が必要になるたびに評価されます）。使われると、構造体のインスタンス
  はその変数の値で印を付けられます。その変数は `define-structure` が評価されるときに
  定義されていなければなりません。
- `type` オプションは値 `vector` と `list` に限られます。
- `include` オプションは実装されていません。
