<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 15 オペレーティングシステムインタフェース

Scheme 標準は、ファイルを読み書きする単純な仕組み、すなわちファイルポートを提供します。
MIT Scheme は、オペレーティングシステムの他の側面を扱う追加の道具を提供します。

- **パス名（pathname）**は、ファイル名の構成部分を操作する、ほどよくオペレーティング
  システムに依存しない道具です。ファイル名の構成部分の既定値を実装するのに役立ちます。
- **現在の作業ディレクトリ**の制御。相対的なファイル名がそこから解釈される、ファイル
  システム上の場所です。
- ファイルを改名・複製・削除し、存在を調べる手続き。また、特定のファイルについて、その
  型（ディレクトリ、リンクなど）や長さといった詳しい情報を返す手続き。
- ディレクトリの内容を読む手続き。
- さまざまな形式の時刻を得る、形式どうしを変換する、人間が読める時刻の文字列を生成する
  手続き。
- 他のプログラムを Scheme のサブプロセスとして走らせ、その出力を読み、それに入力を書く
  手続き。
- Scheme がどのオペレーティングシステムのもとで走っているかを判定する手段。

## 15.1 パス名

MIT Scheme のプログラムは、ファイルを指し示すのに名前を使う必要があります。ファイルの
名前を扱ううえでの主な難しさは、ファイルシステムごとにファイルの命名形式が違うことです。
たとえば、いくつかのファイルシステム（実際にはファイルシステムを提供するオペレーティング
システム）と、そのそれぞれで等価なファイル名がどう見えるかの表を挙げます。

```text
システム            ファイル名
------            ---------
TOPS-20            <LISPIO>FORMAT.FASL.13
TOPS-10            FORMAT.FAS[1,4]
ITS               LISPIO;FORMAT FASL
MULTICS           >udd>LispIO>format.fasl
TENEX             <LISPIO>FORMAT.FASL;13
VAX/VMS           [LISPIO]FORMAT.FAS;13
UNIX              /usr/lispio/format.fasl
DOS               C:\USR\LISPIO\FORMAT.FAS
```

ファイル名を扱う各プログラムが、存在するすべての異なるファイル名の形式を知るのは不可能
でしょう。Scheme が移植される新しいオペレーティングシステムは、その前身のどれとも異なる
形式を使うかもしれません。そこで MIT Scheme は、ファイル名を表す2つの方法を提供します。
**ファイル名（filename）**（名前文字列（namestring）とも呼ばれます）は、ファイルシステム
に慣例的な実装依存の形の文字列です。**パス名（pathname）**は、ファイル名を実装非依存の
形で表す特別な抽象データオブジェクトです。この2つの表現のあいだを変換する手続きが提供
され、ファイルのすべての操作は、パス名を使って機械非依存の言葉で表せます。

MIT Scheme のプログラムが、複数種類のファイルシステムを持ちうるネットワーク環境で動作
できるように、パス名機構は、どのファイルシステムを使うかをファイル名が指定できるように
します。この文脈では、ふつうのネットワークの用語法に従って、各ファイルシステムを**ホスト
（host）**と呼びます[^1]。

この節で挙げる例は Unix のパス名に固有であることに注意してください。他のオペレーティング
システムのパス名は異なる外部表現を持ちます。

### 15.1.1 ファイル名とパス名

パス名オブジェクトは、ふつうファイル名（文字列）を構成部分へ構文解析して作られます。MIT
Scheme は、ファイル名をパス名へ、またその逆に変換する演算を提供します。

#### `->pathname object` 〔手続き＋〕

`object` の等価物であるパス名を返します。`object` はパス名か文字列でなければなりません。
`object` がパス名なら、それが返されます。`object` が文字列なら、この手続きはその文字列に
対応するパス名を返します。この場合、`(parse-namestring object #f #f)` と等価です。

```scheme
(->pathname "foo")                 ⇒ #[pathname 65 "foo"]
(->pathname "/usr/morris") ⇒ #[pathname 66 "/usr/morris"]
```

#### `parse-namestring thing [host [defaults]]` 〔手続き＋〕

`thing` をパス名にします。`thing` はパス名か文字列でなければなりません。`thing` がパス名
なら、それが返されます。`thing` が文字列なら、この手続きはその文字列に対応するパス名を、
`host` が指定するファイルシステムの構文に従って構文解析して返します。

この手続きはパス名の構成部分の既定値の補完を行いません。

省略可能引数は、文字列の構文解析にどの構文を使うべきかを決めるのに使われます。一般に、
これが本当に役立つのは、あなたの MIT Scheme の実装が複数のファイルシステムをサポートする
場合だけです。そうでなければ `->pathname` を使うでしょう。与えられれば、`host` はホスト
オブジェクトか `#f` でなければならず、`defaults` はパス名でなければなりません。`host` は
文字列の構文解析に使われる構文を指定します。`host` が与えられないか `#f` なら、`defaults`
のホスト成分が代わりに使われます。`defaults` が与えられなければ、`*default-pathname-defaults*`
のホスト成分が使われます。

#### `->namestring pathname` 〔手続き＋〕

`->namestring` は `pathname` に対応するファイル名である、新しく割り当てられた文字列を
返します。

```scheme
(->namestring (->pathname "/usr/morris/minor.van"))
     ⇒ "/usr/morris/minor.van"
```

#### `pathname-simplify pathname` 〔手続き＋〕

`pathname` と同じファイルまたはディレクトリを指すが、ある意味でより単純なパス名を返し
ます。`pathname-simplify` はつねにパス名を単純化できるとはかぎらないことに注意してください。
たとえば Unix でシンボリックリンクがあると、ディレクトリ `/usr/morris/../` は `/usr/` と
同じとはかぎりません。不確かな場合、ふるまいは控えめで、もとのパス名か部分的に単純化された
パス名を返します。

```scheme
(pathname-simplify "/usr/morris/../morris/dance")
       ⇒ #[pathname "/usr/morris/dance"]
```

### 15.1.2 パス名の構成部分

パス名オブジェクトはつねに、下で説明する6つの構成部分を持ちます。これらの構成部分は、
プログラムが異なるファイルシステムで同じように動作できるようにする共通のインタフェース
です。パス名の構成部分を、各ファイルシステムに固有の概念へ写すことは、Scheme の実装が
面倒を見ます。

**host（ホスト）**
ファイルが存在するファイルシステムの名前。現在の実装では、この構成部分はつねに、ランタイム
システムが自動的に埋めるホストオブジェクトです。ホスト成分を指定するときは、`#f` か変数
`local-host` の値のどちらかを使います。

**device（デバイス）**
多くのホストファイルシステムの「デバイス」または「ファイル構造」の概念に対応します。
ファイルを含む（論理的または物理的）デバイスの名前です。この構成部分は、PC のファイル
システムではドライブ文字であり、Unix のファイルシステムでは使われません。

**directory（ディレクトリ）**
多くのホストファイルシステムの「ディレクトリ」の概念に対応します。関連するファイルの
グループ（ふつう単一のユーザまたはプロジェクトに属するもの）の名前です。この構成部分は
すべてのファイルシステムでつねに使われます。

**name（名前）**
概念的に「同じ」ファイルと考えられるファイルのグループの名前。この構成部分はすべての
ファイルシステムでつねに使われます。

**type（型）**
多くのホストファイルシステムの「ファイルタイプ」または「拡張子」の概念に対応します。これ
はこれがどんな種類のファイルかを言います。同じ名前で異なる型のファイルは、ふつう何らかの
特定の形で関連します。たとえば、1つがソースファイル、別のものがそのソースをコンパイルした
形、3つ目がコンパイラからのエラーメッセージの一覧、というようにです。この構成部分は現在
すべてのファイルシステムで使われ、名前文字列の最後のドットに続く文字をとって作られます。

**version（版）**
多くのホストファイルシステムの「版番号」の概念に対応します。ふつうこれは、ファイルが変更
されるたびに増える数です。この構成部分は現在すべてのファイルシステムで使われません。

パス名は必ずしも特定のファイルの名前ではないことに注意してください。むしろ、ファイルに
どうアクセスするかの指定（場合によっては部分的な指定にすぎません）です。パス名は、実際に
存在するどのファイルにも対応する必要はなく、複数のパス名が同じファイルを指しうります。
たとえば、版が `newest` のパス名は、版が特定の数である点だけが異なる同じ構成部分のパス名
と、同じファイルを指すかもしれません。実際、版が `newest` のパス名は、時が経つにつれて
異なるファイルを指すかもしれません。そのようなパス名の意味はファイルシステムの状態に依存
するからです。「リンク」、複数のファイル名、論理デバイスなどの機能を持つファイルシステム
では、まったく異なって見える2つのパス名が、同じファイルを指すことがわかるかもしれません。
パス名を与えられてファイルにアクセスするには、`open-input-file` のようなファイルシステム
の演算をしなければなりません。

パス名に関わる2つの重要な演算は、**構文解析（parsing）**と**マージ（merging）**です。
構文解析は、ファイル名（ユーザがファイルの名前を求められて対話的に供給するものかもしれ
ません）をパス名オブジェクトへ変換することです。この演算は実装依存です。ファイル名の形式
が実装依存だからです。マージは、欠けた構成部分を持つパス名を取り、それらの構成部分の値を
既定値の供給元から補います。

パス名のすべての構成部分が指定される必要はありません。パス名の構成部分が欠けていれば、
その値は `#f` です。ファイルシステムのインタフェースがファイルに対して何か興味深いこと、
たとえばファイルを開くことをする前に、パス名の欠けた構成部分をすべて埋めなければなりません。
欠けた構成部分を持つパス名は、内部でさまざまな目的に使われます。とくに、ある構成部分を
指定しない名前文字列を構文解析すると、欠けた構成部分を持つパス名になります。

パス名のどの構成部分も、シンボル `unspecific` でありえます。これは、その構成部分が意味を
なさないファイルシステムで、その構成部分が単に存在しないことを意味します。たとえば、Unix、
Windows、OS/2 のファイルシステムはふつう版番号をサポートしないので、そのようなホストの
version 成分は `unspecific` かもしれません[^2]。

`#f` と `unspecific` に加えて、パス名の構成部分は次の意味のある値をとりえます。

**host**
実装で定められた型で、`host?` 述語を使って検査できます。

**device**
この構成部分をサポートするシステム（Windows と OS/2）では、1つの英字を含む文字列として
指定でき、その英字の大文字小文字は無視されます。

**directory**
空でないリストで、ディレクトリの経路を表します。ディレクトリの列で、その各ディレクトリは
前のディレクトリの中に名前を持ち、最後のものが経路全体が指定するディレクトリです。そのような
経路の各要素は、その左の要素が指定するディレクトリに対する相対的なディレクトリの名前を
指定します。リストの最初の要素は、シンボル `absolute` かシンボル `relative` のどちらかです。
リストの最初の要素がシンボル `absolute` なら、directory 成分（したがってパス名）は絶対
です。列の最初の成分はファイルシステムの「根（root）」で見つかります。directory が相対なら、
最初の成分はまだ指定されていない何らかのディレクトリで見つかります。ふつうこれは後で現在
の作業ディレクトリと指定されます。

リストの最初の要素としてのみ現れる `absolute` と `relative` を除けば、リストの続く各要素
は次のいずれかです。文字列（リテラルの構成部分）、シンボル `wild`（ディレクトリの読み手と
一緒に使うときにのみ意味を持ちます）、またはシンボル `up`（次のディレクトリが前のものの
「親」であることを意味します）。`up` は Unix と PC のファイルシステムのファイル `..` に
対応します。

（次の注記は、MIT Scheme が現在サポートするどのファイルシステムも指しませんが、完全性の
ために含めます。）「階層的」構造を持たないファイルシステムでは、指定された directory 成分
はつねに、最初の要素が `absolute` であるリストになります。システムが単一の大域的な
ディレクトリ以外のディレクトリをサポートしなければ、リストに他の要素はありません。システム
が「平坦な」ディレクトリ、すなわち下位ディレクトリのないディレクトリの大域的な集合を
サポートするなら、リストは2番目の要素を含み、それは文字列か `wild` です。言い換えると、
非階層的なファイルシステムは、それが階層的であるかのように扱われますが、階層的な機能は
使われません。この表現はそのようなファイルシステムにはやや不便ですが、プログラマがコード
をファイル階層の欠如に依存させるのを思いとどまらせます。

**name**
文字列（リテラルの構成部分）、またはシンボル `wild`（ディレクトリの読み手と一緒に使う
ときにのみ意味を持ちます）。

**type**
文字列（リテラルの構成部分）、またはシンボル `wild`（ディレクトリの読み手と一緒に使う
ときにのみ意味を持ちます）。

**version**
正確な正整数（リテラルの構成部分）、シンボル `newest`（そのファイルの利用できる最大の版
番号を選ぶことを意味します）、シンボル `oldest`（最小の版番号を選ぶことを意味します）、
またはシンボル `wild`（ディレクトリの読み手と一緒に使うときにのみ意味を持ちます）。将来、
`installed` などの他の値が加わるかもしれません。現在どのファイルシステムも版番号をサポート
しないので、この構成部分は使われず、`#f` と指定すべきであることに注意してください。

#### `make-pathname host device directory name type version` 〔手続き＋〕

構成部分がそれぞれの引数であるパス名オブジェクトを返します。各引数は、上で概説した対応する
構成部分の制限を満たさなければなりません。

```scheme
(make-pathname #f
               #f
               '(absolute "usr" "morris")
               "foo"
               "scm"
               #f)
     ⇒ #[pathname 67 "/usr/morris/foo.scm"]
```

#### `pathname-host pathname` 〔手続き＋〕
#### `pathname-device pathname` 〔手続き＋〕
#### `pathname-directory pathname` 〔手続き＋〕
#### `pathname-name pathname` 〔手続き＋〕
#### `pathname-type pathname` 〔手続き＋〕
#### `pathname-version pathname` 〔手続き＋〕

`pathname` の特定の構成部分を返します。

```scheme
(define x (->pathname "/usr/morris/foo.scm"))
(pathname-host x)       ⇒ #[host 1]
(pathname-device x)     ⇒ unspecific
(pathname-directory x) ⇒ (absolute "usr" "morris")
(pathname-name x)       ⇒ "foo"
(pathname-type x)       ⇒ "scm"
(pathname-version x)    ⇒ unspecific
```

#### `pathname-new-device pathname device` 〔手続き＋〕
#### `pathname-new-directory pathname directory` 〔手続き＋〕
#### `pathname-new-name pathname name` 〔手続き＋〕
#### `pathname-new-type pathname type` 〔手続き＋〕
#### `pathname-new-version pathname version` 〔手続き＋〕

それぞれの構成部分を第2引数で置き換えた `pathname` の新しい複製を返します。`pathname` は
変わりません。移植可能なプログラムは、構成部分を明示的に `unspecific` で置き換えるべきでは
ありません。状況によっては許されないかもしれないからです。

```scheme
(define p (->pathname "/usr/blisp/rel15"))
p
      ⇒ #[pathname 71 "/usr/blisp/rel15"]
(pathname-new-name p "rel100")
      ⇒ #[pathname 72 "/usr/blisp/rel100"]
(pathname-new-directory p '(relative "test" "morris"))
      ⇒ #[pathname 73 "test/morris/rel15"]
p
      ⇒ #[pathname 71 "/usr/blisp/rel15"]
```

#### `pathname-default-device pathname device` 〔手続き＋〕
#### `pathname-default-directory pathname directory` 〔手続き＋〕
#### `pathname-default-name pathname name` 〔手続き＋〕
#### `pathname-default-type pathname type` 〔手続き＋〕
#### `pathname-default-version pathname version` 〔手続き＋〕

これらの演算は、成分ごとの `pathname-new-` の演算（`pathname-new-device` など）に似て
いますが、指定された構成部分が `pathname` で `#f` の値を持つ場合にのみ、それを変える点が
異なります。

### 15.1.3 パス名の演算

#### `pathname? object` 〔手続き＋〕

`object` がパス名なら `#t` を、そうでなければ `#f` を返します。

#### `pathname=? pathname1 pathname2` 〔手続き＋〕

`pathname1` が `pathname2` と等価なら `#t` を、そうでなければ `#f` を返します。パス名は、
そのすべての構成部分が等価なら等価です。したがって等価な2つのパス名は、同じファイルまたは
等価な部分パス名を指定しなければなりません。ただし、逆は成り立ちません。等価でないパス名が
同じファイルを指定しうる（たとえば絶対と相対の directory 成分によって）し、まったくファイル
を指定しないパス名（たとえば name と directory 成分が指定されていない）が等価でありえます。

#### `pathname-absolute? pathname` 〔手続き＋〕

`pathname` が相対ではなく絶対のパス名オブジェクトなら `#t` を、そうでなければ `#f` を返し
ます。具体的には、この手続きは `pathname` の directory 成分がシンボル `absolute` で始まる
リストのとき `#t` を返し、他のすべての場合に `#f` を返します。すべてのパス名は絶対か相対
のどちらかなので、この手続きが `#f` を返せば、引数は相対のパス名です。

#### `directory-pathname? pathname` 〔手続き＋〕

`pathname` が directory 成分だけを持ち、ファイルの成分を持たなければ `#t` を返します。これ
はおおよそ次と等価ですが、より速いです。

```scheme
(define (directory-pathname? pathname)
  (string-null? (file-namestring pathname)))
```

#### `pathname-wild? pathname` 〔手続き＋〕

`pathname` がワイルドカードの構成部分を含めば `#t` を、そうでなければ `#f` を返します。

#### `merge-pathnames pathname [defaults [default-version]]` 〔手続き＋〕

`pathname` と `defaults` の構成部分を組み合わせて得られる構成部分を持つパス名を返します。
`defaults` は既定で `*default-pathname-defaults*` の値、`default-version` は既定で `newest`
です。

パス名は構成部分ごとに組み合わされます。`pathname` が欠けていない構成部分を持てば、それが
結果の構成部分になり、そうでなければ `defaults` の構成部分が使われます。`default-version`
は、その構成部分が `pathname` で欠けていたという情報を保つために `#f` にできます。directory
成分は特別に扱われます。両方のパス名が directory 成分としてリストを持ち、`pathname` の
directory 成分が相対（すなわち `relative` で始まる）なら、結果の directory 成分は `pathname`
の成分を `defaults` の成分に追加して作られます。たとえば、

```scheme
(define path1 (->pathname "scheme/foo.scm"))
(define path2 (->pathname "/usr/morris"))
path1
      ⇒ #[pathname 74 "scheme/foo.scm"]
path2
      ⇒ #[pathname 75 "/usr/morris"]
(merge-pathnames path1 path2)
      ⇒ #[pathname 76 "/usr/scheme/foo.scm"]
(merge-pathnames path2 path1)
      ⇒ #[pathname 77 "/usr/morris.scm"]
```

version のマージ規則はより複雑で、`pathname` が name を指定するかどうかによります。
`pathname` が name を指定しなければ、version は、与えられていなければ `defaults` から来
ます。しかし `pathname` が name を指定すれば、version は `defaults` の影響を受けません。
理由は、version が他の何らかのファイル名に「属して」おり、新しいものとは関係がなさそうだ
からです。最後に、この過程で version が欠けたままなら、`default-version` が使われます。

正味の効果は、ユーザが name だけを供給すれば、host、device、directory、type は `defaults`
から来ますが、version は `default-version` から来る、ということです。ユーザが何も供給しない
か、directory だけを供給すれば、name、type、version は `defaults` からまとめて来ます。

#### `*default-pathname-defaults*` 〔変数＋〕

これは既定のパス名既定値のパス名です。既定値の集合を必要とするどのパス名基本手続きも、それ
が与えられなければこれを使います。`set-working-directory-pathname!` は、新しい作業ディレク
トリをこの変数の古い値とマージして計算した新しい値を、この変数に設定します。

#### `pathname-default pathname device directory name type version` 〔手続き＋〕

この手続きは `pathname` のすべての構成部分を同時に既定値で補います。次のように定義できた
はずです。

```scheme
(define (pathname-default pathname
                               device directory name type version)
  (make-pathname (pathname-host pathname)
                    (or (pathname-device pathname) device)
                    (or (pathname-directory pathname) directory)
                    (or (pathname-name pathname) name)
                    (or (pathname-type pathname) type)
                    (or (pathname-version pathname) version)))
```

#### `file-namestring pathname` 〔手続き＋〕
#### `directory-namestring pathname` 〔手続き＋〕
#### `host-namestring pathname` 〔手続き＋〕
#### `enough-namestring pathname [defaults]` 〔手続き＋〕

これらの手続きは、パス名の情報の部分集合に対応する文字列を返します。`file-namestring` は
`pathname` の name、type、version 成分だけを表す文字列を返します。`directory-namestring`
の結果は host、device、directory 成分だけを表します。`host-namestring` は host 部分だけの
文字列を返します。

`enough-namestring` はもう1つの引数 `defaults` を取ります。`defaults`（既定で
`*default-pathname-defaults*`）に対する相対とみなしたときに、`pathname` が名指すファイルを
識別するのにちょうど十分な、短縮された名前文字列を返します。

```scheme
(file-namestring "/usr/morris/minor.van")
       ⇒ "minor.van"
(directory-namestring "/usr/morris/minor.van")
       ⇒ "/usr/morris/"
(enough-namestring "/usr/morris/men")
       ⇒ "men"            ;たぶん
```

#### `file-pathname pathname` 〔手続き＋〕
#### `directory-pathname pathname` 〔手続き＋〕
#### `enough-pathname pathname [defaults]` 〔手続き＋〕

これらの手続きは、パス名の情報の部分集合に対応するパス名を返します。`file-pathname` は
`pathname` の name、type、version 成分だけを持つパス名を返します。`directory-pathname` の
結果は、`pathname` の host、device、directory 成分を含むパス名です。

`enough-pathname` はもう1つの引数 `defaults` を取ります。`defaults`（既定で
`*default-pathname-defaults*`）に対する相対とみなしたときに、`pathname` が名指すファイルを
識別するのにちょうど十分な、短縮されたパス名を返します。

これらの手続きは `file-namestring`、`directory-namestring`、`enough-namestring` に似て
いますが、文字列ではなくパス名を返します。

#### `directory-pathname-as-file pathname` 〔手続き＋〕

`pathname` と等価だが、directory 成分がファイルとして表されるパス名を返します。最後の
ディレクトリが directory 成分から取り除かれ、name と type 成分に変換されます。これは
`pathname-as-directory` の逆演算です。

```scheme
(directory-pathname-as-file (->pathname "/usr/blisp/"))
      ⇒ #[pathname "/usr/blisp"]
```

#### `pathname-as-directory pathname` 〔手続き＋〕

`pathname` と等価だが、ファイルの成分が directory 成分に変換されたパス名を返します。
`pathname` が name、type、version 成分を持たなければ、それは変更されずに返されます。そう
でなければ、これらのファイルの成分が文字列に変換され、その文字列が directory 成分のリスト
の末尾に加えられます。これは `directory-pathname-as-file` の逆演算です。

```scheme
(pathname-as-directory (->pathname "/usr/blisp/rel5"))
       ⇒ #[pathname "/usr/blisp/rel5/"]
```

### 15.1.4 その他のパス名手続き

この節では、ホストオブジェクトの標準的な演算と、いくつかの役立つパス名を返す手続きを挙げ
ます。

#### `local-host` 〔変数＋〕

この変数は、その値として、ローカルホストのファイルシステムを記述するホストオブジェクトを
持ちます。

#### `host? object` 〔手続き＋〕

`object` がパス名のホストなら `#t` を、そうでなければ `#f` を返します。

#### `host=? host1 host2` 〔手続き＋〕

`host1` と `host2` が同じパス名のホストを表せば `#t` を、そうでなければ `#f` を返します。

#### `init-file-pathname [host]` 〔手続き＋〕

`host` 上のユーザの初期化ファイルのパス名を返します。`host` 引数は既定で `local-host` の
値です。初期化ファイルが存在しなければ、この手続きは `#f` を返します。

Unix では、初期化ファイルは `.scheme.init` と呼ばれます。Windows と OS/2 では、初期化
ファイルは `scheme.ini` と呼ばれます。どちらの場合も、`user-homedir-pathname` が計算する
ユーザのホームディレクトリに置かれます。

#### `user-homedir-pathname [host]` 〔手続き＋〕

`host` 上のユーザの「ホームディレクトリ」のパス名を返します。`host` 引数は既定で
`local-host` の値です。「ホームディレクトリ」の概念それ自体がやや実装依存ですが、ユーザが
初期化ファイルやメールのような個人的なファイルを置く場所であるべきです。

Unix では、ユーザのホームディレクトリは環境変数 `HOME` で指定されます。この変数が未定義
なら、`getlogin` システムコールを使って、それが失敗すれば `getuid` システムコールを使って
ユーザ名が計算されます。結果のユーザ名は `getpwnam` システムコールに渡されてホームディレクトリ
を得ます。

OS/2 では、ユーザのホームディレクトリを見つけるためにいくつかの発見的方法が試されます。
まず、環境変数 `HOME` が定義されていれば、それがホームディレクトリです。`HOME` が未定義
だが、`USERDIR` と `USER` 環境変数が定義され、ディレクトリ `%USERDIR%\%USER%` が存在すれば、
それが使われます。それも駄目なら、ディレクトリ `%USER%` が OS/2 システムドライブに存在すれ
ば、それが使われます。最後の手段として、OS/2 システムドライブがホームディレクトリです。

OS/2 と同様に、Windows の実装は環境変数に基づく発見的方法を使います。ユーザのホーム
ディレクトリは、次の順でいくつかの環境変数を調べて計算されます。

- `HOMEDRIVE` と `HOMEPATH` の両方が定義され、`%HOMEDRIVE%%HOMEPATH%` が存在する
  ディレクトリである。（これらの変数は Windows NT が自動的に定義します。）
- `HOME` が定義され、`%HOME%` が存在するディレクトリである。
- `USERDIR` と `USERNAME` が定義され、`%USERDIR%\%USERNAME%` が存在するディレクトリである。
- `USERDIR` と `USER` が定義され、`%USERDIR%\%USER%` が存在するディレクトリである。
- `USERNAME` が定義され、`%USERNAME%` が Windows システムドライブに存在するディレクトリで
  ある。
- `USER` が定義され、`%USER%` が Windows システムドライブに存在するディレクトリである。
- 最後に、他のすべてが駄目なら、Windows システムドライブがホームディレクトリとして使われ
  ます。

#### `system-library-pathname pathname` 〔手続き＋〕

`pathname` を MIT Scheme のシステムライブラリディレクトリの中で見つけます。`pathname` が
ライブラリの探索パス上で見つけられなければ、`condition-type:file-operation-error` 型の
エラーが通知されます。

```scheme
(system-library-pathname "compiler.com")
   ⇒ #[pathname 45 "/usr/local/lib/mit-scheme/compiler.com"]
```

#### `system-library-directory-pathname pathname` 〔手続き＋〕

MIT Scheme のシステムライブラリディレクトリのパス名を見つけます。`pathname` がライブラリの
探索パス上で見つけられなければ、`condition-type:file-operation-error` 型のエラーが通知
されます。

```scheme
(system-library-directory-pathname "options")
      ⇒ #[pathname 44 "/usr/local/lib/mit-scheme/options/"]
```

## 15.2 作業ディレクトリ

MIT Scheme が起動されると、現在の作業ディレクトリ（あるいは単に作業ディレクトリ）が
オペレーティングシステム依存の形で初期化されます。ふつう、それは Scheme が起動された
ディレクトリです。作業ディレクトリは、Scheme の中から `pwd` 手続きを呼んで判定でき、`cd`
手続きを呼んで変えられます。各 rep ループは独自の作業ディレクトリを持ち、下位の rep ループ
は、作られたときに上位で有効な値から作業ディレクトリを初期化します。

#### `working-directory-pathname` 〔手続き＋〕
#### `pwd` 〔手続き＋〕

現在の作業ディレクトリを、name、type、version 成分を持たず、host、device、directory 成分
だけを持つパス名として返します。`pwd` は `working-directory-pathname` の別名です。長い
名前はプログラム用、短い名前は対話的な使用のためのものです。

#### `set-working-directory-pathname! filename` 〔手続き＋〕
#### `cd filename` 〔手続き＋〕

`filename` を現在の作業ディレクトリにし、新しい現在の作業ディレクトリをパス名として返し
ます。`filename` は `pathname-as-directory` を使ってパス名に強制されます。`cd` は
`set-working-directory-pathname!` の別名です。長い名前はプログラム用、短い名前は対話的な
使用のためのものです。

加えて、`set-working-directory-pathname!` は、新しい作業ディレクトリをマージすることで
`*default-pathname-defaults*` の値を書き換えます。この手続きがトップレベルの rep ループで
実行されると、走っている Scheme 実行ファイルの作業ディレクトリを変えます。

```scheme
(set-working-directory-pathname! "/usr/morris/blisp")
       ⇒ #[pathname "/usr/morris/blisp/"]
(set-working-directory-pathname! "~")
       ⇒ #[pathname "/usr/morris/"]
```

この手続きは、`filename` が存在するディレクトリを指さなければエラーを通知します。`filename`
が絶対ではなく相対のパス名を記述すれば、この手続きは、作業ディレクトリを変える前に、それを
現在の作業ディレクトリに対する相対と解釈します。

```scheme
(working-directory-pathname)
       ⇒ #[pathname "/usr/morris/"]
(set-working-directory-pathname! "foo")
       ⇒ #[pathname "/usr/morris/foo/"]
```

#### `with-working-directory-pathname filename thunk` 〔手続き＋〕

この手続きは、現在の作業ディレクトリを一時的に `filename` に再束縛し、`thunk`（引数のない
手続き）を起動し、それから以前の作業ディレクトリを復元し、`thunk` が生んだ値を返します。
`filename` は `pathname-as-directory` を使ってパス名に強制されます。作業ディレクトリを
束縛するのに加えて、`with-working-directory-pathname` は変数 `*default-pathname-defaults*`
も束縛し、その変数の古い値を新しい作業ディレクトリのパス名とマージします。どちらの束縛も、
変数の動的束縛とまったく同じ形で行われます（2.3節「動的束縛」を見よ）。

## 15.3 ファイルの操作

この節では、ファイルとディレクトリを操作する手続きを説明します。これらの手続きはどれも、
多くの理由でいくつものエラーを通知しうります。これらのエラーの詳細はあまりにオペレーティング
システムに依存しすぎるので、ここでは記録しません。ただし、そのようなエラーがこれらの手続き
の1つによって通知されると、それは `condition-type:file-operation-error` 型です。

#### `file-exists? filename` 〔手続き＋〕
#### `file-exists-direct? filename` 〔手続き＋〕
#### `file-exists-indirect? filename` 〔手続き＋〕

これらの手続きは、`filename` が存在するファイルまたはディレクトリなら `#t` を、そうでなけ
れば `#f` を返します。シンボリックリンクをサポートするオペレーティングシステムで、ファイル
がシンボリックリンクなら、`file-exists-direct?` はリンクの存在を調べ、
`file-exists-indirect?` と `file-exists?` はリンクが指すファイルの存在を調べます。

#### `copy-file source-filename target-filename` 〔手続き＋〕

`source-filename` が名指すファイルの複製を作ります。複製は、`target-filename` という新しい
ファイルを作り、それを `source-filename` と同じデータで埋めることで行われます。

#### `rename-file source-filename target-filename` 〔手続き＋〕

`source-filename` の名前を `target-filename` に変えます。Unix の実装では、これはファイル
システムをまたいでの改名はしません。

#### `delete-file filename` 〔手続き＋〕

`filename` という名前のファイルを削除します。

#### `delete-file-no-errors filename` 〔手続き＋〕

`delete-file` に似ていますが、削除のあいだにエラーが起きたかどうかを示す真偽値を返します。
エラーが起きなければ `#t` が返されます。`condition-type:file-error` 型か
`condition-type:port-error` 型のエラーが通知されれば、`#f` が返されます。

#### `hard-link-file source-filename target-filename` 〔手続き＋〕

`source-filename` から `target-filename` へのハードリンクを作ります。この演算は
`source-filename` が指定するファイルに、古い名前に加えて新しい名前を与えます。

これは現在 Unix システムでのみ働きます。さらに、`source-filename` と `target-filename` が
同じファイルシステムの名前を指すときにのみ働くよう制限されます。

#### `soft-link-file source-filename target-filename` 〔手続き＋〕

ファイル `source-filename` を指す、`target-filename` という新しいソフトリンクを作ります。
（ソフトリンクはシンボリックリンクと呼ばれることもあります。）`source-filename` は文字列
として解釈されることに注意してください（望むならパス名オブジェクトとして指定できます）。
この文字列の内容はソフトリンクとしてファイルシステムに格納されます。ファイル演算がリンクを
開こうとすると、リンクの内容はそのときのリンクの位置に対する相対と解釈されます。

これは現在 Unix システムでのみ働きます。

#### `make-directory filename` 〔手続き＋〕

`filename` という新しいディレクトリを作ります。`filename` がすでに存在するか、ディレクトリ
を作れなければエラーを通知します。

#### `delete-directory filename` 〔手続き＋〕

`filename` という名前のディレクトリを削除します。ディレクトリが存在しない、ディレクトリで
ない、またはファイルや下位ディレクトリを含めばエラーを通知します。

#### `->truename filename` 〔手続き＋〕

この手続きは、ファイルシステムの中で `filename` に結びついたファイルの「真の名前」を見つけて
返そうとします。適切なファイルがファイルシステムの中で見つけられなければ、
`condition-type:file-operation-error` 型のエラーが通知されます。

#### `call-with-temporary-file-pathname procedure` 〔手続き＋〕

`temporary-file-pathname` を呼んで一時ファイルを作り、それからそのファイルを指すパス名を
1つの引数として `procedure` を呼びます。`procedure` が返ると、一時ファイルがまだ存在すれば、
それが削除されます。それから、`procedure` が生んだ値が返されます。`procedure` がその継続
から脱出し、ファイルがまだ存在すれば、それが削除されます。

#### `temporary-file-pathname [directory]` 〔手続き＋〕

新しい空の一時ファイルを作り、それを指すパス名を返します。一時ファイルは Scheme の既定の
許可で作られるので、まれな状況を除いてエラーなく入力・出力のために開けます。一時ファイルは
明示的に削除されるまで存在しつづけます。Scheme プロセスが終了するときにファイルがまだ存在
すれば、それは削除されます。

`directory` が指定されれば、一時ファイルはそこに格納されます。指定されないか `#f` なら、
一時ファイルは `temporary-directory-pathname` が返すディレクトリに格納されます。

#### `temporary-directory-pathname` 〔手続き＋〕

一時ファイルを格納するのに使える、存在するディレクトリのパス名を返します。書き込み可能な
ディレクトリが見つかるまで、次のディレクトリ名が順に試されます。

- 環境変数 `TMPDIR`、`TEMP`、`TMP` が指定するディレクトリ。
- Unix では、ディレクトリ `/var/tmp`、`/usr/tmp`、`/tmp`。
- OS/2 または Windows では、システムドライブ上の次のディレクトリ。`\temp`、`\tmp`、`\`。
- OS/2 または Windows では、`*default-pathname-defaults*` が指定する現在のディレクトリ。

#### `file-directory? filename` 〔手続き＋〕

`filename` という名前のファイルが存在し、ディレクトリなら `#t` を返します。そうでなければ
`#f` を返します。シンボリックリンクをサポートするオペレーティングシステムで、`filename` が
シンボリックリンクを名指せば、これはリンク自体ではなくリンク先のファイルを調べます。次と
等価です。

```scheme
(eq? 'directory (file-type-indirect filename))
```

#### `file-regular? filename` 〔手続き＋〕

`filename` という名前のファイルが存在し、通常ファイル（すなわちディレクトリ、シンボリック
リンク、デバイスファイルなどでない）なら `#t` を返します。そうでなければ `#f` を返します。
シンボリックリンクをサポートするオペレーティングシステムで、`filename` がシンボリックリンク
を名指せば、これはリンク自体ではなくリンク先のファイルを調べます。次と等価です。

```scheme
(eq? 'regular (file-type-indirect filename))
```

#### `file-symbolic-link? filename` 〔手続き＋〕

シンボリックリンクをサポートするオペレーティングシステムで、`filename` という名前のファイル
が存在しシンボリックリンクなら、この手続きはシンボリックリンクの内容を、新しく割り当てられた
文字列として返します。返される値はシンボリックリンクが指すファイルの名前で、`filename` の
ディレクトリに対する相対と解釈されなければなりません。`filename` が存在しないかシンボリック
リンクでない場合、またはオペレーティングシステムがシンボリックリンクをサポートしない場合、
この手続きは `#f` を返します。

#### `file-type-direct filename` 〔手続き＋〕
#### `file-type-indirect filename` 〔手続き＋〕

`filename` という名前のファイルが存在すれば、`file-type-direct` はそれがどんな型のファイル
かを指定するシンボルを返します。たとえば、`filename` がディレクトリを指せば、シンボル
`directory` が返されます。`filename` が存在するファイルを指さなければ、`#f` が返されます。

`filename` がシンボリックリンクを指せば、`file-type-direct` はリンク自体の型を返し、
`file-type-indirect` はリンク先のファイルの型を返します。

現時点で返されうるシンボルは次のとおりです。名前は見て意味がわかるようにしてあります。これ
らの名前のほとんどは特定のオペレーティングシステムでしか返されえないので、オペレーティング
システムの名前が前に付いています。

```text
regular
directory
unix-symbolic-link
unix-character-device
unix-block-device
unix-named-pipe
unix-socket
os2-named-pipe
win32-named-pipe
```

#### `file-readable? filename` 〔手続き＋〕

`filename` が入力のために開けるファイル、すなわち読み込み可能なファイルを名指せば `#t` を
返します。そうでなければ `#f` を返します。

#### `file-writeable? filename` 〔手続き＋〕

`filename` が出力のために開けるファイル、すなわち書き込み可能なファイルを名指せば `#t` を
返します。そうでなければ `#f` を返します。

#### `file-executable? filename` 〔手続き＋〕

`filename` が実行できるファイルを名指せば `#t` を返します。そうでなければ `#f` を返します。
Unix では、実行可能ファイルはそのモードビットで識別されます。OS/2 では、実行可能ファイルは
ファイル拡張子 `.exe`、`.com`、`.cmd`、`.bat` のいずれかを持ちます。Windows では、実行可能
ファイルはファイル拡張子 `.exe`、`.com`、`.bat` のいずれかを持ちます。

#### `file-access filename mode` 〔手続き＋〕

`mode` は 0 以上 7 以下の正確な整数でなければなりません。これはビットごとに符号化された
述語の選択子で、1 が「実行可能」、2 が「書き込み可能」、4 が「読み込み可能」を意味します。
`file-access` は、`filename` が存在し、`mode` が選ぶ述語を満たせば `#t` を返します。たと
えば `mode` が 5 なら、`filename` は読み込み可能かつ実行可能でなければなりません。`filename`
が存在しないか、選ばれた述語を満たさなければ、`#f` が返されます。

#### `file-eq? filename1 filename2` 〔手続き＋〕

`filename1` と `filename2` が同じファイルを指すかどうかを判定します。Unix では、これは2つの
ファイルの inode とデバイスを比較して行われます。OS/2 と Windows では、これはファイル名の
文字列を比較して行われます。

#### `file-modes filename` 〔手続き＋〕

`filename` が存在するファイルを名指せば、`file-modes` はファイルの許可を符号化する正確な
非負整数を返します。この整数の符号化はオペレーティングシステム依存です。Unix では、`struct
stat` 構造の `st_mode` 要素の最下位12ビットです。OS/2 と Windows では、下で説明するファイル
属性ビットです。`filename` が存在するファイルを名指さなければ、`#f` が返されます。

#### `set-file-modes! filename modes` 〔手続き＋〕

`filename` は存在するファイルを名指さなければなりません。`modes` は `file-modes` の呼び出し
が返しえた正確な非負整数でなければなりません。`set-file-modes!` はファイルの許可を `modes`
が符号化するものに書き換えます。

#### `os2-file-mode/read-only` 〔変数＋〕
#### `os2-file-mode/hidden` 〔変数＋〕
#### `os2-file-mode/system` 〔変数＋〕
#### `os2-file-mode/directory` 〔変数＋〕
#### `os2-file-mode/archived` 〔変数＋〕

これらの変数の値は、OS/2 で `file-modes` が返す値を構成する「モードビット」です。これらの
ビットは小さい整数で、足し合わせて完全なモードの集合を作れます。整数 0 は、これらのビットの
どれも立っていないモードの集合を表します。

#### `nt-file-mode/read-only` 〔変数＋〕
#### `nt-file-mode/hidden` 〔変数＋〕
#### `nt-file-mode/system` 〔変数＋〕
#### `nt-file-mode/directory` 〔変数＋〕
#### `nt-file-mode/archive` 〔変数＋〕
#### `nt-file-mode/normal` 〔変数＋〕
#### `nt-file-mode/temporary` 〔変数＋〕
#### `nt-file-mode/compressed` 〔変数＋〕

これらの変数の値は、Windows で `file-modes` が返す値を構成する「モードビット」です。これ
らのビットは小さい整数で、足し合わせて完全なモードの集合を作れます。整数 0 は、これらの
ビットのどれも立っていないモードの集合を表します。

#### `file-modification-time filename` 〔手続き＋〕

`filename` の変更時刻を正確な非負整数として返します。結果は、ふつうの整数の算術を使って他の
ファイル時刻と比較できます。`filename` が存在しないファイルを名指せば、`file-modification-time`
は `#f` を返します。

シンボリックリンクをサポートするオペレーティングシステムで、`filename` がシンボリックリンク
を名指せば、`file-modification-time` はリンク先のファイルの変更時刻を返します。別の手続き
`file-modification-time-direct` はリンク自体の変更時刻を返します。他のすべての点で
`file-modification-time` と同一です。対称性のため、`file-modification-time-indirect` は
`file-modification-time` の同義語です。

#### `file-access-time filename` 〔手続き＋〕

`filename` のアクセス時刻を正確な非負整数として返します。結果は、ふつうの整数の算術を使って
他のファイル時刻と比較できます。`filename` が存在しないファイルを名指せば、`file-access-time`
は `#f` を返します。

シンボリックリンクをサポートするオペレーティングシステムで、`filename` がシンボリックリンク
を名指せば、`file-access-time` はリンク先のファイルのアクセス時刻を返します。別の手続き
`file-access-time-direct` はリンク自体のアクセス時刻を返します。他のすべての点で
`file-access-time` と同一です。対称性のため、`file-access-time-indirect` は
`file-access-time` の同義語です。

#### `set-file-times! filename access-time modification-time` 〔手続き＋〕

`filename` は存在するファイルを名指さなければならず、`access-time` と `modification-time`
はそれぞれ `file-access-time` と `file-modification-time` が返しえた妥当なファイル時刻で
なければなりません。`set-file-times!` は、`filename` が指定するファイルのアクセス時刻と
変更時刻を、それぞれ `access-time` と `modification-time` が与える値に変えます。便宜のため、
どちらの時刻引数も `#f` と指定できます。この場合、対応する時刻は変えられません。
`set-file-times!` は未規定の値を返します。

#### `current-file-time` 〔手続き＋〕

現在の時刻を、上のファイル時刻の手続きが使うのと同じ形式で、正確な非負整数として返します。
この数は、ふつうの算術演算を使って他のファイル時刻と比較できます。

#### `file-touch filename` 〔手続き＋〕

`filename` という名前のファイルをタッチします。ファイルがすでに存在すれば、その変更時刻が
現在のファイル時刻に設定され、`#f` が返されます。そうでなければ、ファイルが作られ、`#t` が
返されます。これは不可分なテストアンドセット演算なので、同期の仕組みとして役立ちます。

#### `file-length filename` 〔手続き＋〕

`filename` という名前のファイルの長さを、バイト単位で、正確な非負整数として返します。

#### `file-attributes filename` 〔手続き＋〕

この手続きは、`filename` という名前のファイルが存在するかどうかを判定し、存在すればそれに
ついての情報を返します。ファイルが存在しなければ `#f` を返します。

シンボリックリンクをサポートするオペレーティングシステムで、`filename` がシンボリックリンク
を名指せば、`file-attributes` はリンク自体の属性を返します。別の手続き
`file-attributes-indirect` はリンク先のファイルの属性を返します。他のすべての点で
`file-attributes` と同一です。対称性のため、`file-attributes-direct` は `file-attributes`
の同義語です。

`file-attributes` が返す情報は、アクセサ手続きで復号されます。次のアクセサはすべての
オペレーティングシステムで定義されます。

#### `file-attributes/type attributes` 〔手続き＋〕

ファイルの型。ファイルがディレクトリなら `#t`、シンボリックリンクなら文字列（リンク先の
名前）、他のすべての型のファイルなら `#f`。

#### `file-attributes/access-time attributes` 〔手続き＋〕

ファイルの最終アクセス時刻、正確な非負整数。

#### `file-attributes/modification-time attributes` 〔手続き＋〕

ファイルの最終変更時刻、正確な非負整数。

#### `file-attributes/change-time attributes` 〔手続き＋〕

ファイルの最終変化時刻、正確な非負整数。

#### `file-attributes/length attributes` 〔手続き＋〕

ファイルの長さ、バイト単位。

#### `file-attributes/mode-string attributes` 〔手続き＋〕

ファイルのモード文字列、ファイルのモードビットを示す新しく割り当てられた文字列。Unix では、
この文字列は Unix 形式です。OS/2 と Windows では、この文字列は標準の「DOS」属性をそのふつう
の形式で示します。

#### `file-attributes/n-links attributes` 〔手続き＋〕

ファイルへのリンクの数、正確な正整数。Windows と OS/2 では、これはつねに 1 です。

次の追加のアクセサは Unix で定義されます。

#### `file-attributes/uid attributes` 〔手続き＋〕

ファイルの所有者のユーザ id、正確な非負整数。

#### `file-attributes/gid attributes` 〔手続き＋〕

ファイルのグループのグループ id、正確な非負整数。

#### `file-attributes/inode-number attributes` 〔手続き＋〕

ファイルの inode 番号、正確な非負整数。

次の追加のアクセサは OS/2 と Windows で定義されます。

#### `file-attributes/modes attributes` 〔手続き＋〕

ファイルの属性ビット。これは、オペレーティングシステムの API が指定するとおりのファイルの
属性ビットを含む、正確な非負整数です。

次の追加のアクセサは OS/2 で定義されます。

#### `file-attributes/allocated-length attributes` 〔手続き＋〕

ファイルの割り当てられた長さ。固定長の割り当て単位のために、ファイルの長さより大きくなり
えます。

## 15.4 ディレクトリの読み手

#### `directory-read directory [sort?]` 〔手続き＋〕

`directory` は `->pathname` でパス名に変換できるオブジェクトでなければなりません。`directory`
が指定するディレクトリが読まれ、ディレクトリの内容が、絶対パス名の新しく割り当てられた
リストとして返されます。結果は、`sort?` が `#f` と指定されないかぎり、ディレクトリのふつう
のソートの慣習に従ってソートされます。`directory` が name、type、version 成分を持てば、返さ
れるリストは、name、type、version 成分が `directory` のものに一致するパス名だけを含みます。
これらの成分の1つとしての `wild` や `#f` は「何にでも一致」を意味します。

OS/2 と Windows の実装は「グロブ（globbing）」をサポートします。文字 `*` と `?` がそれぞれ
「何にでも一致」と「任意の文字に一致」を意味すると解釈されます。この「グロブ」は `directory`
のファイル部分でのみサポートされます。

## 15.5 日付と時刻

MIT Scheme は、日付と時刻の情報を操作する単純な手続きの集合を提供します。4つの時刻表現が
あり、それぞれ異なる目的に役立ちます。各表現は他のどれにも変換できます。

主要な時刻表現である**協定時刻（universal time）**は、1900年1月1日 UTC の真夜中から経過した
秒数を数える正確な非負整数です。（UTC は Coordinated Universal Time の略で、グリニッジ標準
時の現代的な名前です。）この形式は `get-universal-time` と `decoded-time->universal-time`
が生みます。

2番目の表現である**分解時刻（decoded time）**は、時刻が月・分などの構成部分に分解された
レコード構造です。分解時刻はつねに特定の時間帯に対する相対で、時間帯は構造の構成部分です。
この形式は `global-decoded-time` と `local-decoded-time` が生みます。

3番目の表現である**ファイル時刻（file time）**は、時刻が増えるほど大きくなる正確な非負整数
です。協定時刻と違って、この表現はオペレーティングシステム依存です。この形式は、
`file-modification-time` や `file-attributes` のような、すべてのファイル属性の手続きが生み
ます。

4番目の表現である**時刻文字列（time string）**は、時刻の外部表現です。この形式は RFC-822
（Standard for the format of ARPA Internet text messages）が定めますが、年が2桁の数ではなく
4桁の数として表される変更を加えています。この形式は、インターネットのメールと他の数多くの
ネットワークプロトコルの標準的な形式です。

この節では、`universal-time`、`decoded-time`、`file-time`、`time-string` という名前の引数
変数は、それぞれ対応する形式であることが要求されます。

### 15.5.1 協定時刻

#### `get-universal-time` 〔手続き＋〕

現在の時刻を協定形式で返します。

```scheme
(get-universal-time) ⇒ 3131453078
```

#### `epoch` 〔変数＋〕

`epoch` は、1970年1月1日 UTC の真夜中を協定時刻形式で表したものです。

```scheme
epoch ⇒ 2208988800
```

### 15.5.2 分解時刻

秒や分のような標準の時刻の構成部分を表すオブジェクトは、正確な非負整数であることが要求され
ます。秒と分は 0 以上 59 以下、時は 0 以上 23 以下、日は 1 以上 31 以下、月は 1 以上 12
以下でなければなりません。年は「4桁」形式で表され、1999年は 99 ではなく 1999 と表されます。

#### `local-decoded-time` 〔手続き＋〕

現在の時刻を分解形式で返します。分解時刻はローカルの時間帯で表されます。

```scheme
(pp (local-decoded-time))
-| #[decoded-time 76]
-| (second 2)
-| (minute 12)
-| (hour 11)
-| (day 27)
-| (month 4)
-| (year 1999)
-| (day-of-week 1)
-| (daylight-savings-time 1)
-| (zone 5)
```

#### `global-decoded-time` 〔手続き＋〕

現在の時刻を分解形式で返します。分解時刻は UTC で表されます。

```scheme
(pp (global-decoded-time))
-| #[decoded-time 77]
-| (second 8)
-| (minute 12)
-| (hour 15)
-| (day 27)
-| (month 4)
-| (year 1999)
-| (day-of-week 1)
-| (daylight-savings-time 0)
-| (zone 0)
```

#### `make-decoded-time second minute hour day month year [zone]` 〔手続き＋〕

与えられた時刻を表す新しい分解時刻オブジェクトを返します。引数は上の規則に従って妥当な
構成部分でなければならず、妥当な日付をなさなければなりません。

`zone` が与えられないか `#f` なら、結果の分解時刻はローカルの時間帯で表されます。そうでなけ
れば、`zone` は妥当な時間帯でなければならず、結果はその時間帯で表されます。

警告: この手続きはオペレーティングシステムのランタイムライブラリに依存するので、すべての
日付を表せるわけではありません。とくに、ほとんどの Unix システムでは、1970年1月1日 UTC の
真夜中より前に起こる日付を符号化できません。これをしようとするとエラーを通知します。

```scheme
(pp (make-decoded-time 0 9 11 26 3 1999))
-| #[decoded-time 19]
-| (second 0)
-| (minute 9)
-| (hour 11)
-| (day 26)
-| (month 3)
-| (year 1999)
-| (day-of-week 4)
-| (daylight-savings-time 0)
-| (zone 5)
(pp (make-decoded-time 0 9 11 26 3 1999 3))
-| #[decoded-time 80]
-| (second 0)
-| (minute 9)
-| (hour 11)
-| (day 26)
-| (month 3)
-| (year 1999)
-| (day-of-week 4)
-| (daylight-savings-time 0)
-| (zone 3)
```

#### `decoded-time/second decoded-time` 〔手続き＋〕
#### `decoded-time/minute decoded-time` 〔手続き＋〕
#### `decoded-time/hour decoded-time` 〔手続き＋〕
#### `decoded-time/day decoded-time` 〔手続き＋〕
#### `decoded-time/month decoded-time` 〔手続き＋〕
#### `decoded-time/year decoded-time` 〔手続き＋〕

`decoded-time` の対応する構成部分を返します。

```scheme
(decoded-time/second (local-decoded-time)) ⇒ 17
(decoded-time/year (local-decoded-time)) ⇒ 1999
(decoded-time/day (local-decoded-time)) ⇒ 26
```

#### `decoded-time/day-of-week decoded-time` 〔手続き＋〕

`decoded-time` が当たる曜日を、0（月曜）以上 6（日曜）以下の正確な整数として符号化して返し
ます。

```scheme
(decoded-time/day-of-week (local-decoded-time)) ⇒ 4
```

#### `decoded-time/daylight-savings-time? decoded-time` 〔手続き＋〕

`decoded-time` が夏時間を使って表されていれば `#t` を返します。そうでなければ `#f` を返し
ます。

```scheme
(decoded-time/daylight-savings-time? (local-decoded-time))
                  ⇒ #f
```

#### `decoded-time/zone decoded-time` 〔手続き＋〕

`decoded-time` が表される時間帯を返します。これは -24 以上 +24 以下の正確な有理数で、3600
を掛けると整数になります。値は UTC から西へ何時間かの数です。

```scheme
(decoded-time/zone (local-decoded-time)) ⇒ 5
```

#### `time-zone? object` 〔手続き＋〕

`object` が -24 以上 +24 以下の正確な数で、3600 を掛けると整数になるなら `#t` を返します。

```scheme
(time-zone? -5)   ⇒ #t
(time-zone? 11/2) ⇒ #t
(time-zone? 11/7) ⇒ #f
```

#### `month/max-days month` 〔手続き＋〕

`month` にありうる最大の日数を返します。`month` は 1 以上 12 以下の正確な整数でなければ
なりません。

```scheme
(month/max-days 2) ⇒ 29
(month/max-days 3) ⇒ 31
(month/max-days 4) ⇒ 30
```

### 15.5.3 ファイル時刻

上で述べたように、ファイル時刻はオペレーティングシステム依存です。この執筆時点で、2つの
形式が使われています。Unix と Windows のシステムでは、ファイル時刻は 1970年1月1日 UTC の
真夜中からの秒数です（標準の Unix 時刻の慣習）。

OS/2 はファイル時刻を32ビットの符号なし整数として表し、時刻の構成部分が符号なしのビット
フィールドに分解されます。構成部分はつねにローカル時刻で述べられます。フィールドは、MSB
から LSB へ次のとおりです。

- 1900年に対する相対の年を表す7ビット。
- 1 から 12 まで番号を付けた月を表す4ビット。
- 1 から 31 まで番号を付けた月の日を表す5ビット。
- 0 から 23 まで番号を付けた日の時を表す5ビット。
- 0 から 59 まで番号を付けた分を表す6ビット。
- 秒を表す5ビット。このフィールドは、2秒単位で数える点で変わっており、0 から 29 までの数で、
  0 から 58 に対応する秒数を表します。

次の手続きは、結果をファイル時刻形式で生成します。

```text
file-access-time
file-access-time-direct
file-access-time-indirect
file-modification-time
file-modification-time-direct
file-modification-time-indirect
file-attributes/access-time
file-attributes/modification-time
file-attributes/change-time
```

加えて、`set-file-times!` は時刻引数をファイル時刻形式で受け取ります。

### 15.5.4 時刻形式の変換

この節で説明する手続きは、時刻をある形式から別の形式へ変換します。

#### `universal-time->local-decoded-time universal-time` 〔手続き＋〕
#### `universal-time->global-decoded-time universal-time` 〔手続き＋〕

協定時刻形式の引数を分解時刻形式に変換します。結果はそれぞれローカルの時間帯または UTC
です。

```scheme
(pp (universal-time->local-decoded-time (get-universal-time)))
-| #[decoded-time 21]
-| (second 23)
-| (minute 57)
-| (hour 17)
-| (day 29)
-| (month 4)
-| (year 1999)
-| (day-of-week 3)
-| (daylight-savings-time 1)
-| (zone 5)
(pp (universal-time->global-decoded-time
     (get-universal-time)))
-| #[decoded-time 22]
-| (second 27)
-| (minute 57)
-| (hour 21)
-| (day 29)
-| (month 4)
-| (year 1999)
-| (day-of-week 3)
-| (daylight-savings-time 0)
-| (zone 0)
```

#### `universal-time->file-time universal-time` 〔手続き＋〕

協定時刻形式の引数をファイル時刻形式に変換します。

```scheme
(universal-time->file-time (get-universal-time))
     ⇒ 925422988
```

#### `universal-time->local-time-string universal-time` 〔手続き＋〕
#### `universal-time->global-time-string universal-time` 〔手続き＋〕

協定時刻形式の引数を時刻文字列に変換します。結果はそれぞれローカルの時間帯または UTC です。

```scheme
(universal-time->local-time-string (get-universal-time))
     ⇒ "Thu, 29 Apr 1999 17:55:31 -0400"
(universal-time->global-time-string (get-universal-time))
     ⇒ "Thu, 29 Apr 1999 21:55:51 +0000"
```

#### `decoded-time->universal-time decoded-time` 〔手続き＋〕

分解時刻形式の引数を協定時刻形式に変換します。

```scheme
(decoded-time->universal-time (local-decoded-time))
     ⇒ 3134411942
(decoded-time->universal-time (global-decoded-time))
     ⇒ 3134411947
```

#### `decoded-time->file-time decoded-time` 〔手続き＋〕

分解時刻形式の引数をファイル時刻形式に変換します。

```scheme
(decoded-time->file-time (local-decoded-time))
     ⇒ 925423191
(decoded-time->file-time (global-decoded-time))
     ⇒ 925423195
```

#### `decoded-time->string decoded-time` 〔手続き＋〕

分解時刻形式の引数を時刻文字列に変換します。

```scheme
(decoded-time->string (local-decoded-time))
     ⇒ "Thu, 29 Apr 1999 18:00:43 -0400"
(decoded-time->string (global-decoded-time))
     ⇒ "Thu, 29 Apr 1999 22:00:46 +0000"
```

#### `file-time->universal-time file-time` 〔手続き＋〕

ファイル時刻形式の引数を協定時刻形式に変換します。

```scheme
(file-time->universal-time (file-modification-time "/"))
     ⇒ 3133891907
```

#### `file-time->local-decoded-time file-time` 〔手続き＋〕
#### `file-time->global-decoded-time file-time` 〔手続き＋〕

ファイル時刻形式の引数を分解時刻形式に変換します。結果はそれぞれローカルの時間帯または
UTC です。

```scheme
(pp (file-time->local-decoded-time
     (file-modification-time "/")))
-| #[decoded-time 26]
-| (second 47)
-| (minute 31)
-| (hour 17)
-| (day 23)
-| (month 4)
-| (year 1999)
-| (day-of-week 4)
-| (daylight-savings-time 1)
-| (zone 5)
(pp (file-time->global-decoded-time
     (file-modification-time "/")))
-| #[decoded-time 27]
-| (second 47)
-| (minute 31)
-| (hour 21)
-| (day 23)
-| (month 4)
-| (year 1999)
-| (day-of-week 4)
-| (daylight-savings-time 0)
-| (zone 0)
```

#### `file-time->local-time-string file-time` 〔手続き＋〕
#### `file-time->global-time-string file-time` 〔手続き＋〕

ファイル時刻形式の引数を時刻文字列に変換します。結果はそれぞれローカルの時間帯または UTC
です。

```scheme
(file-time->local-time-string (file-modification-time "/"))
     ⇒ "Fri, 23 Apr 1999 17:31:47 -0400"
(file-time->global-time-string (file-modification-time "/"))
     ⇒ "Fri, 23 Apr 1999 21:31:47 +0000"
```

#### `string->universal-time time-string` 〔手続き＋〕

時刻文字列の引数を協定時刻形式に変換します。

```scheme
(string->universal-time "Fri, 23 Apr 1999 21:31:47 +0000")
     ⇒ 3133888307
(string->universal-time "Fri, 23 Apr 1999 17:31:47 -0400")
     ⇒ 3133888307
```

#### `string->decoded-time time-string` 〔手続き＋〕

時刻文字列の引数を分解時刻形式に変換します。

```scheme
(pp (string->decoded-time "Fri, 23 Apr 1999 17:31:47 -0400"))
-| #[decoded-time 30]
-| (second 47)
-| (minute 31)
-| (hour 17)
-| (day 23)
-| (month 4)
-| (year 1999)
-| (day-of-week 4)
-| (daylight-savings-time 0)
-| (zone 4)
```

#### `string->file-time time-string` 〔手続き＋〕

時刻文字列の引数をファイル時刻形式に変換します。

```scheme
(string->file-time "Fri, 23 Apr 1999 17:31:47 -0400")
     ⇒ 924899507
```

### 15.5.5 時刻の外部表現

時刻のふつうの外部表現は、上で説明した時刻文字列です。この節の手続きは、より冗長で、人間の
読み手への提示によりふさわしいかもしれない、時刻の別の外部表現を生成します。

#### `decoded-time/date-string decoded-time` 〔手続き＋〕
#### `decoded-time/time-string decoded-time` 〔手続き＋〕

これらの手続きは、`decoded-time` が表す日付と時刻の外部表現をそれぞれ含む文字列を返します。
結果は暗黙にローカル時刻です。

```scheme
(decoded-time/date-string (local-decoded-time))
     ⇒ "Tuesday March 30, 1999"
(decoded-time/time-string (local-decoded-time))
     ⇒ "11:22:38 AM"
```

#### `day-of-week/long-string day-of-week` 〔手続き＋〕
#### `day-of-week/short-string day-of-week` 〔手続き＋〕

与えられた `day-of-week` を表す文字列を返します。引数は 0 以上 6 以下の正確な非負整数で
なければなりません。`day-of-week/long-string` は曜日の名前を完全に綴った長い文字列を返し
ます。`day-of-week/short-string` は曜日を3文字に略した短い文字列を返します。

```scheme
(day-of-week/long-string 0) ⇒ "Monday"
(day-of-week/short-string 0) ⇒ "Mon"
(day-of-week/short-string 3) ⇒ "Thu"
```

#### `month/long-string month` 〔手続き＋〕
#### `month/short-string month` 〔手続き＋〕

与えられた `month` を表す文字列を返します。引数は 1 以上 12 以下の正確な非負整数でなければ
なりません。`month/long-string` は月の名前を完全に綴った長い文字列を返します。
`month/short-string` は月を3文字に略した短い文字列を返します。

```scheme
(month/long-string 1)         ⇒ "January"
(month/short-string 1) ⇒ "Jan"
(month/short-string 10) ⇒ "Oct"
```

#### `time-zone->string` 〔手続き＋〕

与えられた時間帯に対応する文字列を返します。この文字列は、RFC-822 の時刻文字列を生成する
のに使われるのと同じ文字列です。

```scheme
(time-zone->string 5)         ⇒ "-0500"
(time-zone->string -4)        ⇒ "+0400"
(time-zone->string 11/2) ⇒ "-0530"
```

## 15.6 機械時刻

前の節は時計の時刻を操作する手続きを扱いました。この節では、計算機の時間、すなわち経過した
CPU 時間、経過した実時間などを扱う手続きを説明します。これらの手続きは、コードの実行に
かかる時間の量を測るのに役立ちます。

この節の手続きのいくつかは、**ティック（ticks）**と呼ばれる時間表現を操作します。ティックは
ここでは規定されない時間の単位ですが、提供される手続きで秒に、また秒からに変換できます。
ティックの数は正確な整数として表されます。現在、各ティックは 1 ミリ秒ですが、将来変わる
かもしれません。

#### `process-time-clock` 〔手続き＋〕

Scheme が起動されてから経過したプロセス時間を、ティック単位で返します。プロセス時間は
オペレーティングシステムが測るもので、Scheme プロセスが計算しているあいだの時間です。
システムコールの時間は含みませんが、オペレーティングシステムによってはサブプロセスが使った
時間を含むかもしれません。

```scheme
(process-time-clock) ⇒ 21290
```

#### `real-time-clock` 〔手続き＋〕

Scheme が起動されてから経過した実時間を、ティック単位で返します。実時間はふつうの時計が
測る時間です。

```scheme
(real-time-clock) ⇒ 33474836
```

#### `internal-time/ticks->seconds ticks` 〔手続き＋〕

`ticks` に対応する秒数を返します。結果はつねに実数です。

```scheme
(internal-time/ticks->seconds 21290) ⇒ 21.29
(internal-time/ticks->seconds 33474836) ⇒ 33474.836
```

#### `internal-time/seconds->ticks seconds` 〔手続き＋〕

`seconds` に対応するティックの数を返します。`seconds` は実数でなければなりません。

```scheme
(internal-time/seconds->ticks 20.88) ⇒ 20880
(internal-time/seconds->ticks 20.83) ⇒ 20830
```

#### `system-clock` 〔手続き＋〕

Scheme が起動されてから経過したプロセス時間を、秒単位で返します。おおよそ次と等価です。

```scheme
(internal-time/ticks->seconds (process-time-clock))
```

例:

```scheme
(system-clock) ⇒ 20.88
```

#### `runtime` 〔手続き＋〕

Scheme が起動されてから経過したプロセス時間を、秒単位で返します。ただし、ガベージコレクション
に費やされた時間は含みません。

```scheme
(runtime) ⇒ 20.83
```

#### `with-timings thunk receiver` 〔手続き＋〕

`thunk` を引数なしで呼びます。`thunk` が返ったあと、`receiver` が、`thunk` を計算するあいだに
費やされた時間を記述する3つの引数で呼ばれます。経過した実行時間、ガベージコレクタで費やされた
時間の量、経過した実時間です。3つの時間はすべてティック単位です。

この手続きは性能測定をするのにもっとも役立ち、比較的低いオーバーヘッドを持つよう設計されて
います。

```scheme
(with-timings
 (lambda () ...込み入った計算...)
 (lambda (run-time gc-time real-time)
   (write (internal-time/ticks->seconds run-time))
   (write-char #\space)
   (write (internal-time/ticks->seconds gc-time))
   (write-char #\space)
   (write (internal-time/ticks->seconds real-time))
   (newline)))
```

#### `measure-interval runtime? procedure` 〔手続き＋〕

`procedure` を、現在のプロセス時間を秒単位で引数として渡して呼びます。この呼び出しの結果は
別の手続きでなければなりません。`procedure` が返ると、結果の手続きが、終了時刻を秒単位で
引数として末尾再帰的に呼ばれます。`runtime?` が `#f` なら、経過時間が `runtime` が返す経過
システム時間から差し引かれます。

この手続きは時間測定に使えますが、そのインタフェースはその目的にはやや不格好です。かわりに
`with-timings` を使うことを勧めます。より便利で、より低いオーバーヘッドを持つからです。

```scheme
(measure-interval #t
                  (lambda (start-time)
                    (let ((v ...込み入った計算...))
                      (lambda (end-time)
                        (write (- end-time start-time))
                        (newline)
                        v))))
```

## 15.7 サブプロセス

MIT Scheme はサブプロセスを走らせて制御する能力を提供します。このサポートは2つの部分に
分かれます。基礎となるオペレーティングシステムのプロセス制御の基本手続きに写る低水準の
基本手続きの集合と、サブプロセスを起動して1回の呼び出しで完了まで走らせる高水準の手続きの
集合です。後者の形で走らせるサブプロセスは、Scheme の手続き呼び出しと同期して起動・停止
されるので、**同期的（synchronous）**と呼ばれます。

この章では、Scheme の高水準の同期的サブプロセスのサポートを記録します。低水準のサポートは
記録しませんが、ソースコードを読む気のある人には利用できます。

同期的サブプロセスのサポートは、実行時に読み込めるオプションです。使うには、呼ぶ前に一度、
次を実行します。

```scheme
(load-option 'synchronous-subprocess)
```

### 15.7.1 サブプロセスの手続き

Scheme のもとで同期的サブプロセスを走らせるコマンドが2つあります。`run-shell-command` は
使うのが非常に簡単で、すべてのシェルの機能へのアクセスを提供し、ほとんどの状況で好まれる
べきです。`run-synchronous-subprocess` は、プログラムの直接の実行と、プログラムに渡される
コマンドライン引数の正確な制御を許しますが、ファイルのグロブ、I/O のリダイレクト、その他の
シェルの機能を提供しません。

#### `run-shell-command command option …` 〔手続き＋〕

`command`（文字列でなければなりません）を走らせます。`command` は解釈のためにコマンドシェル
に渡されます。シェルがどう選ばれるかは下で詳しく述べます。

`option` は、任意のふるまいを指定するキーワードと値の対の列です。オプションについての詳しい
情報は下を見よ。

`run-shell-command` はサブプロセスが実行を完了するまで待ち、サブプロセスからの終了コードを
返します。サブプロセスが kill されるか停止すると、エラーが通知され、手続きは返りません。

#### `run-synchronous-subprocess program arguments option …` 〔手続き＋〕

`program` を、与えられたコマンドライン引数を渡して走らせます。`program` は、パス上のプログラム
の名前か、特定のプログラムへのパス名のどちらかでなければなりません。`arguments` は文字列の
リストでなければなりません。各文字列はプログラムへの1つのコマンドライン引数です。

`option` は、任意のふるまいを指定するキーワードと値の対の列です。オプションについての詳しい
情報は下を見よ。

`run-synchronous-subprocess` はサブプロセスが実行を完了するまで待ち、サブプロセスからの
終了コードを返します。サブプロセスが kill されるか停止すると、エラーが通知され、手続きは
返りません。

### 15.7.2 サブプロセスの条件

上の手続きが生んだサブプロセスが kill されるか中断されると、次のエラーのいずれかが通知され
ます。

#### `condition-type:subprocess-signalled subprocess reason` 〔条件型＋〕

この条件型は `condition-type:subprocess-abnormal-termination` の下位型です。サブプロセス
が kill されると通知されます。

`subprocess` は関わったサブプロセスを表すオブジェクトです。このオブジェクトの内部にはアクセス
できますが、インタフェースは現時点で記録されていません。詳細はソースコードを見よ。

`reason` は Unix システムでのみ興味深く、そこではプロセスを kill したシグナルです。他の
システムでは、役立つ情報を伝えない固定の値です。

#### `condition-type:subprocess-stopped subprocess reason` 〔条件型＋〕

この条件型は `condition-type:subprocess-abnormal-termination` の下位型です。サブプロセス
が停止または中断されると通知されます。

`subprocess` は関わったサブプロセスを表すオブジェクトです。このオブジェクトの内部にはアクセス
できますが、インタフェースは現時点で記録されていません。詳細はソースコードを見よ。

`reason` は Unix システムでのみ興味深く、そこではプロセスを停止したシグナルです。他の
システムでは、役立つ情報を伝えない固定の値です。

#### `condition-type:subprocess-abnormal-termination subprocess reason` 〔条件型＋〕

この条件型は `condition-type:error` の下位型です。これは決して通知されない抽象型です。条件
ハンドラをこれに束縛できるように提供されています。

### 15.7.3 サブプロセスのオプション

次のサブプロセスのオプションを `run-shell-command` や `run-synchronous-subprocess` に
渡せます。これらのオプションは、キーワードと値の対を交互に並べて渡します。たとえば、

```scheme
(run-shell-command "ls /"
                     'output my-output-port
                     'output-buffer-size 8192)
```

この例は、2つのオプション `output` と `output-buffer-size` を指定してシェルコマンドを走らせる
のを示しています。

#### `input port` 〔サブプロセスオプション＋〕

サブプロセスの標準入力を指定します。`port` は入力ポートでよく、この場合 `port` から文字が
読まれ、`port` がファイル終端に達するまでサブプロセスに与えられます。あるいは、`port` は `#f`
でよく、サブプロセスに標準入力がないことを示します。このオプションの既定値は `#f` です。

```scheme
(call-with-input-file "foo.in"
  (lambda (port)
    (run-shell-command "cat > /dev/null" 'input port)))
```

#### `input-line-translation line-ending` 〔サブプロセスオプション＋〕

サブプロセスに文字を書くときに行末をどう変換すべきかを指定します。`input` オプションが `#f`
なら無視されます。`line-ending` は、行末を指定する文字列か、オペレーティングシステムの標準
の行末を使うことを意味するシンボル `default` のどちらかでなければなりません。どちらの場合も、
入力ポートに書かれる改行文字は、書かれる前に指定された行末に変換されます。このオプションの
既定値は `default` です。

```scheme
(call-with-input-file "foo.in"
  (lambda (port)
     (run-shell-command "cat > /dev/null"
                             'input port
                             'input-line-translation "\r\n")))
```

#### `input-buffer-size n` 〔サブプロセスオプション＋〕

サブプロセスの標準入力の入力バッファの大きさを指定します。（これは Scheme 側のバッファで、
サブプロセス側で行われるバッファリングとは関係ありません。）`input` オプションが `#f` なら
無視されます。`n` は、バッファが保持できる文字数を指定する正確な正整数でなければなりません。
このオプションの既定値は 512 です。

```scheme
(call-with-input-file "foo.in"
  (lambda (port)
     (run-shell-command "cat > /dev/null"
                            'input port
                            'input-buffer-size 4096)))
```

#### `output port` 〔サブプロセスオプション＋〕

サブプロセスの標準出力と標準エラーを指定します。`port` は出力ポートでよく、この場合サブ
プロセスから文字が読まれ、サブプロセスが終わるまで `port` に与えられます。あるいは、`port`
は `#f` でよく、サブプロセスに標準出力も標準エラーもないことを示します。このオプションの
既定値は `(current-output-port)` の値です。

```scheme
(call-with-output-file "foo.out"
  (lambda (port)
    (run-shell-command "ls -la /etc" 'output port)))
```

#### `output-line-translation line-ending` 〔サブプロセスオプション＋〕

サブプロセスの標準出力から文字を読むときに行末をどう変換すべきかを指定します。`output`
オプションが `#f` なら無視されます。`line-ending` は、行末を指定する文字列か、オペレーティング
システムの標準の行末を使うことを意味するシンボル `default` のどちらかでなければなりません。
どちらの場合も、サブプロセスのポートから読まれる改行文字は指定された行末に変換されます。この
オプションの既定値は `default` です。

```scheme
(call-with-output-file "foo.out"
   (lambda (port)
     (run-shell-command "ls -la /etc"
                             'output port
                             'output-line-translation "\r\n")))
```

#### `output-buffer-size n` 〔サブプロセスオプション＋〕

サブプロセスの標準出力の出力バッファの大きさを指定します。（これは Scheme 側のバッファで、
サブプロセス側で行われるバッファリングとは関係ありません。）`output` オプションが `#f` なら
無視されます。`n` は、バッファが保持できる文字数を指定する正確な正整数でなければなりません。
このオプションの既定値は 512 です。

```scheme
(call-with-output-file "foo.out"
  (lambda (port)
     (run-shell-command "ls -la /etc"
                             'output port
                             'output-buffer-size 4096)))
```

#### `redisplay-hook thunk` 〔サブプロセスオプション＋〕

サブプロセスからの出力が使えるときに `thunk` を定期的に走らせることを指定します。`thunk` は
引数のない手続きか、フックが供給されないことを示す `#f` でなければなりません。このオプション
はおもに対話的なシステムに役立ちます。たとえば、Edwin テキストエディタは、あるサブプロセスを
走らせるときに出力バッファを更新するのにこれを使います。このオプションの既定値は `#f` です。

```scheme
(run-shell-command "ls -la /etc"
                        'redisplay-hook
                        (lambda ()
                          (update-buffer-contents buffer)))
```

#### `environment environment` 〔サブプロセスオプション＋〕

サブプロセスに使われる環境変数を指定します。`environment` は、文字列のベクタか、既定の環境
を示す `#f` のどちらかでなければなりません。文字列のベクタなら、各文字列は名前と値の対で
なければならず、名前と値は等号で区切られます。たとえば `"foo=bar"` です。値のない変数を
定義するには、`"foo="` のように値を省くだけです。

変数 `scheme-subprocess-environment` が既定のサブプロセスの環境に束縛されていることに注意
してください。このオプションの既定値は `#f` です。

```scheme
(run-shell-command "ls -la /etc"
                   'environment
                   (let* ((v scheme-subprocess-environment)
                          (n (vector-length v))
                          (v (vector-grow v (+ n 1))))
                     (vector-set! v n "TERM=none")
                     v))
```

#### `working-directory pathname` 〔サブプロセスオプション＋〕

サブプロセスが走る作業ディレクトリを指定します。このオプションの既定値は
`(working-directory-pathname)` です。

```scheme
(run-shell-command "ls -la" 'working-directory "/etc/")
```

#### `use-pty? boolean` 〔サブプロセスオプション＋〕

このオプションは Unix システムでのみ意味を持ちます。他のシステムでは無視されます。サブ
プロセスとの通信に pty デバイスを使うかどうかを指定します。真なら pty が使われ、そうで
なければパイプが使われます。このオプションの既定値は `#f` です。

```scheme
(run-shell-command "ls -la /etc" 'use-pty? #t)
```

#### `shell-file-name pathname` 〔サブプロセスオプション＋〕

`run-shell-command` に使うシェルプログラムを指定します。このオプションの既定値は
`(os/shell-file-name)` です。これは環境変数 `SHELL` の値です。`SHELL` が設定されていなければ、
値はオペレーティングシステム依存で次のとおりです。

- Unix システムでは `/bin/sh` が使われます。
- OS/2 システムでは環境変数 `COMSPEC` の値が使われ、それが設定されていなければ現在のパスの
  `cmd.exe` が使われます。
- Windows システムでは環境変数 `COMSPEC` の値が使われます。それが設定されていなければ、
  Windows NT では `cmd.exe`、Windows 9x では `command.com` が使われます。どちらの場合も、
  シェルはパスを探索して見つけられます。

```scheme
(run-shell-command "ls -la /etc"
                        'shell-file-name "/usr/local/bin/bash")
```

## 15.8 TCP ソケット

MIT Scheme は、プロセス間通信の仕組みである**ソケット（socket）**へのアクセスを提供します。
tcp/ip ネットワークを介してコンピュータ間で通信する tcp ストリームソケットがサポートされて
います。tcp ソケットはすべてのオペレーティングシステムでサポートされます。

tcp ソケットは2つの異なるインタフェースを持ちます。クライアントを実装するインタフェースと、
サーバを実装する別のインタフェースです。基本的なプロトコルは、サーバが待ち受けポートを設定
してクライアントからの接続を待つ、というものです。クライアントの実装のほうが単純なので、
まずそれを扱います。

ソケットの手続きは、`host-name` と `service` と呼ばれる2つの特別な引数を受け取ります。
`host-name` は文字列で、インターネットホストの名前でなければなりません。あなたのコンピュータ
のふつうの検索規則を使って調べられます。たとえば、あなたのホストが `foo.mit.edu` で
`host-name` が `"bar"` なら、`bar.mit.edu` を指定します。

`service` は接続するサービスを指定します。ネットワークに接続されたコンピュータは、ふつう
telnet や ftp のようないくつもの異なるサービスを提供します。各サービスは一意なポート番号に
結びついています。たとえば `"www"` サービスはポート 80 に結びついています。`service` 引数は
ポート番号を、文字列として、あるいは直接に正確な非負整数として指定します。ポート文字列は、
オペレーティングシステムが表を使って復号します。たとえば Unix では表は `/etc/services` に
あります。ふつうは番号ではなくポート文字列を使うでしょう。

#### `open-tcp-stream-socket host-name service [buffer-size [line-translation]]` 〔手続き＋〕

`open-tcp-stream-socket` は `host-name` が指定するホストへの接続を開きます。`host-name` は
あなたのコンピュータのふつうの検索規則を使って調べられます。接続は `service` が指定する
サービスへ確立されます。返される値は i/o ポートで、`read-char` や `write-char` のような
ふつうの Scheme の i/o 手続きを使って文字を読み書きできます。

`buffer-size` はポートが使う読み書きバッファの大きさを指定します。これが指定されないか `#f`
なら、バッファは 4096 バイトを保持します。

`line-translation` は、ソケットを読み書きするときに行末文字をどう変換するかを指定します。
これが指定されないか `#f` なら、行はほとんどのインターネットプロトコルの標準である cr-lf
で終えられます。そうでなければ、使う行末の文字列を指定する文字列でなければなりません。

接続を閉じたいときは、`close-port` を使うだけです。

例として、Web サーバへの接続を開く方法を挙げます。

```scheme
(open-tcp-stream-socket "web.mit.edu" "www")
```

次に、少し複雑な tcp サーバの設定を扱います。サーバを作るのは2部分の過程です。まず、サーバ
ソケットを開かなければなりません。これはオペレーティングシステムに、指定したポートでネット
ワークを待ち受けさせます。サーバソケットが開かれると、オペレーティングシステムはクライアント
がそのポートであなたのコンピュータに接続することを許します。

過程の2番目の段階で、接続を**受け入れ（accept）**ます。これはクライアントが始めた接続を完成
させ、クライアントと通信できるようにします。接続を受け入れてもサーバソケットには影響しま
せん。それは追加のクライアント接続を待ち受けつづけます。同じサーバソケットへの複数のクライアント
接続を同時に開けます。

#### `open-tcp-server-socket service [address]` 〔手続き＋〕

この手続きは、`service` への接続を待ち受けるサーバソケットを開きます。ソケットは閉じるまで
待ち受けつづけます。返される値はサーバソケットオブジェクトです。

別のプロセスがすでにそのサービスを待ち受けていればエラーが通知されます。加えて、番号が 1024
より小さいポートは多くのオペレーティングシステムで特権が要り、非特権のプロセスは使えません。
`service` がそのようなポートを指定し、あなたに管理者権限がなければ、エラーが通知されるかも
しれません。

省略可能引数 `address` は、ソケットが待ち受ける ip アドレスを指定します。この引数が与えられ
ないか `#f` として与えられれば、ソケットはこの機械のすべての ip アドレスで待ち受けます。
（これは `host-address-any` を呼んだ結果を渡すのと等価です。）

#### `tcp-server-connection-accept server-socket block? peer-address` 〔手続き＋〕

クライアントが `server-socket` に接続したかどうかを調べます。接続していれば、i/o ポートが
返されます。返されるポートは、`read-char` や `write-char` のようなふつうの Scheme の i/o
手続きを使って読み書きできます。

引数 `block?` は、呼び出しの時点でクライアントが接続していなければどうするかを言います。`#f`
なら、2つの `#f` の値でただちに返ることを言います。そうでなければ、呼び出しはクライアントが
接続するまで待ちます。

引数 `peer-address` は、`#f` か、`allocate-host-address` が割り当てた ip アドレスのどちらか
です。ip アドレスなら、そのアドレスは接続してくるクライアントのアドレスに書き換えられます。

この手続きが返すポートを閉じても `server-socket` には影響しないことに注意してください。それ
は呼び出しが開いた特定のクライアント接続を閉じるだけです。`server-socket` を閉じるには
`close-tcp-server-socket` を使います。

#### `close-tcp-server-socket server-socket` 〔手続き＋〕

サーバソケット `server-socket` を閉じます。オペレーティングシステムはそのサービスへの
ネットワーク接続の待ち受けをやめます。すでに受け入れられた `server-socket` へのクライアント
接続は影響を受けません。

## 15.9 その他の OS 機能

この節には、他のカテゴリに収まらないさまざまなオペレーティングシステムの機能が含まれます。

#### `microcode-id/operating-system` 〔変数＋〕
#### `microcode-id/operating-system-name` 〔変数＋〕

`microcode-id/operating-system` は、Scheme が走っているオペレーティングシステムの種類を
指定するシンボルに束縛されています。ありうる値は3つ、`unix`、`os/2`、`nt` です。

`microcode-id/operating-system-name` は `microcode-id/operating-system` と同じ名前を含む
文字列です。後者は前者をシンボルとしてインターンして作られます。

#### `microcode-id/operating-system-variant` 〔変数＋〕

この変数は、Scheme が走っているオペレーティングシステムの特定の変種を識別する文字列です。
ありうる値のいくつかを挙げます。

```text
"GNU/Linux"
"FreeBSD"
"HP-UX"
"SunOS"
"OS/2 2.1"
"OS/2 4.0"
"Microsoft Windows NT 4.0 (Build 1381; Service Pack 3)"
"Microsoft Windows 98 (Build 410)"
```

Windows システムでは、この文字列の接頭辞で照合し、`"Build"` の接尾辞を無視することを勧め
ます。これは、接尾辞がサービスパックや修正についての情報を含みうるのに対し、接頭辞は特定の
バージョンの Windows について一定だからです。

次のいくつかの手続きは、`"www.swiss.ai.mit.edu"` のようなインターネットホスト名と、
`18.23.0.16` のような ip アドレスとのあいだの連想を保つドメインネームサービス（dns）への
アクセスを提供します。MIT Scheme では、インターネットホスト名を文字列として、ip アドレスを
長さ 4 のバイトベクタ（バイトベクタは、`string-ref` ではなく `vector-8b-ref` を使って
アクセスされる文字列にすぎません）として表します。ip アドレスのバイトは、書き出されるときと
同じ順で読まれます。

```scheme
(get-host-by-name "www.swiss") ⇒ #("\022\027\000\020")
```

#### `get-host-by-name host-name` 〔手続き＋〕

インターネットホスト名 `host-name` を dns を使って調べ、対応するホストの ip アドレスのベクタ
を返します。そのようなホストがなければ `#f` を返します。ふつう返されるベクタは要素を1つしか
持ちませんが、ホストが複数のネットワークインタフェースを持てば、ベクタは複数の要素を持つ
かもしれません。

```scheme
(get-host-by-name "www.swiss") ⇒ #("\022\027\000\020")
```

#### `get-host-by-address ip-address` 〔手続き＋〕

`ip-address` に対して逆 dns 検索を行い、そのアドレスに対応するインターネットホスト名を返し
ます。そのようなホストがなければ `#f` を返します。

```scheme
(get-host-by-address "\022\027\000\020") ⇒ "swissnet.ai.mit.edu"
```

#### `canonical-host-name host-name` 〔手続き＋〕

`host-name` の「正準」インターネットホスト名を見つけます。たとえば、

```scheme
(canonical-host-name "zurich")          ⇒ "zurich.ai.mit.edu"
(canonical-host-name "www.swiss") ⇒ "swissnet.ai.mit.edu"
```

どちらの例でも、既定のインターネットドメイン `ai.mit.edu` が `host-name` に加えられます。
2番目の例では、`"www.swiss"` は `"swissnet"` という別のコンピュータの別名です。

#### `get-host-name` 〔手続き＋〕

MIT Scheme が走っているコンピュータを識別する文字列を返します。ふつうこれは修飾されていない
インターネットホスト名、すなわちドメインの接尾辞のないホスト名です。

```scheme
(get-host-name) ⇒ "aarau"
```

#### `os/hostname` 〔手続き＋〕

MIT Scheme が走っているコンピュータの正準インターネットホスト名を返します。したがって、
`get-host-name` の例とは対照的に、

```scheme
(os/hostname) ⇒ "aarau.ai.mit.edu"
```

#### `allocate-host-address` 〔手続き＋〕

ip アドレスオブジェクトを割り当てて返します。これは、ip アドレスを格納できる固定長（現在
4 バイト）の文字列にすぎません。この手続きは、`tcp-server-connection-accept` に渡す適切な
引数を生成するのに使われます。

```scheme
(allocate-host-address) ⇒ "Xe\034\241"
```

#### `host-address-any` 〔手続き＋〕

「任意のホスト」を指定する ip アドレスオブジェクトを返します。このオブジェクトは、
`open-tcp-server-socket` の `address` 引数として渡すときにのみ役立ちます。

```scheme
(host-address-any) ⇒ "\000\000\000\000"
```

#### `host-address-loopback` 〔手続き＋〕

ローカルのループバックネットワークインタフェースを指定する ip アドレスオブジェクトを返し
ます。ループバックインタフェースは、同じコンピュータ上のプロセス間の通信にのみ使えるソフト
ウェアのネットワークインタフェースです。このアドレスオブジェクトは、`open-tcp-server-socket`
の `address` 引数として渡すときにのみ役立ちます。

```scheme
(host-address-loopback) ⇒ "\177\000\000\001"
```

---

[^1]: この導入は『Common Lisp, The Language』第2版の 23.1 節を改変したものである。

[^2]: この説明は『Common Lisp, The Language』第2版の 23.1.1 節を改変したものである。
