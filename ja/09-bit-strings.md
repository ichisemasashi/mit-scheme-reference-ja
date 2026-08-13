<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 9 ビット列

**ビット列（bit string）**とは、ビットの並びです。ビット列は集合を表したり、二進データ
を操作したりするのに使えます。ビット列の要素は、0 から、列のビット数より1つ小さい値まで、
右から左への順で番号が付きます（もっとも右のビットが 0 番です）。ビット列を整数に変換
するとき、0 番目のビットは 2 の 0 乗に対応し、1 番目のビットは 1 乗に対応し、以下同様
です。

ビット列はメモリに非常に密に符号化されます。各ビットはちょうど 1 ビットの記憶域を占め、
ビット列全体のオーバーヘッドは小さい定数で抑えられます。しかし、ビット列のビットに
アクセスするのは、ベクタや文字列の要素にアクセスするのに比べて遅いです。性能が何よりも
重要なら、より多くの場所を占めても、真偽値の集合を格納するには文字列を使うほうがよい
です。

ビット列の**長さ**は、それが含むビットの数です。この数は、ビット列が作られるときに固定
される正確な非負整数です。ビット列の妥当な添字は、ビット列の長さより小さい正確な非負
整数です。

ビット列は 0 個以上のビットを含めます。機械のワードの長さに制限されません。ビット列の
表示表現では、ビット列の内容の前に `#*` が付きます。内容はもっとも上位のビット（もっとも
大きい添字）から表示されます。

ビット列の外部表現は、Common Lisp のビット列の表現とは逆のビット順序を使うことに注意
してください。MIT Scheme の表現は将来、Common Lisp と互換にするために変えられそうです。
当面、この表現はデータとしてビット列を入力する手段ではなく、ビット列を見るための便宜と
考えるべきです。

```text
#*11111
#*1010
#*00000000
#*
```

ビット列の手続きはすべて MIT Scheme の拡張です。

## 9.1 ビット列の構築

#### `make-bit-string k initialization` 〔手続き＋〕

長さ `k` の新しく割り当てられたビット列を返します。`initialization` が `#f` なら、ビット
列は 0 ビットで埋められ、そうでなければ 1 ビットで埋められます。

```scheme
(make-bit-string 7 #f)                              ⇒ #*0000000
```

#### `bit-string-allocate k` 〔手続き＋〕

長さ `k` の新しく割り当てられたビット列を返しますが、初期化はしません。

#### `bit-string-copy bit-string` 〔手続き＋〕

`bit-string` の新しく割り当てられた複製を返します。

## 9.2 ビット列の成分の選択

#### `bit-string? object` 〔手続き＋〕

`object` がビット列なら `#t` を、そうでなければ `#f` を返します。

#### `bit-string-length bit-string` 〔手続き＋〕

`bit-string` の長さを返します。

#### `bit-string-ref bit-string k` 〔手続き＋〕

`k` 番目のビットが 1 なら `#t` を、そうでなければ `#f` を返します。`k` は `bit-string`
の妥当な添字でなければなりません。

#### `bit-string-set! bit-string k` 〔手続き＋〕

`bit-string` の `k` 番目のビットを 1 に設定し、未規定の値を返します。`k` は `bit-string`
の妥当な添字でなければなりません。

#### `bit-string-clear! bit-string k` 〔手続き＋〕

`bit-string` の `k` 番目のビットを 0 に設定し、未規定の値を返します。`k` は `bit-string`
の妥当な添字でなければなりません。

#### `bit-substring-find-next-set-bit bit-string start end` 〔手続き＋〕

`bit-string` の `start`（を含む）から `end`（を含まない）までの部分列における、立った
ビットの最初の出現の添字を返します。部分列のビットがどれも立っていなければ `#f` が返され
ます。返される添字は、部分列ではなくビット列の全体を基準とします。

次の手続きは、`bit-substring-find-next-set-bit` を使って、立ったビットをすべて見つけ、
その添字を表示します。

```scheme
(define (scan-bitstring bs)
  (let ((end (bit-string-length bs)))
    (let loop ((start 0))
       (let ((next
               (bit-substring-find-next-set-bit bs start end)))
         (if next
              (begin
                 (write-line next)
                 (if (< next end)
                     (loop (+ next 1)))))))))
```

## 9.3 ビット列の切り貼り

#### `bit-string-append bit-string-1 bit-string-2` 〔手続き＋〕

2つのビット列の引数を連結し、新しく割り当てられたビット列を結果として返します。結果
では、`bit-string-1` から複製されたビットが、`bit-string-2` から複製されたものより
下位（小さい添字）になります。

#### `bit-substring bit-string start end` 〔手続き＋〕

添字 `start`（を含む）から始まり `end`（を含まない）で終わる、`bit-string` から複製した
ビットからなる、新しく割り当てられたビット列を返します。

## 9.4 ビット列のビットごとの演算

#### `bit-string-zero? bit-string` 〔手続き＋〕

`bit-string` が 0 ビットだけを含むなら `#t` を、そうでなければ `#f` を返します。

#### `bit-string=? bit-string-1 bit-string-2` 〔手続き＋〕

2つのビット列の引数を比較し、同じ長さで同じビットを含むなら `#t` を、そうでなければ
`#f` を返します。

#### `bit-string-not bit-string` 〔手続き＋〕

`bit-string` のビットごとの論理否定である、新しく割り当てられたビット列を返します。

#### `bit-string-movec! target-bit-string bit-string` 〔手続き＋〕

`bit-string-not` の破壊的な版です。引数 `target-bit-string` と `bit-string` は同じ長さ
のビット列でなければなりません。`bit-string` のビットごとの論理否定が計算され、結果が
`target-bit-string` に置かれます。この手続きの値は未規定です。

#### `bit-string-and bit-string-1 bit-string-2` 〔手続き＋〕

引数のビットごとの論理「かつ（and）」である、新しく割り当てられたビット列を返します。
引数は同一の長さのビット列でなければなりません。

#### `bit-string-andc bit-string-1 bit-string-2` 〔手続き＋〕

`bit-string-1` と、`bit-string-2` のビットごとの論理否定との、ビットごとの論理「かつ」
である、新しく割り当てられたビット列を返します。引数は同一の長さのビット列でなければ
なりません。

#### `bit-string-or bit-string-1 bit-string-2` 〔手続き＋〕

引数のビットごとの論理「または（inclusive or）」である、新しく割り当てられたビット列を
返します。引数は同一の長さのビット列でなければなりません。

#### `bit-string-xor bit-string-1 bit-string-2` 〔手続き＋〕

引数のビットごとの論理「排他的または（exclusive or）」である、新しく割り当てられたビット
列を返します。引数は同一の長さのビット列でなければなりません。

#### `bit-string-and! target-bit-string bit-string` 〔手続き＋〕
#### `bit-string-or! target-bit-string bit-string` 〔手続き＋〕
#### `bit-string-xor! target-bit-string bit-string` 〔手続き＋〕
#### `bit-string-andc! target-bit-string bit-string` 〔手続き＋〕

これらは上の演算の破壊的な版です。引数 `target-bit-string` と `bit-string` は同じ長さ
のビット列でなければなりません。これらの手続きはそれぞれ、引数に対して対応するビット
ごとの論理演算を行い、結果を `target-bit-string` に置き、未規定の結果を返します。

## 9.5 ビット列の変更

#### `bit-string-fill! bit-string initialization` 〔手続き＋〕

`initialization` が `#f` なら `bit-string` を 0 で埋め、そうでなければ 1 で埋めます。
未規定の値を返します。

#### `bit-string-move! target-bit-string bit-string` 〔手続き＋〕

`bit-string` の内容を `target-bit-string` に移します。どちらの引数も同じ長さのビット列
でなければなりません。引数が同じビット列なら、演算の結果は未定義です。

#### `bit-substring-move-right! bit-string-1 start1 end1 bit-string-2 start2` 〔手続き＋〕

`bit-string-1` の、添字 `start1`（を含む）から `end1`（を含まない）までのビットを、
`bit-string-2` の添字 `start2`（を含む）から始まる位置へ破壊的に複製します。`start1` と
`end1` は `bit-string-1` の妥当な部分列の添字でなければならず、`start2` は
`bit-string-2` の妥当な添字でなければなりません。もとの部分列の長さは、`bit-string-2`
の長さから添字 `start2` を引いた値を超えてはなりません。

ビットは MSB から始めて LSB へ向かって複製されます。複製の向きが重要なのは、
`bit-string-1` と `bit-string-2` が `eqv?` であるときだけです。

## 9.6 ビット列の整数変換

#### `unsigned-integer->bit-string length integer` 〔手続き＋〕

`length` と `integer` はどちらも正確な非負整数でなければなりません。`integer` を、
`length` ビットの新しく割り当てられたビット列に変換します。`integer` が `length` ビット
で表現するには大きすぎれば、`condition-type:bad-range-argument` 型のエラーを通知します。

#### `signed-integer->bit-string length integer` 〔手続き＋〕

`length` は正確な非負整数でなければならず、`integer` は任意の正確な整数でよいです。
`integer` を、負の数には 2 の補数の符号化を使って、`length` ビットの新しく割り当てられた
ビット列に変換します。`integer` が `length` ビットで表現するには大きすぎれば、
`condition-type:bad-range-argument` 型のエラーを通知します。

#### `bit-string->unsigned-integer bit-string` 〔手続き＋〕
#### `bit-string->signed-integer bit-string` 〔手続き＋〕

`bit-string` を正確な整数に変換します。`bit-string->signed-integer` は `bit-string` を
符号付き整数の 2 の補数表現とみなし、同じ符号と絶対値の整数を作ります。
`bit-string->unsigned-integer` は `bit-string` を符号なしの量とみなし、それに応じて
整数に変換します。
