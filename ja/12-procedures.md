<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 12 手続き

手続きは lambda 式を評価して作られます（2.1節「Lambda 式」を見よ）。lambda は明示的でも、
「手続き define」のように暗黙でもよいです（2.4節「定義」を見よ）。また、`car` のような、
**基本手続き（primitive procedure）**と呼ばれる特別な組み込みの手続きもあります。これら
の手続きは Scheme ではなく、Scheme システムを実装するのに使われた言語で書かれています。
MIT Scheme はさらに、手続きのようにふるまうデータ構造の構築をサポートする**適用フック
（application hook）**を提供します。

MIT Scheme では、手続きの表示表現が手続きの種類（コンパイル済み、解釈実行、基本）を
教えます。

```scheme
pp
     ⇒ #[compiled-procedure 56 ("pp" #x2) #x10 #x307578]
(lambda (x) x)
     ⇒ #[compound-procedure 57]
(define (foo x) x)
foo
     ⇒ #[compound-procedure 58 foo]
car
     ⇒ #[primitive-procedure car]
(call-with-current-continuation (lambda (x) x))
     ⇒ #[continuation 59]
```

解釈実行の手続きは「複合（compound）」手続きと呼ばれることに注意してください（厳密には、
コンパイル済みの手続きも複合手続きです）。表示表現は歴史的な理由からこの区別をしており、
いずれ変わるかもしれません。

## 12.1 手続きの演算

#### `apply procedure object object …` 〔手続き〕

次のリストの要素を引数として `procedure` を呼びます。

```scheme
(cons* object object ...)
```

最初のほうの `object` は任意のオブジェクトでよいですが、最後の `object`（少なくとも1つの
`object` がなければなりません）はリストでなければなりません。

```scheme
(apply + (list 3 4 5 6))                         ⇒ 18
(apply + 3 4 '(5 6))                             ⇒ 18

(define compose
  (lambda (f g)
    (lambda args
      (f (apply g args)))))
((compose sqrt *) 12 75)                         ⇒ 30
```

#### `procedure? object` 〔手続き＋〕

`object` が手続きなら `#t` を、そうでなければ `#f` を返します。`#t` が返されれば、次の
述語のちょうど1つが `object` によって満たされます。`compiled-procedure?`、
`compound-procedure?`、`primitive-procedure?` です。

#### `compiled-procedure? object` 〔手続き＋〕

`object` がコンパイル済みの手続きなら `#t` を、そうでなければ `#f` を返します。

#### `compound-procedure? object` 〔手続き＋〕

`object` が複合（すなわち解釈実行の）手続きなら `#t` を、そうでなければ `#f` を返します。

#### `primitive-procedure? object` 〔手続き＋〕

`object` が基本手続きなら `#t` を、そうでなければ `#f` を返します。

次の2つの手続きは、手続きの引数の個数（arity）、すなわち手続きが受け取る引数の数を調べ
ます。この検査の結果は、手続きを呼んだときの効果より制限が緩いことがあります。言い換える
と、これらの手続きは、手続きが与えられた数の引数を受け取ると示すかもしれませんが、手続き
を呼ぶと `condition-type:wrong-number-of-arguments` エラーを通知するかもしれません。
これは、これらの手続きが手続きの見かけの引数の個数を調べるからです。たとえば、次は任意
の数の引数を受け取るように見えますが、呼ばれると引数の数が1でなければエラーを通知する
手続きです。

```scheme
(lambda arguments (apply car arguments))
```

#### `procedure-arity-valid? procedure k` 〔手続き＋〕

`procedure` が `k` 個の引数を受け取るなら `#t` を、そうでなければ `#f` を返します。

#### `procedure-arity procedure` 〔手続き＋〕

`procedure` が受け取る引数の数の記述を返します。結果は新しく割り当てられたペアで、car
フィールドが引数の最小数、cdr フィールドが引数の最大数です。最小は正確な非負整数です。
最大は、正確な非負整数か、手続きに引数の最大数がないことを意味する `#f` のどちらかです。

```scheme
(procedure-arity (lambda () 3))                 ⇒ (0 . 0)
(procedure-arity (lambda (x) x))                ⇒ (1 . 1)
(procedure-arity car)                           ⇒ (1 . 1)
(procedure-arity (lambda x x))                  ⇒ (0 . #f)
(procedure-arity (lambda (x . y) x))            ⇒ (1 . #f)
(procedure-arity (lambda (x #!optional y) x))
                                                ⇒ (1 . 2)
```

#### `procedure-environment procedure` 〔手続き＋〕

`procedure` の閉包環境を返します。`procedure` が基本手続きの場合、または `procedure` が
デバッグ情報を得られないコンパイル済みの手続きの場合、エラーを通知します。

## 12.2 基本手続き

#### `make-primitive-procedure name [arity]` 〔手続き＋〕

`name` はシンボルでなければなりません。`arity` は正確な非負整数、`-1`、`#f`、`#t` のいず
れかでなければなりません。与えられなければ既定で `#f` です。`name` という名前の基本手続き
を返します。`arity` に応じてさらに動作するかもしれません。

**`#f`**
基本手続きが実装されていなければ、エラーを通知します。

**`#t`**
基本手続きが実装されていなければ、`#f` を返します。

**整数**
基本手続きが実装されていれば、その引数の個数が `arity` と等しくなければエラーを通知します。
基本手続きが実装されていなければ、`arity` 個の引数を受け取る、実装されていない基本手続き
オブジェクトを返します。`arity` が `-1` なら任意の数の引数を受け取ることを意味します。

#### `primitive-procedure-name primitive-procedure` 〔手続き＋〕

`primitive-procedure` の名前、すなわちシンボルを返します。

```scheme
(primitive-procedure-name car)                ⇒ car
```

#### `implemented-primitive-procedure? primitive-procedure` 〔手続き＋〕

`primitive-procedure` が実装されていれば `#t` を、そうでなければ `#f` を返します。特定
の基本手続きを実装するコードが、実行可能な Scheme プログラムに必ずしもリンクされていない
ので、役立ちます。

## 12.3 継続

#### `call-with-current-continuation procedure` 〔手続き〕

`procedure` は1引数の手続きでなければなりません。現在の継続（下記）を脱出手続き（escape
procedure）として包み、`procedure` に引数として渡します。脱出手続きは1引数の Scheme の
手続きで、あとで値を渡されると、その後の時点で有効な継続が何であれ無視し、かわりにその
値を、脱出手続きが作られたときに有効だった継続に渡します。`call-with-current-continuation`
が作る脱出手続きは、Scheme の他のどの手続きとも同じく無制限の存続期間を持ちます。変数や
データ構造に格納でき、望むだけ何度でも呼べます。

次の例は、この手続きのもっともよくある使い方だけを示します。すべての実際のプログラムが
これらの例ほど単純なら、`call-with-current-continuation` ほどの力を持つ手続きは必要
ないでしょう。

```scheme
(call-with-current-continuation
   (lambda (exit)
     (for-each (lambda (x)
                    (if (negative? x)
                         (exit x)))
                 '(54 0 37 -3 245 19))
     #t))                                         ⇒ -3

(define list-length
   (lambda (obj)
     (call-with-current-continuation
        (lambda (return)
          (letrec ((r
                        (lambda (obj)
                          (cond ((null? obj) 0)
                                  ((pair? obj) (+ (r (cdr obj)) 1))
                                  (else (return #f))))))
             (r obj))))))
(list-length '(1 2 3 4))                           ⇒ 4
(list-length '(a b . c))                           ⇒ #f
```

`call-with-current-continuation` のよくある使い方は、ループや手続きの本体からの
構造化された非局所脱出ですが、実は `call-with-current-continuation` は、幅広い高度な
制御構造を実装するのにも非常に役立ちます。

Scheme の式が評価されるときはいつでも、その式の結果を求める継続が存在します。継続は、
計算の（既定の）未来全体を表します。たとえば式がトップレベルで評価されるなら、継続は
結果を取り、画面に表示し、次の入力を促し、それを評価し、と永遠に続けます。たいてい継続
は、結果を取り、局所変数に格納された値と掛け、7 を足し、その答えを表示するためにトップ
レベルの継続に渡す継続のように、ユーザのコードが指定する動作を含みます。ふつう、これらの
遍在する継続は舞台裏に隠れており、プログラマはそれらについてあまり考えません。継続を
明示的に扱う必要がまれに生じたとき、`call-with-current-continuation` は、現在の継続
とちょうど同じようにふるまう手続きを作ることで、それをできるようにします。

#### `continuation? object` 〔手続き＋〕

`object` が継続なら `#t` を、そうでなければ `#f` を返します。

#### `within-continuation continuation thunk` 〔手続き＋〕

`thunk` は引数のない手続きでなければなりません。概念的には、`within-continuation` は
`thunk` を起動した結果に対して `continuation` を起動しますが、`thunk` は `continuation`
の動的文脈で実行されます。言い換えると、「現在の」継続は `thunk` が起動される前に捨てられ
ます。

#### `dynamic-wind before thunk after` 〔手続き＋〕

`thunk` を引数なしで呼び、この呼び出しの結果を返します。`before` と `after` も引数なしで、
次の規則が求めるとおりに呼ばれます（`call-with-current-continuation` で捕らえた継続の
呼び出しがなければ、3つの引数はそれぞれ順に1回ずつ呼ばれることに注意してください）。
`before` は、実行が `thunk` の呼び出しの動的存続期間に入るたびに呼ばれ、`after` はその
動的存続期間を出るたびに呼ばれます。手続き呼び出しの動的存続期間は、呼び出しが始められて
から返るまでの期間です。Scheme では、`call-with-current-continuation` のために、呼び出し
の動的存続期間は単一の連続した時間の区間でないかもしれません。次のように定義されます。

- 動的存続期間には、呼ばれた手続きの本体の実行が始まるときに入ります。
- 動的存続期間には、実行が動的存続期間内でなく、動的存続期間のあいだに
  （`call-with-current-continuation` で）捕らえた継続が起動されたときにも入ります。
- 呼ばれた手続きが返るときに出ます。
- 実行が動的存続期間内で、動的存続期間内でないときに捕らえた継続が起動されたときにも
  出ます。

`thunk` の呼び出しの動的存続期間内で `dynamic-wind` への2度目の呼び出しが起こり、次に、
これら2つの `dynamic-wind` の起動の `after` が両方とも呼ばれるような形で継続が起動され
ると、2度目の（内側の）`dynamic-wind` の呼び出しに結びついた `after` が先に呼ばれます。

`thunk` の呼び出しの動的存続期間内で `dynamic-wind` への2度目の呼び出しが起こり、次に、
これら2つの `dynamic-wind` の起動の `before` が両方とも呼ばれるような形で継続が起動され
ると、1度目の（外側の）`dynamic-wind` の呼び出しに結びついた `before` が先に呼ばれます。

継続の起動が、ある `dynamic-wind` の呼び出しの `before` と別の `dynamic-wind` の呼び出し
の `after` を呼ぶことを要求するなら、`after` が先に呼ばれます。

捕らえた継続を使って、`before` や `after` の呼び出しの動的存続期間に入ったり出たりする
ことの効果は未定義です。

```scheme
(let ((path '())
       (c #f))
  (let ((add (lambda (s)
                   (set! path (cons s path)))))
     (dynamic-wind
       (lambda () (add 'connect))
       (lambda ()
          (add (call-with-current-continuation
                   (lambda (c0)
                      (set! c c0)
                      'talk1))))
       (lambda () (add 'disconnect)))
     (if (< (length path) 4)
          (c 'talk2)
          (reverse path))))

⇒ (connect talk1 disconnect connect talk2 disconnect)
```

次の2つの手続きは多値をサポートします。

#### `call-with-values thunk procedure` 〔手続き＋〕

`thunk` は引数のない手続きでなければならず、`procedure` は手続きでなければなりません。
`thunk` は、多値を受け取ることを期待する継続とともに起動されます。具体的には、その継続
は、`procedure` が引数として受け取るのと同じ数の値を受け取ることを期待します。`thunk` は
`values` 手続きを使って多値を返さなければなりません。そして `procedure` がその多値を引数
として呼ばれます。`procedure` が生む結果が `call-with-values` の結果として返されます。

#### `values object …` 〔手続き＋〕

多値を返します。この手続きが呼ばれたときに有効な継続は、`call-with-values` が作った多値
継続でなければなりません。さらに、`object` の数だけの値を受け取らなければなりません。

## 12.4 適用フック

**適用フック（application hook）**は、手続きのように適用できるオブジェクトです。各適用
フックは2つの部分を持ちます。適用フックが適用されたときに何をするかを指定する手続きと、
`extra` と呼ばれる任意のオブジェクトです。しばしば手続きは `extra` オブジェクトを使って
何をするかを決めます。

適用フックには2種類あり、手続きに渡される引数が異なります。**apply フック**が適用される
と、手続きには apply フックに渡されたのとまったく同じ引数が渡されます。**エンティティ
（entity）**が適用されると、エンティティ自身が最初の引数として渡され、続いてエンティティ
に渡された他の引数が渡されます。

apply フックとエンティティはどちらも述語 `procedure?` を満たします。それぞれ、その手続き
成分に応じて `compiled-procedure?`、`compound-procedure?`、`primitive-procedure?` の
いずれかを満たします。apply フックはその手続きと同じ数の引数を受け取るとみなされ、
エンティティはその手続きより1つ少ない引数を受け取るとみなされます。

#### `make-apply-hook procedure object` 〔手続き＋〕

手続き成分が `procedure` で `extra` 成分が `object` である、新しく割り当てられた apply
フックを返します。

#### `apply-hook? object` 〔手続き＋〕

`object` が apply フックなら `#t` を、そうでなければ `#f` を返します。

#### `apply-hook-procedure apply-hook` 〔手続き＋〕

`apply-hook` の手続き成分を返します。

#### `set-apply-hook-procedure! apply-hook procedure` 〔手続き＋〕

`apply-hook` の手続き成分を `procedure` に変えます。未規定の値を返します。

#### `apply-hook-extra apply-hook` 〔手続き＋〕

`apply-hook` の `extra` 成分を返します。

#### `set-apply-hook-extra! apply-hook object` 〔手続き＋〕

`apply-hook` の `extra` 成分を `object` に変えます。未規定の値を返します。

#### `make-entity procedure object` 〔手続き＋〕

手続き成分が `procedure` で `extra` 成分が `object` である、新しく割り当てられた
エンティティを返します。

#### `entity? object` 〔手続き＋〕

`object` がエンティティなら `#t` を、そうでなければ `#f` を返します。

#### `entity-procedure entity` 〔手続き＋〕

`entity` の手続き成分を返します。

#### `set-entity-procedure! entity procedure` 〔手続き＋〕

`entity` の手続き成分を `procedure` に変えます。未規定の値を返します。

#### `entity-extra entity` 〔手続き＋〕

`entity` の `extra` 成分を返します。

#### `set-entity-extra! entity object` 〔手続き＋〕

`entity` の `extra` 成分を `object` に変えます。未規定の値を返します。
