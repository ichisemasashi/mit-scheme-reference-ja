<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 6 文字列

**文字列（string）**とは、可変の文字の並びです。現在の MIT Scheme の実装では、文字列の
要素はすべて述語 `char-ascii?` を満たさなければなりません。誰かが MIT Scheme を非
ASCII のオペレーティングシステムに移植すると、この要求は変わります。

文字列は、二重引用符 `" "` で囲んだ文字の並びとして書きます。文字列の中に二重引用符を
含めるには、二重引用符の前にバックスラッシュ `\` を置きます（エスケープします）。次の
ようにです。

```scheme
"The word \"recursion\" has many meanings."
```

この文字列の表示表現は次のとおりです。

```text
The word "recursion" has many meanings.
```

文字列の中にバックスラッシュを含めるには、その前にもう1つのバックスラッシュを置きます。
たとえば、

```scheme
"Use #\\Control-q to quit."
```

この文字列の表示表現は次のとおりです。

```text
Use #\Control-q to quit.
```

二重引用符やバックスラッシュの前に置かれないバックスラッシュの効果は、標準 Scheme では
未規定ですが、MIT Scheme は他の3つの文字について効果を定めています。`\t`、`\n`、`\f`
です。これらのエスケープ列は、それぞれ次の文字に変換されます。`#\tab`、`#\newline`、
`#\page`。最後に、バックスラッシュにちょうど3桁の8進数字が続いたものは、ASCII コードが
それらの数字である文字に変換されます。

文字列リテラルが1つの行から次の行へ続く場合、文字列は行の切れ目に改行文字（`#\newline`）
を含みます。標準 Scheme は、行の切れ目で文字列リテラルに何が現れるかを規定していません。

文字列の**長さ（length）**は、それが含む文字の数です。この数は、文字列が作られるときに
定まる正確な非負整数です（ただし6.10節「可変長文字列」を見よ）。文字列の各文字は
**添字（index）**を持ちます。これは、文字列における文字の位置を示す数です。文字列の
最初の（もっとも左の）文字の添字は 0 で、最後の文字の添字は文字列の長さより1つ小さい
値です。文字列の妥当な添字は、文字列の長さより小さい正確な非負整数です。

いくつかの文字列手続きは**部分文字列（substring）**を操作します。部分文字列とは文字列の
一区間で、次の関係を満たす2つの整数 `start` と `end` で指定されます。

```text
0 ≤ start ≤ end ≤ (string-length string)
```

`start` は部分文字列の最初の文字の添字で、`end` は部分文字列の最後の文字の添字より1つ
大きい値です。したがって `start` と `end` が等しければ、それらは空の部分文字列を指し、
`start` が 0 で `end` が `string` の長さなら、それらは `string` の全体を指します。

文字列を操作する手続きのいくつかは、大文字と小文字の違いを無視します。大文字小文字を
無視する版は、名前に `-ci`（「case insensitive」の意）を含みます。

## 6.1 文字列の構築

#### `make-string k [char]` 〔手続き〕

長さ `k` の新しく割り当てられた文字列を返します。`char` を指定すれば、文字列のすべての
要素が `char` に初期化され、そうでなければ文字列の内容は未規定です。`char` は述語
`char-ascii?` を満たさなければなりません。

```scheme
(make-string 10 #\x)                      ⇒ "xxxxxxxxxx"
```

#### `string char …` 〔手続き＋〕

指定された文字からなる、新しく割り当てられた文字列を返します。引数はすべて `char-ascii?`
を満たさなければなりません。

```scheme
(string #\a)                                            ⇒ "a"
(string #\a #\b #\c)                                    ⇒ "abc"
(string #\a #\space #\b #\space #\c)                    ⇒ "a b c"
(string)                                                ⇒ ""
```

#### `list->string char-list` 〔手続き〕

`char-list` は ASCII 文字のリストでなければなりません。`list->string` は、`char-list`
の要素から作られた、新しく割り当てられた文字列を返します。これは `(apply string
char-list)` と等価です。この演算の逆は `string->list` です。

```scheme
(list->string '(#\a #\b))                     ⇒ "ab"
(string->list "Hello")                        ⇒ (#\H #\e #\l #\l #\o)
```

#### `string-copy string` 〔手続き〕

`string` の新しく割り当てられた複製を返します。

可変長文字列に関する注意: 結果の最大長は `string` の長さだけに依存し、その最大長には
依存しません。文字列を複製してその最大長を保ちたければ、次のようにします。

```scheme
(define (string-copy-preserving-max-length string)
  (let ((length))
    (dynamic-wind
     (lambda ()
       (set! length (string-length string))
       (set-string-length! string
                           (string-maximum-length string)))
     (lambda ()
       (string-copy string))
     (lambda ()
       (set-string-length! string length)))))
```

## 6.2 文字列の成分の選択

#### `string? object` 〔手続き〕

`object` が文字列なら `#t` を、そうでなければ `#f` を返します。

```scheme
(string? "Hi")                           ⇒ #t
(string? 'Hi)                            ⇒ #f
```

#### `string-length string` 〔手続き〕

`string` の長さを正確な非負整数として返します。

```scheme
(string-length "")                     ⇒ 0
(string-length "The length")           ⇒ 10
```

#### `string-null? string` 〔手続き〕

`string` の長さが 0 なら `#t` を、そうでなければ `#f` を返します。

```scheme
(string-null? "")                       ⇒ #t
(string-null? "Hi")                     ⇒ #f
```

#### `string-ref string k` 〔手続き〕

`string` の `k` 番目の文字を返します。`k` は `string` の妥当な添字でなければなりません。

```scheme
(string-ref "Hello" 1)                ⇒ #\e
(string-ref "Hello" 5)                 error> 5 not in correct range
```

#### `string-set! string k char` 〔手続き〕

`char` を `string` の `k` 番目の要素に格納し、未規定の値を返します。`k` は `string` の
妥当な添字でなければならず、`char` は述語 `char-ascii?` を満たさなければなりません。

```scheme
(define str "Dog")                     ⇒ unspecified
(string-set! str 0 #\L)                ⇒ unspecified
str                                    ⇒ "Log"
(string-set! str 3 #\t)                 error> 3 not in correct range
```

## 6.3 文字列の比較

#### `string=? string1 string2` 〔手続き〕
#### `substring=? string1 start end string2 start end` 〔手続き＋〕
#### `string-ci=? string1 string2` 〔手続き〕
#### `substring-ci=? string1 start end string2 start end` 〔手続き＋〕

2つの文字列（部分文字列）が同じ長さで、同じ（相対的な）位置に同じ文字を含むなら `#t`
を、そうでなければ `#f` を返します。`string-ci=?` と `substring-ci=?` は大文字と小文字
を区別しませんが、`string=?` と `substring=?` は区別します。

```scheme
(string=? "PIE" "PIE")                          ⇒ #t
(string=? "PIE" "pie")                          ⇒ #f
(string-ci=? "PIE" "pie")                       ⇒ #t
(substring=? "Alamo" 1 3 "cola" 2 4)            ⇒ #t ; "la" を比較する
```

#### `string<? string1 string2` 〔手続き〕
#### `substring<? string1 start1 end1 string2 start2 end2` 〔手続き＋〕
#### `string>? string1 string2` 〔手続き〕
#### `string<=? string1 string2` 〔手続き〕
#### `string>=? string1 string2` 〔手続き〕
#### `string-ci<? string1 string2` 〔手続き〕
#### `substring-ci<? string1 start1 end1 string2 start2 end2` 〔手続き＋〕
#### `string-ci>? string1 string2` 〔手続き〕
#### `string-ci<=? string1 string2` 〔手続き〕
#### `string-ci>=? string1 string2` 〔手続き〕

これらの手続きは、文字列（部分文字列）を、それが含む文字の順序に従って比較します
（5.2節「文字の比較」も見よ）。引数は辞書式（辞書）順で比較されます。2つの文字列が
長さで異なるが、短いほうの長さまで同じなら、短いほうが長いほうより小さいとみなされ
ます。

```scheme
(string<? "cat" "dog")                 ⇒ #t
(string<? "cat" "DOG")                 ⇒ #f
(string-ci<? "cat" "DOG")              ⇒ #t
(string>? "catkin" "cat")              ⇒ #t ; 短いほうが小さい
```

#### `string-compare string1 string2 if-eq if-lt if-gt` 〔手続き＋〕
#### `string-compare-ci string1 string2 if-eq if-lt if-gt` 〔手続き＋〕

`if-eq`、`if-lt`、`if-gt` は引数のない手続き（thunk）です。2つの文字列が比較され、
等しければ `if-eq` が適用され、`string1` が `string2` より小さければ `if-lt` が適用され、
そうでなく `string1` が `string2` より大きければ `if-gt` が適用されます。手続きの値は、
適用された thunk の値です。`string-compare` は大文字と小文字を区別し、
`string-compare-ci` は区別しません。

```scheme
(define (cheer) (display "Hooray!"))
(define (boo)        (display "Boo-hiss!"))
(string-compare "a" "b" cheer (lambda() 'ignore) boo)
           -| Hooray!
           ⇒ unspecified
```

#### `string-hash string` 〔手続き＋〕
#### `string-hash-mod string k` 〔手続き＋〕

`string-hash` は、指定された文字列をハッシュ表に格納するのに使える正確な非負整数を
返します。（`string=?` の意味で）等しい文字列は等しい（`=`）ハッシュコードを返し、
等しくないが似た文字列は、ふつう互いに異なるハッシュコードに写されます。

`string-hash-mod` は `string-hash` に似ていますが、正確な非負整数 `k` に基づいて結果を
特定の範囲に限る点が異なります。次は等価です。

```scheme
(string-hash-mod string k)
(modulo (string-hash string) k)
```

## 6.4 文字列における大文字小文字

#### `string-capitalized? string` 〔手続き＋〕
#### `substring-capitalized? string start end` 〔手続き＋〕

これらの手続きは、文字列（部分文字列）の最初の語が先頭大文字で、それに続く語がすべて
小文字か先頭大文字なら `#t` を、そうでなければ `#f` を返します。語とは、非英字または
文字列（部分文字列）の端で区切られた、空でない連続した英字の並びと定義されます。語が
先頭大文字（capitalized）であるとは、最初の文字が大文字で、残りの文字がすべて小文字で
あることをいいます。

```scheme
(map string-capitalized? '(""                "A"       "art" "Art" "ART"))
                                 ⇒ (#f       #t        #f      #t        #f)
```

#### `string-upper-case? string` 〔手続き＋〕
#### `substring-upper-case? string start end` 〔手続き＋〕
#### `string-lower-case? string` 〔手続き＋〕
#### `substring-lower-case? string start end` 〔手続き＋〕

これらの手続きは、文字列（部分文字列）のすべての文字（レター）が正しい大文字小文字なら
`#t` を、そうでなければ `#f` を返します。文字列（部分文字列）は少なくとも1つの文字を
含まなければならず、そうでなければ手続きは `#f` を返します。

```scheme
(map string-upper-case? '(""              "A"      "art" "Art" "ART"))
                            ⇒ (#f         #t       #f      #f       #t)
```

#### `string-capitalize string` 〔手続き＋〕
#### `string-capitalize! string` 〔手続き＋〕
#### `substring-capitalize! string start end` 〔手続き＋〕

`string-capitalize` は、最初の英字が大文字で残りの英字が小文字である、`string` の
新しく割り当てられた複製を返します。たとえば `"abcDEF"` は `"Abcdef"` になります。
`string-capitalize!` は `string-capitalize` の破壊的な版です。`string` を書き換え、
未規定の値を返します。`substring-capitalize!` は `string` の指定された部分を破壊的に
先頭大文字化します。

#### `string-downcase string` 〔手続き＋〕
#### `string-downcase! string` 〔手続き＋〕
#### `substring-downcase! string start end` 〔手続き＋〕

`string-downcase` は、すべての大文字が小文字に変えられた、`string` の新しく割り当て
られた複製を返します。`string-downcase!` は `string-downcase` の破壊的な版です。
`string` を書き換え、未規定の値を返します。`substring-downcase!` は `string` の指定
された部分の大文字小文字を破壊的に変えます。

```scheme
(define str "ABCDEFG")              ⇒ unspecified
(substring-downcase! str 3 5)       ⇒ unspecified
str                                 ⇒ "ABCdeFG"
```

#### `string-upcase string` 〔手続き＋〕
#### `string-upcase! string` 〔手続き＋〕
#### `substring-upcase! string start end` 〔手続き＋〕

`string-upcase` は、すべての小文字が大文字に変えられた、`string` の新しく割り当て
られた複製を返します。`string-upcase!` は `string-upcase` の破壊的な版です。`string`
を書き換え、未規定の値を返します。`substring-upcase!` は `string` の指定された部分の
大文字小文字を破壊的に変えます。

## 6.5 文字列の切り貼り

#### `string-append string …` 〔手続き〕

与えられた文字列の連結から作られた、新しく割り当てられた文字列を返します。引数がなけ
れば、`string-append` は空文字列（`""`）を返します。

```scheme
(string-append)                               ⇒ ""
(string-append "*" "ace" "*")                 ⇒ "*ace*"
(string-append "" "" "")                      ⇒ ""
(eq? str (string-append str))                 ⇒ #f ; 新しく割り当てられる
```

#### `substring string start end` 〔手続き〕

添字 `start`（を含む）から始まり `end`（を含まない）で終わる `string` の文字から作られた、
新しく割り当てられた文字列を返します。

```scheme
(substring "" 0 0)                    ⇒ ""
(substring "arduous" 2 5)             ⇒ "duo"
(substring "arduous" 2 8)              error> 8 not in correct range

(define (string-copy s)
  (substring s 0 (string-length s)))
```

#### `string-head string end` 〔手続き＋〕

`end` まで（を含まない）の `string` の先頭部分文字列の、新しく割り当てられた複製を
返します。次のように定義できたはずです。

```scheme
(define (string-head string end)
  (substring string 0 end))
```

#### `string-tail string start` 〔手続き＋〕

添字 `start` から始まり `string` の末尾まで続く、`string` の末尾部分文字列の、新しく
割り当てられた複製を返します。次のように定義できたはずです。

```scheme
(define (string-tail string start)
  (substring string start (string-length string)))
```

```scheme
(string-tail "uncommon" 2)             ⇒ "common"
```

#### `string-pad-left string k [char]` 〔手続き＋〕
#### `string-pad-right string k [char]` 〔手続き＋〕

これらの手続きは、`char` を使って `string` を長さ `k` まで詰めることで作られた、新しく
割り当てられた文字列を返します。`char` が与えられなければ、既定で `#\space` です。`k`
が `string` の長さより小さければ、結果の文字列は `string` を切り詰めた形になります。
`string-pad-left` は文字列の先頭（もっとも小さい添字）から詰め文字を加えるか切り詰め、
`string-pad-right` は文字列の末尾（もっとも大きい添字）でそうします。

```scheme
(string-pad-left "hello" 4)                       ⇒ "ello"
(string-pad-left "hello" 8)                       ⇒ "   hello"
(string-pad-left "hello" 8 #\*)                   ⇒ "***hello"
(string-pad-right "hello" 4)                      ⇒ "hell"
(string-pad-right "hello" 8)                      ⇒ "hello   "
```

#### `string-trim string [char-set]` 〔手続き＋〕
#### `string-trim-left string [char-set]` 〔手続き＋〕
#### `string-trim-right string [char-set]` 〔手続き＋〕

`char-set` にない文字をすべて、`string` の（`string-trim`）両端／（`string-trim-left`）
先頭／（`string-trim-right`）末尾から取り除くことで作られた、新しく割り当てられた文字列
を返します。`char-set` は既定で `char-set:not-whitespace` です。

```scheme
(string-trim " in the end ")            ⇒ "in the end"
(string-trim "              ")          ⇒ ""
(string-trim "100th" char-set:numeric) ⇒ "100"
(string-trim-left "-.-+-=-" (char-set #\+))
                                        ⇒ "+-=-"
(string-trim "but (+ x y) is" (char-set #\( #\)))
                                        ⇒ "(+ x y)"
```

## 6.6 文字列の検索

この節の最初のいくつかの手続きは、文字列検索を行います。すなわち、与えられた文字列
（**テキスト**）を検索して、別の与えられた文字列（**パターン**）を真部分文字列として
含むかどうかを調べます。現在これらの手続きは、混成の方策で実装されています。4文字未満の
短いパターンには、素朴な文字列検索アルゴリズムが使われます。長いパターンには、
Boyer-Moore 文字列検索アルゴリズムが使われます。

#### `string-search-forward pattern string` 〔手続き＋〕
#### `substring-search-forward pattern string start end` 〔手続き＋〕

`pattern` は文字列でなければなりません。`string` の中で、部分文字列 `pattern` のもっとも
左の出現を検索します。成功すれば、一致した部分文字列の最初の文字の添字が返され、そう
でなければ `#f` が返されます。`substring-search-forward` は検索を `string` の指定された
部分文字列に限り、`string-search-forward` は `string` の全体を検索します。

```scheme
(string-search-forward "rat" "pirate")
    ⇒ 2
(string-search-forward "rat" "pirate rating")
    ⇒ 2
(substring-search-forward "rat" "pirate rating" 4 13)
    ⇒ 7
(substring-search-forward "rat" "pirate rating" 9 13)
    ⇒ #f
```

#### `string-search-backward pattern string` 〔手続き＋〕
#### `substring-search-backward pattern string start end` 〔手続き＋〕

`pattern` は文字列でなければなりません。`string` の中で、部分文字列 `pattern` のもっとも
右の出現を検索します。成功すれば、一致した部分文字列の最後の文字の右の添字が返され、
そうでなければ `#f` が返されます。`substring-search-backward` は検索を `string` の指定
された部分文字列に限り、`string-search-backward` は `string` の全体を検索します。

```scheme
(string-search-backward "rat" "pirate")
    ⇒ 5
(string-search-backward "rat" "pirate rating")
    ⇒ 10
(substring-search-backward "rat" "pirate rating" 1 8)
    ⇒ 5
(substring-search-backward "rat" "pirate rating" 9 13)
    ⇒ #f
```

#### `string-search-all pattern string` 〔手続き＋〕
#### `substring-search-all pattern string start end` 〔手続き＋〕

`pattern` は文字列でなければなりません。`string` を検索して、部分文字列 `pattern` の
すべての出現を見つけます。出現のリストを返します。リストの各要素は、ある出現の最初の
文字を指す添字です。`substring-search-all` は検索を `string` の指定された部分文字列に
限り、`string-search-all` は `string` の全体を検索します。

```scheme
(string-search-all "rat" "pirate")
    ⇒ (2)
(string-search-all "rat" "pirate rating")
    ⇒ (2 7)
(substring-search-all "rat" "pirate rating" 4 13)
    ⇒ (7)
(substring-search-all "rat" "pirate rating" 9 13)
    ⇒ ()
```

#### `substring? pattern string` 〔手続き＋〕

`pattern` は文字列でなければなりません。`string` を検索して、部分文字列 `pattern` を
含むかどうかを調べます。`pattern` が `string` の部分文字列なら `#t` を、そうでなければ
`#f` を返します。

```scheme
(substring? "rat" "pirate")                     ⇒ #t
(substring? "rat" "outrage")                    ⇒ #f
(substring? "" any-string)                      ⇒ #t
(if (substring? "moon" text)
    (process-lunar text)
    'no-moon)
```

#### `string-find-next-char string char` 〔手続き＋〕
#### `substring-find-next-char string start end char` 〔手続き＋〕
#### `string-find-next-char-ci string char` 〔手続き＋〕
#### `substring-find-next-char-ci string start end char` 〔手続き＋〕

文字列（部分文字列）における `char` の最初の出現の添字を返します。`char` が文字列に現れ
なければ `#f` を返します。部分文字列の手続きでは、返される添字は部分文字列だけでなく
文字列の全体を基準とします。`-ci` の手続きは大文字と小文字を区別しません。

```scheme
(string-find-next-char "Adam" #\A)                          ⇒ 0
(substring-find-next-char "Adam" 1 4 #\A)                   ⇒ #f
(substring-find-next-char-ci "Adam" 1 4 #\A)                ⇒ 2
```

#### `string-find-next-char-in-set string char-set` 〔手続き＋〕
#### `substring-find-next-char-in-set string start end char-set` 〔手続き＋〕

文字列（または部分文字列）の中で、`char-set` にもある最初の文字の添字を返します。
`char-set` の文字がどれも `string` に現れなければ `#f` を返します。部分文字列の手続き
では、部分文字列だけが検索されますが、返される添字は部分文字列だけでなく文字列の全体を
基準とします。

```scheme
(string-find-next-char-in-set my-string char-set:alphabetic)
     ⇒ my-string の最初の語の開始位置
; 述語としても使える:
(if (string-find-next-char-in-set my-string
                                          (char-set #\( #\) ))
     'contains-parentheses
     'no-parentheses)
```

#### `string-find-previous-char string char` 〔手続き＋〕
#### `substring-find-previous-char string start end char` 〔手続き＋〕
#### `string-find-previous-char-ci string char` 〔手続き＋〕
#### `substring-find-previous-char-ci string start end char` 〔手続き＋〕

文字列（部分文字列）における `char` の最後の出現の添字を返します。`char` が文字列に現れ
なければ `#f` を返します。部分文字列の手続きでは、返される添字は部分文字列だけでなく
文字列の全体を基準とします。`-ci` の手続きは大文字と小文字を区別しません。

#### `string-find-previous-char-in-set string char-set` 〔手続き＋〕
#### `substring-find-previous-char-in-set string start end char-set` 〔手続き＋〕

文字列（部分文字列）の中で、`char-set` にもある最後の文字の添字を返します。部分文字列の
手続きでは、返される添字は部分文字列だけでなく文字列の全体を基準とします。

## 6.7 文字列の照合

#### `string-match-forward string1 string2` 〔手続き＋〕
#### `substring-match-forward string1 start end string2 start end` 〔手続き＋〕
#### `string-match-forward-ci string1 string2` 〔手続き＋〕
#### `substring-match-forward-ci string1 start end string2 start end` 〔手続き＋〕

2つの文字列（部分文字列）を先頭から比較し、同じである文字の数を返します。2つの文字列
（部分文字列）が違う文字で始まれば 0 を返します。`-ci` の手続きは大文字と小文字を区別
しません。

```scheme
(string-match-forward "mirror" "micro") ⇒ 2 ; "mi" が一致
(string-match-forward "a" "b")                ⇒ 0 ; 一致なし
```

#### `string-match-backward string1 string2` 〔手続き＋〕
#### `substring-match-backward string1 start end string2 start end` 〔手続き＋〕
#### `string-match-backward-ci string1 string2` 〔手続き＋〕
#### `substring-match-backward-ci string1 start end string2 start end` 〔手続き＋〕

2つの文字列（部分文字列）を末尾から始めて前方へ向かって照合し、同じである文字の数を
返します。2つの文字列（部分文字列）が違う文字で終われば 0 を返します。`-ci` の手続き
は大文字と小文字を区別しません。

```scheme
(string-match-backward-ci "BULBOUS" "fractious")
                                                ⇒ 3 ; "ous" が一致
```

#### `string-prefix? string1 string2` 〔手続き＋〕
#### `substring-prefix? string1 start1 end1 string2 start2 end2` 〔手続き＋〕
#### `string-prefix-ci? string1 string2` 〔手続き＋〕
#### `substring-prefix-ci? string1 start1 end1 string2 start2 end2` 〔手続き＋〕

これらの手続きは、最初の文字列（部分文字列）が2番目の接頭辞をなすなら `#t` を、そう
でなければ `#f` を返します。`-ci` の手続きは大文字と小文字を区別しません。

```scheme
(string-prefix? "abc" "abcdef")                   ⇒ #t
(string-prefix? "" any-string)                    ⇒ #t
```

#### `string-suffix? string1 string2` 〔手続き＋〕
#### `substring-suffix? string1 start1 end1 string2 start2 end2` 〔手続き＋〕
#### `string-suffix-ci? string1 string2` 〔手続き＋〕
#### `substring-suffix-ci? string1 start1 end1 string2 start2 end2` 〔手続き＋〕

これらの手続きは、最初の文字列（部分文字列）が2番目の接尾辞をなすなら `#t` を、そう
でなければ `#f` を返します。`-ci` の手続きは大文字と小文字を区別しません。

```scheme
(string-suffix? "ous" "bulbous")                  ⇒ #t
(string-suffix? "" any-string)                    ⇒ #t
```

## 6.8 正規表現

MIT Scheme は、正規表現を使って文字列を検索・照合する機能を提供します。このマニュアルは
正規表現を定義しません。かわりに『The Emacs Editor』の「Syntax of Regular Expressions」
の節を見てください。

正規表現のサポートは、実行時に読み込めるオプションです。使うには、ここで定義する手続き
を呼ぶ前に一度、次を実行します。

```scheme
(load-option 'regular-expression)
```

正規表現の照合と検索を行う手続きは、標準化された引数を受け取ります。`regexp` は正規
表現で、文字列です。`string` は照合または検索される文字列です。部分文字列を操作する
手続きは、ふつうの意味の `start` と `end` の添字の引数も受け取ります。省略可能引数
`case-fold?` は、照合・検索が大文字小文字を区別するかどうかを言います。`case-fold?` が
`#f` なら区別し、そうでなければ区別しません。省略可能引数 `syntax-table` は、どの文字が
合法な語の構成要素かといった文字の構文を定める、文字構文表です。この機能はおもに Edwin
のためのものなので、文字構文表はここでは説明しません。`syntax-table` に `#f` を与える
（か省く）と、既定の文字構文が選ばれます。これは Edwin の基本モードと等価です。

#### `re-string-match regexp string [case-fold? [syntax-table]]` 〔手続き＋〕
#### `re-substring-match regexp string start end [case-fold? [syntax-table]]` 〔手続き＋〕

これらの手続きは、`regexp` をそれぞれの文字列または部分文字列に対して照合し、一致が
なければ `#f` を、一致が成功すれば一組の一致レジスタ（下記参照）を返します。一致した
部分文字列を取り出す方法を示す例を挙げます。

```scheme
(let ((r (re-substring-match regexp string start end)))
  (and r
        (substring string start (re-match-end-index 0 r))))
```

#### `re-string-search-forward regexp string [case-fold? [syntax-table]]` 〔手続き＋〕
#### `re-substring-search-forward regexp string start end [case-fold? [syntax-table]]` 〔手続き＋〕

`string` の中で、`regexp` に一致するもっとも左の部分文字列を検索します。検索が成功すれば
一組の一致レジスタ（下記参照）を、失敗すれば `#f` を返します。
`re-substring-search-forward` は検索を `string` の指定された部分文字列に限り、
`re-string-search-forward` は `string` の全体を検索します。

#### `re-string-search-backward regexp string [case-fold? [syntax-table]]` 〔手続き＋〕
#### `re-substring-search-backward regexp string start end [case-fold? [syntax-table]]` 〔手続き＋〕

`string` の中で、`regexp` に一致するもっとも右の部分文字列を検索します。検索が成功すれば
一組の一致レジスタ（下記参照）を、失敗すれば `#f` を返します。
`re-substring-search-backward` は検索を `string` の指定された部分文字列に限り、
`re-string-search-backward` は `string` の全体を検索します。

照合または検索が成功すると、上の手続きは一組の一致レジスタを返します。一致レジスタは、
一致した文字列への添字を記録する、一組の添字レジスタです。各添字レジスタは、正規表現の
グループ化演算子 `\(` の1つの出現に対応し、一致したグループの開始添字（を含む）と終了
添字（を含まない）を記録します。これらのレジスタは 1 から 9 まで番号が付き、式の中の
グループ化演算子に左から右へ対応します。加えて、レジスタ 0 は正規表現に一致した部分
文字列の全体に対応します。

#### `re-match-start-index n registers` 〔手続き＋〕
#### `re-match-end-index n registers` 〔手続き＋〕

`n` は 0 以上 9 以下の正確な整数でなければなりません。`registers` は、上の正規表現の
照合または検索の手続きの1つが返した match-registers オブジェクトでなければなりません。
`re-match-start-index` は対応する正規表現レジスタの開始添字を返し、`re-match-end-index`
は対応する終了添字を返します。

#### `re-match-extract string registers n` 〔手続き＋〕

`registers` は、上の正規表現の照合または検索の手続きの1つが返した match-registers
オブジェクトでなければなりません。`string` は、`registers` を返した手続きに引数として
渡された文字列でなければなりません。`n` は 0 以上 9 以下の正確な整数でなければなりません。
一致した正規表現が `m` 個のグループ化演算子を含んでいた場合、この手続きの値は、`m` より
厳密に大きい `n` については未定義です。この手続きは、`registers` と `n` で指定された
一致レジスタに対応する部分文字列を取り出します。これは次の式と等価です。

```scheme
(substring string
              (re-match-start-index n registers)
              (re-match-end-index n registers))
```

#### `regexp-group alternative …` 〔手続き＋〕

各 `alternative` は正規表現でなければなりません。返される値は、グループ化演算子で結合
された選択肢からなる、新しい正規表現です。たとえば、

```scheme
(regexp-group "foo" "bar" "baz")
   ⇒ "\\(foo\\|bar\\|baz\\)"
```

## 6.9 文字列の変更

#### `string-replace string char1 char2` 〔手続き＋〕
#### `substring-replace string start end char1 char2` 〔手続き＋〕
#### `string-replace! string char1 char2` 〔手続き＋〕
#### `substring-replace! string start end char1 char2` 〔手続き＋〕

これらの手続きは、もとの文字列（部分文字列）における `char1` のすべての出現を `char2`
で置き換えます。`string-replace` と `substring-replace` は結果を含む新しく割り当て
られた文字列を返します。`string-replace!` と `substring-replace!` は `string` を破壊的
に書き換え、未規定の値を返します。

```scheme
(define str "a few words")              ⇒ unspecified
(string-replace str #\space #\-)        ⇒ "a-few-words"
(substring-replace str 2 9 #\space #\-) ⇒ "a few-words"
str                                     ⇒ "a few words"
(string-replace! str #\space #\-)       ⇒ unspecified
str                                     ⇒ "a-few-words"
```

#### `string-fill! string char` 〔手続き〕

`char` を `string` のすべての要素に格納し、未規定の値を返します。

#### `substring-fill! string start end char` 〔手続き＋〕

`char` を `string` の `start`（を含む）から `end`（を含まない）までの要素に格納し、
未規定の値を返します。

```scheme
(define s (make-string 10 #\space))              ⇒ unspecified
(substring-fill! s 2 8 #\*)                      ⇒ unspecified
s                                                ⇒ " ****** "
```

#### `substring-move-left! string1 start1 end1 string2 start2` 〔手続き＋〕
#### `substring-move-right! string1 start1 end1 string2 start2` 〔手続き＋〕

`string1` の `start1` から `end1` までの文字を、`string2` の `start2` 番目の位置に複製
します。文字は次のように複製されます（これが重要なのは `string1` と `string2` が `eqv?`
であるときだけであることに注意してください）。

**`substring-move-left!`**
複製は左端から始まり右へ向かって進みます（小さい添字から大きい添字へ）。したがって
`string1` と `string2` が同じなら、この手続きは文字列の中で文字を左へ動かします。

**`substring-move-right!`**
複製は右端から始まり左へ向かって進みます（大きい添字から小さい添字へ）。したがって
`string1` と `string2` が同じなら、この手続きは文字列の中で文字を右へ動かします。

次の例は、これらの手続きを使って文字列を組み立てる方法を示します（`string-append` を
使うほうが簡単だったでしょう）。

```scheme
(define answer (make-string 9 #\*))              ⇒ unspecified
answer                                           ⇒ "*********"
(substring-move-left! "start" 0 5 answer 0) ⇒ unspecified
answer                                           ⇒ "start****"
(substring-move-left! "-end" 0 4 answer 5) ⇒ unspecified
answer                                           ⇒ "start-end"
```

#### `reverse-string string` 〔手続き＋〕
#### `reverse-substring string start end` 〔手続き＋〕
#### `reverse-string! string` 〔手続き＋〕
#### `reverse-substring! string start end` 〔手続き＋〕

与えられた文字列または部分文字列の文字の順序を逆にします。`reverse-string` と
`reverse-substring` は新しく割り当てられた文字列を返します。`reverse-string!` と
`reverse-substring!` は引数の文字列を書き換え、未規定の値を返します。

```scheme
(reverse-string "foo bar baz")                    ⇒ "zab rab oof"
(reverse-substring "foo bar baz" 4 7)             ⇒ "rab"
(let ((foo "foo bar baz"))
  (reverse-string! foo)
  foo)                                            ⇒ "zab rab oof"
(let ((foo "foo bar baz"))
  (reverse-substring! foo 4 7)
  foo)                                            ⇒ "foo rab baz"
```

## 6.10 可変長文字列

MIT Scheme は、文字列の長さを限られた形で動的に調整できるようにしています。新しい文字列
が、どんな方法であれ割り当てられると、それは特定の長さを持ちます。割り当ての時点で、
**最大長（maximum length）**も与えられます。これは文字列の長さと少なくとも同じ大きさで
あることが保証されます。（最大長が長さよりわずかに大きいこともありますが、これに頼るのは
よくない考えです。プログラムは、最大長が文字列の割り当ての時点の長さと同じであると仮定
すべきです。）文字列が割り当てられたあと、演算 `set-string-length!` を使って、文字列の
長さを 0 から文字列の最大長まで（両端を含む）の任意の値に変えられます。

#### `string-maximum-length string` 〔手続き＋〕

`string` の最大長を返します。次が保証されます。

```scheme
(<= (string-length string)
     (string-maximum-length string))          ⇒ #t
```

文字列の最大長が変わることは決してありません。

#### `set-string-length! string k` 〔手続き＋〕

`string` の長さを `k` に変え、未規定の値を返します。`k` は `string` の最大長以下で
なければなりません。`set-string-length!` は `string` の最大長を変えません。

## 6.11 バイトベクタ

MIT Scheme は、文字列を 8 ビットの ASCII バイトを詰めたベクタとして実装します。
`string-ref` のような文字列の演算のほとんどは、これらの 8 ビットのコードを文字オブジェクト
に強制します。しかし、いくつかの低水準の演算が使えるようになっています。

#### `vector-8b-ref string k` 〔手続き＋〕

`string` の `k` 番目の文字を ASCII コードとして返します。`k` は `string` の妥当な添字
でなければなりません。

```scheme
(vector-8b-ref "abcde" 2)                      ⇒ 99 ; 'c' の ASCII
```

#### `vector-8b-set! string k ascii` 〔手続き＋〕

`ascii` を `string` の `k` 番目の要素に格納し、未規定の値を返します。`k` は `string` の
妥当な添字でなければならず、`ascii` は妥当な ASCII コードでなければなりません。

#### `vector-8b-fill! string start end ascii` 〔手続き＋〕

`ascii` を `string` の `start`（を含む）から `end`（を含まない）までの要素に格納し、
未規定の値を返します。`ascii` は妥当な ASCII コードでなければなりません。

#### `vector-8b-find-next-char string start end ascii` 〔手続き＋〕
#### `vector-8b-find-next-char-ci string start end ascii` 〔手続き＋〕

与えられた部分文字列における `ascii` の最初の出現の添字を返します。`ascii` が現れなけ
れば `#f` を返します。返される添字は部分文字列だけでなく文字列の全体を基準とします。
`ascii` は妥当な ASCII コードでなければなりません。`vector-8b-find-next-char-ci` は
大文字と小文字を区別しません。

#### `vector-8b-find-previous-char string start end ascii` 〔手続き＋〕
#### `vector-8b-find-previous-char-ci string start end ascii` 〔手続き＋〕

与えられた部分文字列における `ascii` の最後の出現の添字を返します。`ascii` が現れなけ
れば `#f` を返します。返される添字は部分文字列だけでなく文字列の全体を基準とします。
`ascii` は妥当な ASCII コードでなければなりません。`vector-8b-find-previous-char-ci`
は大文字と小文字を区別しません。
