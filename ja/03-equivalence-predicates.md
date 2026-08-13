<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 3 同値述語

**述語（predicate）**とは、つねに真偽値（`#t` または `#f`）を返す手続きです。**同値
述語（equivalence predicate）**とは、数学の同値関係の計算上の対応物です（対称的、
反射的、推移的です）。この節で説明する同値述語のうち、`eq?` がもっとも細かい（もっとも
弁別する）もので、`equal?` がもっとも粗いものです。`eqv?` は `eq?` よりわずかに弁別
しません。

#### `eqv? obj1 obj2` 〔手続き〕

`eqv?` 手続きは、オブジェクトに対する有用な同値関係を定めます。手短に言えば、`obj1` と
`obj2` がふつう同じオブジェクトとみなされるべきなら `#t` を返します。

`eqv?` 手続きは、次の場合に `#t` を返します。

- `obj1` と `obj2` がともに `#t` であるか、ともに `#f` である。
- `obj1` と `obj2` がともにインターンされたシンボルであり、次が成り立つ。

  ```scheme
  (string=? (symbol->string obj1)
              (symbol->string obj2))
        ⇒ #t
  ```

- `obj1` と `obj2` がともに数であり、`=` 手続きによって数値的に等しく、ともに正確で
  あるかともに不正確である（第4章「数」を見よ）。
- `obj1` と `obj2` がともに文字であり、`char=?` 手続きによって同じ文字である（第5章
  「文字」を見よ）。
- `obj1` と `obj2` がともに空リストである。
- `obj1` と `obj2` が、場所タグの等しい手続きである。
- `obj1` と `obj2` が、記憶域の同じ場所を表すペア・ベクタ・文字列・ビット列・レコード・
  セル・弱いペアである。

`eqv?` 手続きは、次の場合に `#f` を返します。

- `obj1` と `obj2` が異なる型である。
- `obj1` と `obj2` の一方が `#t` で他方が `#f` である。
- `obj1` と `obj2` がシンボルだが、次が成り立つ。

  ```scheme
  (string=? (symbol->string obj1)
              (symbol->string obj2))
        ⇒ #f
  ```

- `obj1` と `obj2` の一方が正確な数で他方が不正確な数である。
- `obj1` と `obj2` が、`=` 手続きが `#f` を返す数である。
- `obj1` と `obj2` が、`char=?` 手続きが `#f` を返す文字である。
- `obj1` と `obj2` の一方が空リストで他方がそうでない。
- `obj1` と `obj2` が、ある引数に対して異なるふるまいをする（異なる値を返すか、異なる
  副作用を持つ）手続きである。
- `obj1` と `obj2` が、互いに異なる場所を表すペア・ベクタ・文字列・ビット列・レコード・
  セル・弱いペアである。

例をいくつか挙げます。

```scheme
(eqv? 'a 'a)                            ⇒ #t
(eqv? 'a 'b)                            ⇒ #f
(eqv? 2 2)                              ⇒ #t
(eqv? '() '())                          ⇒ #t
(eqv? 100000000 100000000)              ⇒ #t
(eqv? (cons 1 2) (cons 1 2))            ⇒ #f
(eqv? (lambda () 1)
      (lambda () 2))                    ⇒ #f
(eqv? #f 'nil)                          ⇒ #f
(let ((p (lambda (x) x)))
  (eqv? p p))                           ⇒ #t
```

次の例は、上の規則が `eqv?` のふるまいを完全には規定しない場合を示します。そのような
場合について言えるのは、`eqv?` が返す値が真偽値でなければならない、ということだけです。

```scheme
(eqv? "" "")                            ⇒ unspecified
(eqv? '#() '#())                        ⇒ unspecified
(eqv? (lambda (x) x)
      (lambda (x) x))                   ⇒ unspecified
(eqv? (lambda (x) x)
      (lambda (y) y))                   ⇒ unspecified
```

次の一連の例は、局所的な状態を持つ手続きに対する `eqv?` の使い方を示します。
`gen-counter` は毎回異なる手続きを返さなければなりません。各手続きが独自の内部
カウンタを持つからです。一方 `gen-loser` は毎回等価な手続きを返します。局所的な状態が
手続きの値や副作用に影響しないからです。

```scheme
(define gen-counter
  (lambda ()
    (let ((n 0))
      (lambda () (set! n (+ n 1)) n))))
(let ((g (gen-counter)))
  (eqv? g g))                   ⇒ #t
(eqv? (gen-counter) (gen-counter))
                                ⇒ #f
(define gen-loser
  (lambda ()
    (let ((n 0))
      (lambda () (set! n (+ n 1)) 27))))
(let ((g (gen-loser)))
  (eqv? g g))                   ⇒ #t
(eqv? (gen-loser) (gen-loser))
                                ⇒ unspecified

(letrec ((f (lambda () (if (eqv? f g) 'both 'f)))
         (g (lambda () (if (eqv? f g) 'both 'g)))
  (eqv? f g))
                                ⇒ unspecified

(letrec ((f (lambda () (if (eqv? f g) 'f 'both)))
            (g (lambda () (if (eqv? f g) 'g 'both)))
   (eqv? f g))
                                        ⇒ #f
```

異なる型のオブジェクトが、同じオブジェクトとみなされることは決してあってはなりません。

定数オブジェクト（リテラルの式が返すもの）を書き換えるのはエラーなので、実装は適切な
ところで定数どうしの構造を共有してよいです。したがって、定数に対する `eqv?` の値は
未規定のことがあります。

```scheme
(let ((x '(a)))
   (eqv? x x))                          ⇒ #t
(eqv? '(a) '(a))                        ⇒ unspecified
(eqv? "a" "a")                          ⇒ unspecified
(eqv? '(b) (cdr '(a b)))                ⇒ unspecified
```

論拠: 上の `eqv?` の定義は、手続きとリテラルの扱いについて実装に自由を許します。実装
は、2つの手続きや2つのリテラルが互いに等価であることを、検出しても検出しなくてもよく、
また、両方を表すのに同じポインタやビットパターンを使って、等価なオブジェクトの表現を
まとめるかどうかを決められます。

#### `eq? obj1 obj2` 〔手続き〕

`eq?` は `eqv?` に似ていますが、場合によっては `eqv?` が検出できるより細かい区別を
見分けられる点が異なります。

`eq?` と `eqv?` は、シンボル・真偽値・空リスト・ペア・レコード・空でない文字列と
ベクタに対して、同じふるまいをすることが保証されています。数と文字に対する `eq?` の
ふるまいは実装依存ですが、つねに真か偽を返し、`eqv?` も真を返すときにのみ真を返します。
`eq?` は、空のベクタや空の文字列に対して `eqv?` と異なるふるまいをすることもあります。

```scheme
(eq? 'a 'a)                            ⇒ #t
(eq? '(a) '(a))                        ⇒ unspecified
(eq? (list 'a) (list 'a))              ⇒ #f
(eq? "a" "a")                          ⇒ unspecified
(eq? "" "")                            ⇒ unspecified
(eq? '() '())                          ⇒ #t
(eq? 2 2)                              ⇒ unspecified
(eq? #\A #\A)                          ⇒ unspecified
(eq? car car)                          ⇒ #t
(let ((n (+ 2 3)))
  (eq? n n))                           ⇒ unspecified
(let ((x '(a)))
  (eq? x x))                           ⇒ #t
(let ((x '#()))
  (eq? x x))                           ⇒ #t
(let ((p (lambda (x) x)))
  (eq? p p))                           ⇒ #t
```

論拠: ふつう `eq?` は `eqv?` よりずっと効率よく、たとえば何かもっと込み入った演算では
なく単純なポインタ比較として実装できます。1つの理由は、2つの数の `eqv?` を定数時間で
計算できるとはかぎらないのに対し、ポインタ比較として実装された `eq?` はつねに定数時間
で終わることです。`eq?` は `eqv?` と同じ制約に従うので、状態を持つオブジェクトを実装
するのに手続きを使うアプリケーションでは、`eqv?` のように使えます。

#### `equal? obj1 obj2` 〔手続き〕

`equal?` は、ペア・ベクタ・文字列の内容を再帰的に比較し、数・シンボル・レコードなどの
ほかのオブジェクトには `eqv?` を適用します。経験則として、オブジェクトは、同じように
表示されればふつう `equal?` です。引数が循環データ構造なら、`equal?` は終わらないこと
があります。

```scheme
(equal? 'a 'a)                         ⇒ #t
(equal? '(a) '(a))                     ⇒ #t
(equal? '(a (b) c)
        '(a (b) c))                    ⇒ #t
(equal? "abc" "abc")                   ⇒ #t
(equal? 2 2)                           ⇒ #t
(equal? (make-vector 5 'a)
        (make-vector 5 'a))            ⇒ #t
(equal? (lambda (x) x)
        (lambda (y) y))                ⇒ unspecified
```
