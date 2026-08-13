<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 8 ベクタ

**ベクタ（vector）**とは、要素が正確な非負整数で添字づけられる異種構造です。ベクタは
ふつう同じ長さのリストより少ない場所を占め、ランダムに選ばれた要素にアクセスするのに
かかる平均時間は、ふつうリストよりベクタのほうが短いです。

ベクタの**長さ**は、それが含む要素の数です。この数は、ベクタが作られるときに固定される
正確な非負整数です。ベクタの妥当な添字は、ベクタの長さより小さい正確な非負整数です。
ベクタの最初の要素は 0 で添字づけられ、最後の要素はベクタの長さより1つ小さい値で添字
づけられます。

ベクタは記法 `#(object ...)` を使って書きます。たとえば、要素 0 に数 0、要素 1 に
リスト `(2 2 2 2)`、要素 2 に文字列 `"Anna"` を含む長さ 3 のベクタは、次のように書けます。

```scheme
#(0 (2 2 2 2) "Anna")
```

これはベクタの外部表現であって、ベクタに評価される式ではないことに注意してください。
リスト定数と同様に、ベクタ定数はクォートしなければなりません。

```scheme
'#(0 (2 2 2 2) "Anna")                  ⇒ #(0 (2 2 2 2) "Anna")
```

いくつかのベクタ手続きは**部分ベクタ（subvector）**を操作します。部分ベクタとはベクタの
一区間で、2つの正確な非負整数 `start` と `end` で指定されます。`start` は部分ベクタに
含まれる最初の要素の添字で、`end` は部分ベクタに含まれる最後の要素の添字より1つ大きい
値です。したがって `start` と `end` が同じなら、それらは空の部分ベクタを指し、`start`
が 0 で `end` がベクタの長さなら、それらはベクタの全体を指します。部分ベクタの妥当な
添字は、`start`（を含む）から `end`（を含まない）までの正確な整数です。

## 8.1 ベクタの構築

#### `make-vector k [object]` 〔手続き〕

`k` 個の要素を持つ、新しく割り当てられたベクタを返します。`object` が指定されれば、
`make-vector` はベクタの各要素を `object` に初期化します。そうでなければ結果の初期の
要素は未規定です。

#### `vector object …` 〔手続き〕

要素が与えられた引数である、新しく割り当てられたベクタを返します。`vector` は `list`
に相当します。

```scheme
(vector 'a 'b 'c)                              ⇒ #(a b c)
```

#### `vector-copy vector` 〔手続き＋〕

`vector` の複製である、新しく割り当てられたベクタを返します。

#### `list->vector list` 〔手続き〕

`list` の要素に初期化された、新しく割り当てられたベクタを返します。`list->vector` の
逆は `vector->list` です。

```scheme
(list->vector '(dididit dah))                    ⇒ #(dididit dah)
```

#### `make-initialized-vector k initialization` 〔手続き＋〕

`make-vector` に似ていますが、結果の要素が、手続き `initialization` を添字に対して呼ぶ
ことで決まる点が異なります。たとえば、

```scheme
(make-initialized-vector 5 (lambda (x) (* x x)))
      ⇒ #(0 1 4 9 16)
```

#### `vector-grow vector k` 〔手続き＋〕

`k` は `vector` の長さ以上でなければなりません。長さ `k` の新しく割り当てられたベクタを
返します。結果の最初の `(vector-length vector)` 個の要素は、`vector` の対応する要素から
初期化されます。結果の残りの要素は未規定です。

#### `vector-map procedure vector` 〔手続き＋〕

`procedure` は1引数の手続きでなければなりません。`vector-map` は `procedure` を `vector`
の要素に要素ごとに適用し、結果の新しく割り当てられたベクタを左から右への順で返します。
`procedure` が `vector` の要素に適用される動的な順序は未規定です。

```scheme
(vector-map cadr '#((a b) (d e) (g h)))               ⇒ #(b e h)
(vector-map (lambda (n) (expt n n)) '#(1 2 3 4))
                                                      ⇒ #(1 4 27 256)
(vector-map + '#(5 7 9))                              ⇒ #(5 7 9)
```

## 8.2 ベクタの成分の選択

#### `vector? object` 〔手続き〕

`object` がベクタなら `#t` を、そうでなければ `#f` を返します。

#### `vector-length vector` 〔手続き〕

`vector` の要素の数を返します。

#### `vector-ref vector k` 〔手続き〕

`vector` の `k` 番目の要素の内容を返します。`k` は `vector` の妥当な添字でなければなり
ません。

```scheme
(vector-ref '#(1 1 2 3 5 8 13 21) 5)           ⇒ 8
```

#### `vector-set! vector k object` 〔手続き〕

`object` を `vector` の `k` 番目の要素に格納し、未規定の値を返します。`k` は `vector`
の妥当な添字でなければなりません。

```scheme
(let ((vec (vector 0 '(2 2 2 2) "Anna")))
  (vector-set! vec 1 '("Sue" "Sue"))
  vec)
     ⇒ #(0 ("Sue" "Sue") "Anna")
```

#### `vector-first vector` 〔手続き＋〕
#### `vector-second vector` 〔手続き＋〕
#### `vector-third vector` 〔手続き＋〕
#### `vector-fourth vector` 〔手続き＋〕
#### `vector-fifth vector` 〔手続き＋〕
#### `vector-sixth vector` 〔手続き＋〕
#### `vector-seventh vector` 〔手続き＋〕
#### `vector-eighth vector` 〔手続き＋〕

これらの手続きは、`vector` の最初のいくつかの要素に、見てのとおりの形でアクセスします。
これらの手続きの1つの暗黙の添字が `vector` の妥当な添字でなければエラーです。

#### `vector-binary-search vector key<? unwrap-key key` 〔手続き＋〕

`key` に一致するキーを持つ要素を `vector` の中で検索し、見つかればその要素を、なければ
`#f` を返します。検索の演算にかかる時間は `vector` の長さの対数に比例します。`unwrap-key`
は `vector` の各要素をキーに写す手続きでなければなりません。`key<?` は要素のキーに全順序
を定める手続きでなければなりません。

```scheme
(define (translate number)
  (vector-binary-search '#((1 . i)
                           (2 . ii)
                           (3 . iii)
                           (6 . vi))
                        < car number))
(translate 2) ⇒ (2 . ii)
(translate 4) ⇒ #F
```

## 8.3 ベクタの切り出し

#### `subvector vector start end` 〔手続き＋〕

添字 `start`（を含む）から `end`（を含まない）までの `vector` の要素を含む、新しく
割り当てられたベクタを返します。

#### `vector-head vector end` 〔手続き＋〕

次と等価です。

```scheme
(subvector vector 0 end)
```

#### `vector-tail vector start` 〔手続き＋〕

次と等価です。

```scheme
(subvector vector start (vector-length vector))
```

## 8.4 ベクタの変更

#### `vector-fill! vector object` 〔手続き〕
#### `subvector-fill! vector start end object` 〔手続き＋〕

`object` をベクタ（部分ベクタ）のすべての要素に格納し、未規定の値を返します。

#### `subvector-move-left! vector1 start1 end1 vector2 start2` 〔手続き＋〕
#### `subvector-move-right! vector1 start1 end1 vector2 start2` 〔手続き＋〕

`vector1` の、添字 `start1`（を含む）から `end1`（を含まない）までの要素を、`vector2`
の添字 `start2`（を含む）から始まる位置へ破壊的に複製します。`vector1`、`start1`、
`end1` は妥当な部分ベクタを指定しなければならず、`start2` は `vector2` の妥当な添字で
なければなりません。もとの部分ベクタの長さは、`vector2` の長さから添字 `start2` を引いた
値を超えてはなりません。

要素は次のように複製されます（これが重要なのは `vector1` と `vector2` が `eqv?` である
ときだけであることに注意してください）。

**`subvector-move-left!`**
複製は左端から始まり右へ向かって進みます（小さい添字から大きい添字へ）。したがって
`vector1` と `vector2` が同じなら、この手続きはベクタの中で要素を左へ動かします。

**`subvector-move-right!`**
複製は右端から始まり左へ向かって進みます（大きい添字から小さい添字へ）。したがって
`vector1` と `vector2` が同じなら、この手続きはベクタの中で要素を右へ動かします。

#### `sort! vector procedure` 〔手続き＋〕
#### `merge-sort! vector procedure` 〔手続き＋〕
#### `quick-sort! vector procedure` 〔手続き＋〕

`procedure` は、`vector` の要素に全順序を定める2引数の手続きでなければなりません。
`vector` の要素は、`procedure` の定める順序でソートされるよう並べ替えられます。要素は
その場で（in place）並べ替えられます。すなわち、`vector` は要素が新しい順序になるよう
破壊的に書き換えられます。`sort!` は `vector` をその値として返します。

2つのソートアルゴリズムが実装されています。`merge-sort!` と `quick-sort!` です。手続き
`sort!` は `merge-sort!` の別名です。`sort` の定義も見よ。
