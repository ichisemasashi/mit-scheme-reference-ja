<!--
本ファイルは、MIT Scheme Reference Manual（Edition 1.94, for Scheme Release 7.5,
2001）の日本語訳です。改変された著作物（翻訳）です。
原著: Copyright © 1988–2001 Massachusetts Institute of Technology.
原著ライセンス: GNU Free Documentation License, Version 1.1 以降（Invariant
Sections なし、Cover Texts なし）。本訳も同じ GFDL のもとで公開します。GFDL 英語
原文は GFDL-1.1.txt に、翻訳の条件は LICENSE.md にあります。食い違う場合は英語原文
が優先します（GFDL 第8節）。改変の告知: 原著（英語）を日本語に翻訳しました。
-->

# 16 エラーシステム

MIT Scheme のエラーシステムは、エラーやその他の例外的な条件を通知する一様な仕組みを提供
します。エラーシステムでもっとも単純で一般に役立つ手続きは次のものです。

**`error`**
単純なエラーを通知するのに使い、メッセージといくつかの刺激物（irritant）オブジェクトを
指定します（16.1節「条件の通知」を見よ）。エラーはふつう、計算を止めてユーザをエラー
repl に置くことで処理されます。

**`warn`**
警告を通知するのに使います（16.1節「条件の通知」を見よ）。警告はふつう、コンソールに
メッセージを表示して計算をふつうに続けることで処理されます。

**`ignore-errors`**
与えられた動的存続期間の中で、エラーのふつうの処理を抑えるのに使います（16.3節「条件の
処理」を見よ）。その存続期間の中で起こるどんなエラーも捕らえられ、ただちに
`ignore-errors` の呼び出し元に返ります。

より要求の厳しいアプリケーションは、より強力な機能を必要とします。具体的な例を挙げると、
浮動小数点の除算が、分母がゼロのときはいつでも非常に大きい数を返すようにしたいとします。
このふるまいはエラーシステムを使って実装できます。

Scheme の算術システムは、浮動小数点のゼロ除算を含む、多くの異なる種類のエラーを通知でき
ます。この例では、この特定の条件を特別に処理し、他の算術エラーはシステムがふつうの形で
処理するようにしたいわけです。

エラーシステムは、異なる型のエラー条件を区別する仕組みと、与えられた条件が生じたら制御を
どこへ移すべきかを指定する仕組みとを提供することで、この種のアプリケーションをサポート
します。この例では、「浮動小数点のゼロ除算」条件型を表す特定のオブジェクトがあり、その型
の条件が通知されたときに実行される任意の Scheme 手続きを動的に指定できます。この手続きは、
除算演算子の呼び出しを含むスタックフレームを見つけ、そのフレームから適切な値を返します。

もう1つの役立つ種類のふるまいは、関連する条件のクラスに一様な処理を指定できることです。
たとえば、ファイルを入力のために開くとき、ファイルシステムに結びついたさまざまな異なる
条件を優雅に処理できると望ましいかもしれません。そのような条件の1つは、ファイルが存在しない
ことかもしれません。この場合、プログラムは何か別の動作、おそらく別のファイルを開くこと
などを試みます。別の関連する条件は、ファイルが存在するが読み出しから保護されていて、入力の
ために開けないことです。これらやその他の関連する条件が起こると、プログラムはこの演算を
飛ばして別のことへ進みたいわけです。

同時に、ファイルシステムに無関係なエラーは、ふつうの形で扱われるべきです。たとえば、引数
3 に `car` を呼ぶとエラーを通知すべきです。あるいは、ファイルに与えられた名前が構文的に
誤っているかもしれません。これは、ファイルが存在しない場合とはおそらく異なる形で処理したい
条件です。

条件のクラスの処理を容易にするために、エラーシステムはすべての条件型を分類学的に組織
します。型は分類学的なリンクで互いに関連づけられ、それは1つの型が別の型の「一種」であること
を指定します。2つの型がこの形でリンクされていれば、一方は他方の**特殊化（specialization）**
とみなされます。逆に言えば、2番目は最初の**一般化（generalization）**です。この例では、
入力ファイルを開くことに結びついたすべてのエラーは、条件型「入力ファイルを開けない」の
特殊化になるでしょう。

条件型の分類学は、どの条件型も高々1つの直接の一般化しか持たないことを許します。したがって、
条件型は森（木の集合）をなします。ユーザは新しい木を作れますが、標準の分類学（16.7節
「分類学」を見よ）は、`condition-type:serious-condition`、`condition-type:warning`、
`condition-type:simple-condition`、`condition-type:breakpoint` を根とします。ユーザは、
森に新しい木を作るのではなく、これらの条件型に新しい下位型を加えることが勧められます。

まとめると、エラーシステムは次の仕事の機能を提供します。以下の節でこれらの機能をより詳しく
説明します。

**条件の通知**
条件はいくつかの異なる方法で通知できます。単純なエラーは、条件型を明示的に定義せずに、
`error` を使って通知できます。`signal-condition` 手続きがもっとも一般的な通知の仕組みを
提供します。

**条件の処理**
プログラマは、`bind-condition-handler` 手続きによって、特定の条件型や条件型のクラスの
ハンドラを動的に指定できます。個々のハンドラは条件の処理を完全に制御でき、加えて、特定の
条件を処理しないと決め、それを以前に束縛されたハンドラに渡すこともできます。

**ハンドラからの再起動**
`with-restart` 手続きは、条件を通知するコードが、条件を処理するコードに、条件を越えて
進むのに何をしなければならないかを伝える手段を提供します。ハンドラは、条件が通知された
ときに有効だった再起動を調べられ、中断された計算を構造化された形で続けられます。

**条件の状態の包装**
各条件は明示的なオブジェクトで表されます。条件オブジェクトは、条件の性質についての情報、
条件が生じた計算の状態を記述する情報、計算を再起動できる方法についての情報を含みます。

**条件の分類**
各条件は型を持ち、条件型オブジェクトで表されます。各条件型は、他の何らかの条件型の特殊化
でありえます。共通の一般化を共有する型のグループは、その一般化のハンドラを指定することで
一様に処理できます。

## 16.1 条件の通知

`make-condition`（または任意の条件コンストラクタ）を使って条件のインスタンスが作られると、
それを通知できます。条件を通知する行為は、条件を作る行為と分けられており、条件がどう処理
されるかにより柔軟性を持たせています。たとえば、条件のインスタンスを手続きの値として返して、
何か異常なことが起こったことを示し、呼び出し元が何らかの状態を後始末できるようにできます。
呼び出し元は、準備ができたら条件を通知できます。

別個の条件通知の仕組みを持つより重要な理由は、それが**再通知（resignalling）**を可能にする
ことです。通知された条件が特定のハンドラに捕らえられ、そのハンドラがその特定の条件を処理
したくないと決めると、条件を再び通知できます。これは、他のハンドラに条件を見る機会を与える
1つの方法です。

#### `error reason argument…` 〔手続き＋〕

これは、計算が進む前に介入を必要とする条件を通知する、もっとも単純で一般的な方法です
（介入が必要でないときは `warn` のほうが適切です）。`error` は（`signal-condition` を
使って）条件を通知し、その条件のどのハンドラも（たとえば再起動を起動して）制御の流れを
変えなければ、手続き `standard-error-handler` を呼びます。これはふつうエラーメッセージを
表示して計算を止め、エラー repl に入ります。ふつうの状況では `error` は値を返しません
（ただし対話的なデバッガを使ってこれを強制的に起こせます）。

どの条件が通知されるかは、`error` への第1引数によります。`reason` が条件なら、その条件が
通知され、引数は無視されます。`reason` が条件型なら、この型の新しいインスタンスが生成されて
通知されます。引数はこの条件型のフィールドの値を生成するのに使われます（`make-condition`
に `field-plist` 引数として渡されます）。しかし、もっともよくある場合、`reason` は条件でも
条件型でもなく、文字列かシンボルです。この場合、`condition-type:simple-error` 型の条件が
作られ、message フィールドに `reason`、irritants フィールドに引数が入ります。

#### `warn reason argument…` 〔手続き＋〕

条件が介入に値するほど深刻でないときは、`error` ではなく `warn` で条件を通知するのが適切
です。`error` と同様に、`warn` はまず `signal-condition` を呼びます。通知される条件は
`error` とまったく同じように選ばれますが、`reason` が条件でも条件型でもなければ
`condition-type:simple-warning` 型の条件が通知される点が異なります。条件が処理されなければ、
`warn` は手続き `standard-warning-handler` を呼びます。これはふつう警告メッセージを表示し、
`warn` から返ることで計算を続けます。

`warn` は `signal-condition` を呼ぶ前に `muffle-warning` という名前の再起動を確立します。
これにより、シグナルハンドラが `muffle-warning` を呼んで警告メッセージの生成を防げます。
`warn` の呼び出しの値は未規定です。

#### `signal-condition condition` 〔手続き＋〕

これは条件を通知する基本的な演算です。`signal-condition` の正確な動作は、`condition` が
インスタンスである条件型、`break-on-signals` が設定した条件型、`bind-condition-handler`
と `bind-default-condition-handler` が確立したハンドラによります。

`condition` が、`break-on-signals` が指定する型のいずれかの特殊化である型のインスタンス
なら、ブレークポイント repl が始まります。そうでなければ（またはその repl が返ると）、
`bind-condition-handler` が確立したハンドラが、新しいものから順に調べられます。当てはまる
各ハンドラが起動され、ハンドラがふつうに返ればハンドラの探索が続きます。当てはまるすべての
ハンドラが返れば、`bind-default-condition-handler` が確立した当てはまるハンドラが、これも
新しいものから順に調べられます。最後に、当てはまるハンドラがなければ（またはすべてがふつう
の形で返れば）、`signal-condition` は未規定の値を返します。

注意: 他の多くのシステムと違って、MIT Scheme のランタイムライブラリはどんな種類のハンドラ
も確立しません。（ただし Edwin テキストエディタは条件ハンドラを広く使います。）したがって、
次の例が示すように、ユーザが供給した条件ハンドラがなければ、`signal-condition` の呼び出し
は呼び出し元に返ります。

```scheme
(signal-condition
 (make-condition
  condition-type:error
  (call-with-current-continuation (lambda (x) x))
  '()    ; 再起動なし
  '())) ; フィールドなし
⇒ unspecified
```

## 16.2 エラーメッセージ

慣習として、エラーメッセージ（および一般に `write-condition-report` が生成する報告）は、
1つ以上の完全な文からなるべきです。文のふつうの規則に従うべきです。文の最初の語は大文字で
始め、文はピリオドで終えるべきです。メッセージには、改行や字下げのような余計な空白を含める
べきではありません。

エラーシステムは、プログラマがエラーメッセージの表示をある程度制御できる、単純な整形言語を
提供します。この整形言語はおそらく将来のリリースで再設計されます。

エラーメッセージはふつう、エラーを記述する文字列に、いくつかの刺激物オブジェクトが続いた
ものからなります。文字列は `display` を使って表示され、刺激物は `write` を使って、ふつう
各刺激物のあいだにスペースを置いて表示されます。単純な整形を可能にするために、**ノイズ
オブジェクト（noise object）**を導入します。これは `display` を使って表示されます。刺激物
のリストは、ふつうのオブジェクトとノイズオブジェクトを混ぜて含めます。各ノイズオブジェクト
は余計な空白なしに `display` で表示され、各ふつうのオブジェクトは、単一のスペース文字を
前に付けて `write` で表示されます。

例を挙げます。

```scheme
(define (error-within-procedure message irritant procedure)
  (error message
         irritant
         (error-irritant/noise "within procedure")
         procedure
         (error-irritant/noise ".")))
```

これは次のように整形されます。

```scheme
(error-within-procedure "Bad widget" 'widget-32 'invert-widget)                  error>

Bad widget widget-32 within procedure invert-widget.
```

エラーメッセージをサポートする演算は次のとおりです。

#### `format-error-message message irritants port` 〔手続き＋〕

`message` はふつう文字列（ただし必須ではありません）、`irritants` は刺激物オブジェクトの
リスト、`port` は出力ポートです。`message` と `irritants` を標準の形で `port` に整形します。
整形の過程で、リストが表示される深さと幅がそれぞれ小さい数に制限され、各刺激物からの出力が
際限なく大きくならないことが保証される点に注意してください。

#### `error-irritant/noise value` 〔手続き＋〕

値が `value` であるノイズオブジェクトを作って返します。

## 16.3 条件の処理

条件の発生は `signal-condition` を使って通知されます。`signal-condition` は、起こった条件
の型を扱う用意のある条件ハンドラを見つけて起動しようとします。条件ハンドラは、通知される
条件という1つの引数を取る手続きです。手続きは、`bind-condition-handler`（特定の thunk が
実行されているあいだだけ有効なハンドラを確立する）か `bind-default-condition-handler`
（恒久的に有効なハンドラを確立する）を呼んで条件ハンドラとして設置されます。名前が示すとおり、
`bind-default-condition-handler` が作るハンドラは、当てはまる他のすべてのハンドラが起動
されたあとにのみ起動されます。

ハンドラは、適切とみなすどんな形でもシグナルを処理できますが、よくある型は次のとおりです。

**条件を無視する。**
ふつうの形でハンドラから返ることによって。

**条件を処理する。**
何らかの処理をし、それから `signal-condition` の呼び出しより前のある地点で確立された再起動
（あるいは、より好ましくないですが継続）を起動することによって。

**条件を再通知する。**
何らかの処理をし、同じ条件か新しく作った条件のどちらかで `signal-condition` を呼ぶことに
よって。これをサポートするために、`signal-condition` は、その後の `signal-condition` の
呼び出しがこのハンドラより前に確立されたハンドラだけを見るような形で、ハンドラを走らせます。

条件ハンドラのデバッグを助けるために、Scheme は、ふつうの条件通知より前に対話的なブレーク
ポイントを起こす条件型の集合を保ちます。すなわち、`signal-condition` は、その引数がこれらの
型のいずれかの特殊化である条件のとき、ふつうの動作より前に新しい repl を作ります。手続き
`break-on-signals` がこの条件型の集合を確立します。

#### `ignore-errors thunk` 〔手続き＋〕

`condition-type:error` の任意の特殊化（`error` の呼び出しが生むものを含む）の通知を横取り
する条件ハンドラとともに `thunk` を実行し、ただちに `thunk` の実行を終わらせ、通知された
条件を値として `ignore-errors` の呼び出しから返します。`thunk` がふつうに返れば、その値が
`ignore-errors` から返されます。

`ignore-errors` は「通知を切る」わけでも条件処理を切るわけでもないことに注意してください。
条件処理はふつうの形で行われますが、`condition-type:error` から特殊化された条件は、既定で
そうされるように伝播されるのではなく捕らえられます。

#### `bind-condition-handler condition-types handler thunk` 〔手続き＋〕

`condition-types` が指定する条件のための条件ハンドラとして `handler` を加えたあと、`thunk`
を起動します。`condition-types` は条件型のリストでなければなりません。これらの型のいずれか
の特殊化である型の条件を通知すると、`handler` が起動されます。ハンドラを起動するのに使われる
仕組みの説明は、`signal-condition` を見よ。

特別な拡張として、`condition-types` が空リストなら、`handler` はすべての条件について呼ばれ
ます。

#### `bind-default-condition-handler condition-types handler` 〔手続き＋〕

`condition-types` が指定する条件のための（恒久的な）条件ハンドラとして `handler` を設置
します。`condition-types` は条件型のリストでなければなりません。これらの型のいずれかの特殊化
である型の条件を通知すると、`handler` が起動されます。ハンドラを起動するのに使われる仕組み
の説明は、`signal-condition` を見よ。

特別な拡張として、`condition-types` が空リストなら、`handler` はすべての条件について呼ばれ
ます。

#### `break-on-signals condition-types` 〔手続き＋〕

`signal-condition` が、`condition-types` のリストのいずれかの型の特殊化である条件を通知
する前に、対話的な repl を作るよう手配します。これは、カスタムの条件ハンドラを使うコードを
デバッグしようとするときに非常に役立ちます。どんな条件型が通知されても repl を作るには、
実際には `signal-condition` の入口にブレークポイントを置くのがいちばんです。

#### `standard-error-handler condition` 〔手続き＋〕

`error` が `signal-condition` を呼んだあと、内部で呼びます。ふつう、プロンプト `"error>"`
の新しい repl を作ります（ただし `standard-error-hook` を見よ）。`error` を呼ぶ効果を
まねるには、コードは `signal-condition` を直接呼び、`signal-condition` が返れば
`standard-error-handler` を呼べます。

#### `standard-error-hook` 〔変数＋〕

この変数は手続き `standard-error-handler`、したがって `error` のふるまいを制御します。
`fluid-let` で束縛することを意図しており、ふつう `#f` です。1引数の手続きに変えられ、その
場合、エラー repl を始める直前に `standard-error-handler` によって（`standard-error-hook`
を `#f` に再束縛して）起動されます。1つの引数、通知される条件が渡されます。

#### `standard-warning-handler condition` 〔手続き＋〕

これは、`warn` が `signal-condition` を呼んだあと、内部で呼ぶ手続きです。
`standard-warning-handler` のふつうのふるまいは、メッセージを表示することです（ただし
`standard-warning-hook` を見よ）。より正確には、メッセージは `notification-output-port`
が返すポートに表示されます。メッセージは、まず文字列 `"Warning: "` をこのポートに表示し、
それから `condition` とそのポートに `write-condition-report` を呼んで作られます。

`warn` を呼ぶ効果をまねるには、コードは `signal-condition` を直接呼び、`signal-condition`
が返れば `standard-warning-handler` を呼べます。（ただし、これは `muffle-warning` プロトコル
を実装するには十分ではありません。その目的には明示的な再起動を提供しなければなりません。）

#### `standard-warning-hook` 〔変数＋〕

この変数は手続き `standard-warning-handler`、したがって `warn` のふるまいを制御します。
`fluid-let` で束縛することを意図しており、ふつう `#f` です。1引数の手続きに変えられ、その
場合、警告メッセージを書く代わりに `standard-warning-handler` によって（`standard-warning-hook`
を `#f` に再束縛して）起動されます。1つの引数、通知される条件が渡されます。

## 16.4 再起動

Scheme のエラーシステムは、**再起動（restart）**として知られる仕組みを提供します。これは、
条件を通知するコードと条件を処理するコードを協調させるのを助けます。条件を検出して通知する
コードのモジュールは、計算を続ける・中止する・再起動したいハンドラが起動する手続きを
（`with-simple-restart` や `with-restart` を使って）提供できます。これらの手続きは
**再起動作動子（restart effector）**と呼ばれ、再起動オブジェクトにカプセル化されます。

条件オブジェクトが作られると、それは再起動オブジェクトの集合を含み、その各々が再起動作動子
を含みます。条件ハンドラは、処理している条件を調べられ（名前で再起動を見つけるには
`find-restart`、集合全体を見るには `condition/restarts` を使います）、結びついた作動子を
起動できます（`invoke-restart` や `invoke-restart-interactively` を使います）。作動子は
引数を取れ、これらは条件を処理するコードが直接計算するか、ユーザから対話的に集めます。

再起動の名前は任意に選べますが、名前の選択は重要です。これらの名前は、通知するコード（再起動
の名前を供給する）と処理するコード（ふつうその再起動の名前で再起動作動子を選ぶ）とのあいだ
を協調させるのに使われます。したがって、名前は、通知するコードが実装し処理するコードが起動
する再起動プロトコルを指定します。プロトコルは、作動子のコードが要求する引数の数と、引数の
意味論を示します。

Scheme は、よく使うための慣習的な名前（したがってプロトコル）の集合を提供します。この集合
から再起動の名前を選ぶことで、通知するコードは、かなりよくある少数の動作（`abort`、
`continue`、`muffle-warning`、`retry`、`store-value`、`use-value`）を行えることを示せます。
それに応じて、単純な条件処理コードは、行いたい種類の動作を探し、名前でそれを起動するだけで
済みます。Scheme の慣習的な名前はすべてシンボルですが、一般に再起動の名前は特定のデータ型に
制限されません。加えて、オブジェクト `#f` は「自動的な使用のためではない」プロトコルを示す
ために予約されています。これらの再起動は人間の制御のもとでのみ作動させるべきです。

再起動それ自体は第一級のオブジェクトです。名前、起動されたら実行される手続き（作動子と
知られます）、再起動の記述を表示するために起動できる thunk（報告器（reporter）と知られ、
たとえば対話的なデバッガが使います）をカプセル化します。再起動を起動することは、ハンドラが
条件の制御を受け入れることを選んだ印です。その帰結として、再起動の作動子は返るべきでは
ありません。返ると、ハンドラが条件の処理を辞退したことを示すからです。したがって、作動子は、
条件の通知の過程が始まる前に捕らえた継続を呼ぶべきです。通知するコードによるもっともよくある
使用の型は `with-simple-restart` にカプセル化されています。

この章では、`restarts` という名前のパラメータは次の値のいずれも受け取ります。

- 再起動オブジェクトのリスト。
- 条件。その条件に手続き `condition/restarts` が呼ばれ、結果の再起動のリストが条件の代わり
  に使われます。
- シンボル `bound-restarts`。手続き `bound-restarts` が（引数なしで）呼ばれ、結果の再起動
  のリストがシンボルの代わりに使われます。
- `restarts` パラメータが省略可能で与えられなければ、シンボル `bound-restarts` を指定した
  のと等価です。

### 16.4.1 再起動コードの確立

#### `with-simple-restart name reporter thunk` 〔手続き＋〕

既存の名前付き再起動に `name` という名前の再起動を加えて作った動的環境で、`thunk` を起動
します。`reporter` は `thunk` の実行のあいだ、新しく作られた再起動の記述を作るのに使えます。
1つの引数（ポート）の手続きか、文字列のどちらかでなければなりません。慣習として、`reporter`
が生成する記述は、最初の語を大文字にしピリオドで終える、短い完全な文であるべきです。文は
少し余裕を残して1行に収まるべきです（下の例を見よ）。ふつうこれは、文が長さ 70 文字以下で
あるべきことを意味します。

`with-simple-restart` が作る再起動が起動されると、`with-simple-restart` の呼び出しから
未規定の値を返すことで、進行中の計算を単に中止します。そうでなければ、`with-simple-restart`
は `thunk` が計算した値を返します。

```scheme
(with-simple-restart 'george "This restart is named george."
  (lambda () 3)) ⇒ 3

(with-simple-restart 'george "This restart is named george."
  (lambda ()
    (invoke-restart (find-restart 'george)))) ⇒ unspecific

(with-simple-restart 'george "This restart is named george."
  (lambda () (car 3)))
;The object 3, passed as the first argument to car,
; is not the correct type.
;To continue, call RESTART with an option number:
; (RESTART 3) => Specify an argument to use in its place.
; (RESTART 2) => This restart is named george.
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `with-restart name reporter effector interactor thunk` 〔手続き＋〕

既存の名前付き再起動に `name` という名前の再起動を加えて作った動的環境で、`thunk` を起動
します。`reporter` は `thunk` の実行のあいだ、新しく作られた再起動の記述を作るのに使えます。
1つの引数（ポート）の手続きか、文字列のどちらかでなければなりません。`effector` は、再起動
が `invoke-restart` によって起動されたときに呼ばれる手続きです。`interactor` は、作動子が
対話的に起動されるときに作動子に渡される引数を指定します。引数のない手続きか `#f` のどちら
かでよいです。`interactor` が `#f` なら、この再起動は対話的に起動されることを意図していま
せん。

`with-restart` が返す値は `thunk` が返す値です。ただし、再起動が条件ハンドラによって起動
されると、作動子はそれを起動したハンドラに返りません。かわりに、作動子は条件の通知の過程が
始まる前に作られた継続を呼ぶべきで、したがって `with-restart` はふつうの形では返りません。

```scheme
(define (by-george! thunk)
  ; このコードは、thunk を実行するあいだに生じる条件を、GEORGE 再起動を
  ; 起動して処理する。再起動の作動子コードに 1 と 2 を渡す。
  (bind-condition-handler '() ; すべての条件
    (lambda (condition)
       (invoke-restart (find-restart 'george) 1 2))
    thunk))

(define (can-george! thunk)
  ; このコードはエラーを処理する方法、すなわち GEORGE 再起動を提供する。
  ; GEORGE するには2つの値を供給しなければならない。
  (lambda ()
     (call-with-current-continuation
      (lambda (kappa)
         (with-restart
          'george                               ; 名前
          "This restart is named george." ; 報告器
          (lambda (a b)                         ; 作動子
            (kappa (list 'george a b)))
          values                                ; 対話子
          thunk)))))                            ; Thunk
(by-george! (can-george! (lambda () -3))        ⇒ -3
(by-george! (can-george! (lambda () (car 'x)))) ⇒ (george 1 2)
```

### 16.4.2 標準の再起動コードの起動

Scheme は、条件から再起動する6つの標準プロトコルをサポートします。各々は、名前付き再起動
（条件を通知するコードが使う）と単純な手続き（条件を処理するコードが使う）を使ってカプセル
化されています。とくに指定がなければ、これらの手続きの1つが対応する再起動を見つけられなけ
れば、ただちに未規定の値で返ります。

これらの手続きはそれぞれ、上の16.4節「再起動」で説明した省略可能引数 `restarts` を受け取り
ます。

#### `abort [restarts]` 〔手続き＋〕

`abort` という名前の再起動を使って計算を中止します。対応する作動子は引数を取らず、現在の
計算の筋を捨てます。これは Scheme の repl が提供する再起動です。

`abort` という名前の再起動がなければ、この手続きは `condition-type:no-such-restart` 型の
エラーを通知します。

#### `continue [restarts]` 〔手続き＋〕

`continue` という名前の再起動を使って現在の計算を続けます。対応する作動子は引数を取らず、
条件が通知された地点を越えて計算を続けます。

#### `muffle-warning [restarts]` 〔手続き＋〕

`muffle-warning` という名前の再起動を使って現在の計算を続けます。対応する作動子は引数を
取らず、条件から生じるどんな警告メッセージもユーザに提示される地点を越えて計算を続けます。
手続き `warn` はこの目的のために `muffle-warning` 再起動を確立します。

`muffle-warning` という名前の再起動がなければ、この手続きは `condition-type:no-such-restart`
型のエラーを通知します。

#### `retry [restarts]` 〔手続き＋〕

`retry` という名前の再起動を使って現在の計算をやり直します。対応する作動子は引数を取らず、
条件を引き起こしたのと同じ計算を単にやり直します。もちろん、根本原因が除かれていなければ、
条件は再発しうります。「ファイルが存在しない」エラーを通知するコードは、`retry` 再起動を
供給すると期待できます。この再起動は、欠けたファイルをまず作ったあとに起動されます。単純に
やり直せば計算が成功しそうだからです。

#### `store-value new-value [restarts]` 〔手続き＋〕

まず `new-value` を格納したあと、`store-value` という名前の再起動を使って現在の計算をやり
直します。対応する作動子は1つの引数 `new-value` を取り、それを再起動に依存する場所に格納
してから、条件を引き起こしたのと同じ計算をやり直します。もちろん、根本原因が除かれていなけ
れば、条件は再発しうります。「未代入の変数」エラーを通知するコードは、`store-value` 再起動
を供給すると期待できます。これは値を変数に格納して計算を続けます。

#### `use-value new-value [restarts]` 〔手続き＋〕

`use-value` という名前の再起動を使って現在の計算をやり直しますが、以前に失敗を引き起こした
値に `new-value` を代入します。対応する作動子は1つの引数 `new-value` を取り、失敗した値の
代わりに新しい値を代入して、条件を引き起こしたのと同じ計算をやり直します。もちろん、新しい
値も条件を引き起こせば、条件は再発しうります。

「未代入の変数」エラーを通知するコードは、`use-value` 再起動を供給すると期待できます。これ
は変数の値の代わりに `new-value` で計算を単に続けます。これを `retry` と `store-value` 再起動
と対比してください。`retry` 再起動を使うと、変数がまだ値を持たないので失敗します。`store-value`
再起動は使えますが、変数の値を変えてしまうので、その後の変数への参照は検出されなくなります。

### 16.4.3 一般の再起動コードの発見と起動

再起動は、条件を通知するコードと条件を処理するコードのあいだのプロトコルを確立する一般的な
仕組みです。Scheme のエラーシステムは、いくつかのよくあるプロトコルの「包装」を提供します。
また、カスタマイズされたプロトコルを実装することを意図した低水準のフックも提供します。通知
するコードが使う仕組み（`with-restart` と `with-simple-restart`）が両方の目的に使われます。

条件を処理するコードの使用のために、4つの追加の演算が提供されます。2つの演算
（`bound-restarts` と `find-restart`）は、条件を処理するコードが有効な再起動を見つけられる
ようにします。他の2つの演算（`invoke-restart` と `invoke-restart-interactively`）は、
再起動オブジェクトが見つかったら再起動作動子を起動できるようにします。

加えて、再起動オブジェクトにカプセル化された情報へのアクセスを提供するデータ抽象があります。

#### `bound-restarts` 〔手続き＋〕

現在有効なすべての再起動オブジェクトのリストを、もっとも最近設置されたものを先頭に返します。
`bound-restarts` は条件を処理するコードでは慎重に使うべきです。条件が通知された時点ではなく、
それが呼ばれた時点で有効なすべての再起動を明かすからです。しかし、新しく生成される条件
オブジェクトに含めるための再起動のリストを集めるのや、システムの現在の状態を調べるのには
役立ちます。

#### `find-restart name [restarts]` 〔手続き＋〕

`restarts` のリストの中で `name` という名前の最初の再起動オブジェクトを返します（`restarts`
に許される値は上の16.4節「再起動」で説明しています）。条件ハンドラで使われるとき、
`find-restart` にはふつう特定の再起動の名前と、通知された条件オブジェクトが渡されます。この
形で、ハンドラは条件が作られたとき（ふつう通知されたときと同じ）に利用できた再起動だけを
見つけます。`restarts` が省かれれば、現在有効な再起動が使われ、これらはしばしば条件が起こった
あとに加えられた再起動を含みます。

#### `invoke-restart restart argument…` 〔手続き＋〕

`restart` にカプセル化された再起動作動子を、指定された引数を渡して呼びます。`invoke-restart`
は、`restart` が実装するプロトコルを理解し、したがって適切な引数の集合を計算して渡せる、
条件を処理するコードの使用を意図しています。

条件ハンドラが作動子の引数を集めるためにユーザと対話する必要があれば（たとえば `restart` が
実装するプロトコルを理解しなければ）、`invoke-restart` の代わりに
`invoke-restart-interactively` を使うべきです。

#### `invoke-restart-interactively restart` 〔手続き＋〕

まず `restart` にカプセル化された対話子を呼び、`restart` の作動子に必要な引数を対話的に集め
ます。それから作動子を呼び、これらの引数を渡します。`invoke-restart-interactively` は
対話的な再起動（`restart/interactor` が `#f` でないもの）を呼ぶことを意図しています。便宜
のため、再起動に対話子がなければ、`invoke-restart-interactively` は再起動の作動子を引数
なしで呼びます。このふるまいは将来変わるかもしれません。

### 16.4.4 名前付き再起動の抽象

再起動オブジェクトは非常に単純です。名前、作動子、対話子、記述だけをカプセル化するからです。

#### `restart? object` 〔手続き＋〕

`object` が再起動でないとき、かつそのときにかぎり `#f` を返します。

#### `restart/name restart` 〔手続き＋〕

`restart` の名前を返します。Scheme のエラーシステムはあらかじめ定めた名前にシンボルと
オブジェクト `#f` しか使いませんが、プログラムは任意のオブジェクトを使えます（名前の等価性
は `eq?` を使って検査されます）。

#### `restart/effector restart` 〔手続き＋〕

`restart` にカプセル化された作動子を返します。`invoke-restart` と
`invoke-restart-interactively` がもっともよくある起動の型を捕らえるので、ふつうこの手続き
は使いません。

#### `restart/interactor restart` 〔手続き＋〕

`restart` にカプセル化された対話子を返します。これは引数のない手続きかオブジェクト `#f` の
どちらかです。`invoke-restart-interactively` がもっともよくある使用を捕らえるので、ふつう
この手続きは使いません。したがって、`restart/interactor` は、`restart` が対話的に起動される
ことを意図しているかを判定する述語としてもっとも役立ちます。

#### `write-restart-report restart port` 〔手続き＋〕

`restart` の記述を `port` に書きます。これは、再起動が作られたときに供給された報告器を、
（文字列なら）`display` するか（手続きなら）呼ぶことで働きます。

## 16.5 条件のインスタンス

条件は、その型に結びついた情報に加えて、ふつう同じ型の他の条件とは共有されない他の情報も
含みます。たとえば、「未束縛の変数」エラーに結びついた条件型は、未束縛だった変数の名前を
指定しません。追加の情報は、条件のインスタンスとも呼ばれる条件オブジェクトに捕らえられます。

与えられた型の条件に固有の情報（「未束縛の変数」条件の変数名など）に加えて、どの条件の
インスタンスも、条件が起こった計算の状態をカプセル化する継続を含みます。この継続は、条件が
起こった文脈についてもっと知るために計算を分析するのに使われます。計算を続ける仕組みを提供
することは意図していません。その仕組みは再起動が提供します。

### 16.5.1 条件に対する演算の生成

Scheme は、条件型を入力として取り、対応する条件オブジェクトに対する演算を生む4つの手続きを
提供します。これらは、レコード演算子を生むレコード型に対する演算を思わせます（10.4節
「レコード」を見よ）。条件型を与えられれば、次を生成できます。型のインスタンスのコンストラクタ
（`condition-constructor` を使う）、型のインスタンスのフィールドの内容を取り出すアクセサ
（`condition-accessor` を使う）、型のインスタンスを検査する述語（`condition-predicate` を
使う）、型のインスタンスを作って通知する手続き（`condition-signaller` を使う）です。

条件オブジェクトの作成は、条件の発生の通知とは別物であることに注意してください。条件
オブジェクトは第一級です。作られて決して通知されないこともあれば、複数回通知されることも
あります。さらに、条件を書き換える手続きはないことに注意してください。いちど作られると、
条件は変えられません。

#### `condition-constructor condition-type field-names` 〔手続き＋〕

`field-names` で指定されるフィールドの値を引数として取り、`condition-type` 型の条件を作る
コンストラクタ手続きを返します。`field-names` は `condition-type` のフィールド名の部分集合
であるシンボルのリストでなければなりません。`condition-constructor` が返すコンストラクタ
手続きは次のシグネチャを持ちます。

```scheme
(lambda (continuation restarts . field-values) ...)
```

ここで `field-names` は `field-values` に対応します。コンストラクタ引数 `restarts` は16.4節
「再起動」で説明しています。コンストラクタ手続きが作る条件は、`field-names` が指定するもの
以外のすべてのフィールドの値に `#f` を持ちます。

たとえば、次の手続き `make-simple-warning` は、継続（条件が起こった場所）、利用できるように
する再起動の記述、警告メッセージ、警告を引き起こした刺激物のリストを与えられて、
`condition-type:simple-warning` 型の条件を構築します。

```scheme
(define make-simple-warning
  (condition-constructor condition-type:simple-warning
                              '(message irritants)))
```

#### `condition-accessor condition-type field-name` 〔手続き＋〕

`condition-type` 型の条件オブジェクトを入力として取り、指定された `field-name` の内容を
取り出す手続きを返します。`condition-accessor` は、`field-name` が `condition-type` の
名前の付いたフィールドの1つでなければ `error:bad-range-argument` を通知します。返される
手続きは、`condition-type` 型またはその特殊化の条件以外のオブジェクトを渡されると
`error:wrong-type-argument` を通知します。

条件の特定のフィールドが繰り返しアクセスされると前もって分かっていれば、（おそらくより便利
だが遅い）`access-condition` 手続きを使うより、`condition-accessor` を使ってそのフィールド
のアクセサを構築する価値があります。

#### `condition-predicate condition-type` 〔手続き＋〕

オブジェクトが `condition-type` 型またはその特殊化の条件かどうかを検査する述語手続きを返し
ます（与えられた型の条件だが、その型の特殊化ではない条件を検査する、あらかじめ定められた
方法はありません）。

#### `condition-signaller condition-type field-names default-handler` 〔手続き＋〕

パラメータ `field-names` を持つ通知手続きを返します。通知手続きが呼ばれると、`condition-type`
型の条件を作って通知します。条件が処理されなければ（すなわち、現在の継続からの脱出を起こす
ハンドラが起動されなければ）、通知手続きは、条件を引数として `default-handler` を呼ぶこと
に帰着します。

`default-handler` に慣習的に使われる標準の手続きがいくつかあります。`condition-type` が
`condition-type:error` の特殊化なら、`default-handler` は手続き `standard-error-handler`
であるべきです。`condition-type` が `condition-type:warning` の特殊化なら、`default-handler`
は手続き `standard-warning-handler` であるべきです。`condition-type` が
`condition-type:breakpoint` の特殊化なら、`default-handler` は手続き
`standard-breakpoint-handler` であるべきです。

### 16.5.2 条件の抽象

条件データ型は、述語 `condition?` とアクセサ手続きの集合を通じて抽象化されます。

#### `condition? object` 〔手続き＋〕

`object` が条件でないとき、かつそのときにかぎり `#f` を返します。

#### `condition/type condition` 〔手続き＋〕

`condition` がインスタンスである条件型を返します。

#### `condition/error? condition` 〔手続き＋〕

`condition` が条件型 `condition-type:error` またはその特殊化のインスタンスなら `#t` を、
そうでなければ `#f` を返します。

#### `condition/restarts condition` 〔手続き＋〕

`condition` が作られたときに指定された再起動のリストを返します。

#### `condition/continuation condition` 〔手続き＋〕

`condition` が作られたときに指定された継続を返します。これは、条件が起こったときのシステム
の状態を調べるために提供されるもので、計算を続けたり再起動したりするためではありません。

#### `write-condition-report condition port` 〔手続き＋〕

`condition` に結びついた条件型の報告器関数を使って、`condition` の記述を `port` に書きます。
`condition/report-string` も見よ。

### 16.5.3 条件のインスタンスに対する単純な演算

この節で説明する単純な手続きは、上で説明した条件オブジェクトのより詳しい抽象の上に構築され
ています。これらの手続きはときに使いやすいですが、しばしば効率が劣ります。

#### `make-condition condition-type continuation restarts field-plist` 〔手続き＋〕

`continuation` に結びついた、`condition-type` 型のインスタンスとして新しい条件オブジェクト
を作ります。継続は調べる目的のためだけに提供されるもので、計算を再起動するためではありま
せん。`restarts` 引数は16.4節「再起動」で説明しています。`field-plist` は、フィールド名と
それらのフィールドの値を交互に並べたリストで、フィールド名は
`(condition-type/field-names condition-type)` が返すものです。これは条件オブジェクトの
フィールドに値を提供するのに使われます。値の指定されないフィールドは `#f` に設定されます。
いちど条件オブジェクトが作られると、これらのフィールドの値を変える方法はありません。

#### `access-condition condition field-name` 〔手続き＋〕

`condition` の中のフィールド `field-name` に格納された値を返します。`field-name` は
`(condition-type/field-names (condition/type condition))` が返す名前の1つでなければなり
ません。`access-condition` は実行時に `field-name` を調べるので、同じフィールドを同じ条件型
のいくつものインスタンスから取り出すなら、`condition-accessor` を使ってアクセス関数を作る
ほうが効率的です。

#### `condition/report-string condition` 〔手続き＋〕

条件の報告を含む文字列を返します。これは、`condition` と文字列出力ポートに
`write-condition-report` を呼び、ポートが集めた出力を文字列として返すことで生成されます。

## 16.6 条件型

各条件は、それに結びついた条件型オブジェクトを持ちます。これらのオブジェクトは、関連する
条件のクラスに焦点を当てる手段として使われます。第一に、特定のクラスの条件についてのすべて
の情報を1つの場所に集中させることで、第二に、型どうしのあいだの継承関係を指定することに
よってです。この継承関係が条件の階層の分類学的な構造をなします（16.7節「分類学」を見よ）。

次の手続きが条件型の抽象をなします。

#### `make-condition-type name generalization field-names reporter` 〔手続き＋〕

`generalization`（条件型なら）の特殊化である、または（`generalization` が `#f` なら）条件型
の新しい木の根である（新しい）条件型を作って返します。デバッグの目的のため、条件型は `name`
を持ち、この型のインスタンスは、すべての条件に共通するフィールド（type、continuation、
restarts）に加えて、`field-names`（シンボルのリスト）が指定するフィールドの記憶域を含み
ます。

`reporter` は、この型の特定の条件の記述を作るのに使われます。条件を記述する文字列、アリティ
が 2 の手続き（第1引数はこの型の条件、第2引数はポート）でメッセージを与えられたポートに書く
もの、あるいは、報告器を条件型の `generalization` から取るべきことを指定する `#f`（または、
`generalization` が `#f` なら「型 … の記録されていない条件」というメッセージを作る）でよい
です。記述を作るのに使われる慣習は16.2節「エラーメッセージ」で詳しく述べています。

#### `condition-type/error? condition-type` 〔手続き＋〕

`condition-type` が `condition-type:error` またはその特殊化なら `#t` を、そうでなければ
`#f` を返します。

#### `condition-type/field-names condition-type` 〔手続き＋〕

`condition-type` 型の条件のすべてのフィールド名のリストを返します。これは、この
`condition-type` が作られたときに指定されたフィールドと、この `condition-type` の
`generalization` の `condition-type/field-names` との和集合です。

#### `condition-type/generalizations condition-type` 〔手続き＋〕

`condition-type` のすべての一般化のリストを返します。どの条件型もそれ自身の一般化とみなされ
ることに注意してください。

#### `condition-type? object` 〔手続き＋〕

`object` が条件型でないとき、かつそのときにかぎり `#f` を返します。

## 16.7 条件型の分類学

MIT Scheme のエラーシステムは、あらかじめ定められた条件型の豊富な集合を提供します。これら
は、「特殊化する」と「一般化する」の関係を提供する分類学的なリンクを通じて森に組織されて
います。下に現れる図は、与えられた型のすべての特殊化を、その型に対して字下げすることで、
これらの関係を示します。これらの条件型に束縛される変数には接頭辞 `condition-type:` が付く
ことに注意してください。たとえば、次の表に `simple-error` として現れる型は、変数
`condition-type:simple-error` に格納されています。ユーザは、既存のものの特殊化を作ることで
新しい条件型を加えることが勧められます。

図に続いて、あらかじめ定められた条件型の詳しい説明があります。これらの型のいくつかは
**抽象型（abstract type）**として印が付いています。抽象型は、条件の型として直接使うことを
意図していません。他の型の一般化として、また条件ハンドラを束縛するために使うものです。抽象
と印の付いていない型は**具体型（concrete）**で、条件の型として明示的に使うことを意図して
います。

```text
serious-condition
    error
        simple-error
        illegal-datum
            wrong-type-datum
                wrong-type-argument
                wrong-number-of-arguments
            datum-out-of-range
                bad-range-argument
            inapplicable-object
        file-error
            file-operation-error
            derived-file-error
        port-error
            derived-port-error
        variable-error
            unbound-variable
            unassigned-variable
        arithmetic-error
            divide-by-zero
            floating-point-overflow
            floating-point-underflow
        control-error
            no-such-restart
        not-loading
        primitive-procedure-error
            system-call-error
warning
    simple-warning
simple-condition
breakpoint
```

#### `condition-type:serious-condition` 〔条件型＋〕

これは抽象型です。何らかの形の介入を必要とするすべての深刻な条件は、この型を継承すべきです。
とくに、すべてのエラーはこの型を継承します。

#### `condition-type:error` 〔条件型＋〕

これは抽象型です。すべてのエラーはこの型を継承すべきです。

#### `condition-type:simple-error message irritants` 〔条件型＋〕

これは、`error` 手続きの第1引数が条件でも条件型でもないときに生成される条件です。フィールド
message と irritants は `error` への引数から直接取られます。message はオブジェクト（ふつう
文字列）を含み、irritants はオブジェクトのリストを含みます。この型の報告器は、message と
irritants から出力を生成するのに `format-error-message` を使います。

#### `condition-type:illegal-datum datum` 〔条件型＋〕

これは抽象型です。この型は、プログラムが、特定の必要な性質を欠くオブジェクトを見つける
エラーのクラスを示します。もっともよくあるのは、オブジェクトが誤った型か、特定の範囲の外に
あることです。datum フィールドは問題のオブジェクトを含みます。

#### `condition-type:wrong-type-datum datum type` 〔条件型＋〕

この型は、プログラムが誤った型のオブジェクトを見つけるエラーのクラスを示します。type
フィールドは期待された型を記述する文字列を含み、datum フィールドは誤った型のオブジェクトを
含みます。

```scheme
(error:wrong-type-datum 3.4 "integer")   error>
;The object 3.4 is not an integer.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:wrong-type-datum datum type` 〔手続き＋〕

この手続きは `condition-type:wrong-type-datum` 型の条件を通知します。条件の datum と type
フィールドは、手続きへの対応する引数から埋められます。

#### `condition-type:wrong-type-argument datum type operator operand` 〔条件型＋〕

この型は、手続きが誤った型の引数を渡されたことを示します。operator フィールドは手続き
（またはその手続きを名指すシンボル）を含み、operand フィールドは関わった引数の位置を示し
（このフィールドはシンボル、非負整数、`#f` のいずれかを含みます）、type フィールドは期待
された型を記述する文字列を含み、datum フィールドは問題の引数を含みます。

```scheme
(+ 'a 3)                                 error>
;The object a, passed as the first argument to integer-add,
; is not the correct type.
;To continue, call RESTART with an option number:
; (RESTART 2) => Specify an argument to use in its place.
; (RESTART 1) => Return to read-eval-print level 1.
(list-copy 3)
;The object 3, passed as an argument to list-copy, is not a list.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:wrong-type-argument datum type operator` 〔手続き＋〕

この手続きは `condition-type:wrong-type-argument` 型の条件を通知します。条件の datum、
type、operator フィールドは、手続きへの対応する引数から埋められます。条件の operand
フィールドは `#f` に設定されます。

#### `condition-type:wrong-number-of-arguments datum type operands` 〔条件型＋〕

この型は、手続きが誤った数の引数で呼ばれたことを示します。datum フィールドは呼ばれている
手続きを含み、type フィールドは手続きが受け取る引数の数を含み、operands フィールドは手続き
に渡された引数のリストを含みます。

```scheme
(car 3 4)                                error>
;The procedure car has been called with 2 arguments;
; it requires exactly 1 argument.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:wrong-number-of-arguments datum type operands` 〔手続き＋〕

この手続きは `condition-type:wrong-number-of-arguments` 型の条件を通知します。条件の
datum、type、operands フィールドは、手続きへの対応する引数から埋められます。

#### `condition-type:datum-out-of-range datum` 〔条件型＋〕

この型は、プログラムが、正しい型だが範囲外のオブジェクトを見つけるエラーのクラスを示します。
もっともよくあるのは、この型が、あるデータ構造への添字がその構造の添字の範囲の外にあること
を示すことです。datum フィールドは問題のオブジェクトを含みます。

```scheme
(error:datum-out-of-range 3)             error>
;The object 3 is not in the correct range.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:datum-out-of-range datum` 〔手続き＋〕

この手続きは `condition-type:datum-out-of-range` 型の条件を通知します。条件の datum
フィールドは、手続きへの対応する引数から埋められます。

#### `condition-type:bad-range-argument datum operator operand` 〔条件型＋〕

この型は、手続きが、正しい型だが範囲外の引数を渡されたことを示します。もっともよくあるのは、
この型が、あるデータ構造への添字がその構造の添字の範囲の外にあることを示すことです。operator
フィールドは手続き（またはその手続きを名指すシンボル）を含み、operand フィールドは関わった
引数の位置を示し（このフィールドはシンボル、非負整数、`#f` のいずれかを含みます）、datum
フィールドは問題の引数です。

```scheme
(string-ref "abc" 3)                     error>
;The object 3, passed as the second argument to string-ref,
; is not in the correct range.
;To continue, call RESTART with an option number:
; (RESTART 2) => Specify an argument to use in its place.
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:bad-range-argument datum operator` 〔手続き＋〕

この手続きは `condition-type:bad-range-argument` 型の条件を通知します。条件の datum と
operator フィールドは、手続きへの対応する引数から埋められます。条件の operand フィールドは
`#f` に設定されます。

#### `condition-type:inapplicable-object datum operands` 〔条件型＋〕

この型は、プログラムが手続きでないオブジェクトを適用しようとしたエラーを示します。適用されて
いるオブジェクトは datum フィールドに保存され、オブジェクトに渡されている引数は operands
フィールドにリストとして保存されます。

```scheme
(3 4)                                    error>
;The object 3 is not applicable.
;To continue, call RESTART with an option number:
; (RESTART 2) => Specify a procedure to use in its place.
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `condition-type:file-error filename` 〔条件型＋〕

これは抽象型です。ファイルに結びついたエラーが起こったことを示します。たとえば、存在しない
ファイルを削除しようとするとエラーを通知します。filename フィールドは、失敗した演算に結びつ
いたファイル名またはパス名を含みます。

#### `condition-type:file-operation-error filename verb noun reason operator operands` 〔条件型＋〕

これは、ファイルシステムのエラーのもっともよくある条件型です。filename フィールドは操作
されていたファイル名またはパス名を含みます。verb フィールドは、行われている演算を記述する
動詞または動詞句である文字列を含み、noun フィールドは、操作されているオブジェクトを記述する
名詞または名詞句である文字列を含みます。reason フィールドは、起こったエラーを記述する文字列
を含みます。operator フィールドは演算を行う手続き（またはその手続きを名指すシンボル）を含み、
operands フィールドはその手続きに渡された引数のリストを含みます。たとえば、存在しないファイル
を削除しようとすると、次のフィールド値を持つでしょう。

```text
filename           "/zu/cph/tmp/no-such-file"
verb               "delete"
noun               "file"
reason             "no such file or directory"
operator           file-remove
operands           ("/zu/cph/tmp/no-such-file")
```

そして次のようなメッセージを生成するでしょう。

```scheme
(delete-file "/zu/cph/tmp/no-such-file") error>
;Unable to delete file "/zu/cph/tmp/no-such-file" because:
; No such file or directory.
;To continue, call RESTART with an option number:
; (RESTART 3) => Try to delete the same file again.
; (RESTART 2) => Try to delete a different file.
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:file-operation-error filename verb noun reason operator operands` 〔手続き＋〕

この手続きは `condition-type:file-operation-error` 型の条件を通知します。条件のフィールド
は、手続きへの対応する引数から埋められます。

#### `condition-type:derived-file-error filename condition` 〔条件型＋〕

これはもう1つの種類のファイルエラーで、標準のカテゴリに収まらない分かりにくいファイル
システムのエラーによって生成されます。filename フィールドは操作されていたファイル名または
パス名を含み、condition フィールドはエラーをより詳しく記述する条件を含みます。ふつう
condition フィールドは `condition-type:system-call-error` 型の条件を含みます。

#### `error:derived-file filename condition` 〔手続き＋〕

この手続きは `condition-type:derived-file-error` 型の条件を通知します。条件の filename と
condition フィールドは、手続きへの対応する引数から埋められます。

#### `condition-type:port-error port` 〔条件型＋〕

これは抽象型です。I/O ポートに結びついたエラーが起こったことを示します。たとえば、ファイル
ポートに出力を書くと、ファイルを含むディスクがいっぱいならエラーを通知しえます。そのエラーは
ポートエラーとして通知されます。port フィールドは結びついたポートを含みます。

#### `condition-type:derived-port-error port condition` 〔条件型＋〕

これは、ポートエラーが起こったときに通知される具体型です。port フィールドはエラーに結びつ
いたポートを含み、condition フィールドはエラーをより詳しく記述する条件オブジェクトを含み
ます。ふつう condition フィールドは `condition-type:system-call-error` 型の条件を含みます。

#### `error:derived-port port condition` 〔手続き＋〕

この手続きは `condition-type:derived-port-error` 型の条件を通知します。条件の port と
condition フィールドは、手続きへの対応する引数から埋められます。

#### `condition-type:variable-error location environment` 〔条件型＋〕

これは抽象型です。変数に結びついたエラーが起こったことを示します。location フィールドは変数
の名前を含み、environment フィールドは変数が参照された環境を含みます。

#### `condition-type:unbound-variable location environment` 〔条件型＋〕

この型は、プログラムが束縛されていない変数にアクセスまたは変更しようとしたときに生成され
ます。location フィールドは変数の名前を含み、environment フィールドは参照が起こった環境を
含みます。

```scheme
foo                                      error>
;Unbound variable: foo
;To continue, call RESTART with an option number:
; (RESTART 3) => Specify a value to use instead of foo.
; (RESTART 2) => Define foo to a given value.
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `condition-type:unassigned-variable location environment` 〔条件型＋〕

この型は、プログラムが代入されていない変数にアクセスしようとしたときに生成されます。location
フィールドは変数の名前を含み、environment フィールドは参照が起こった環境を含みます。

```scheme
foo                                      error>
;Unassigned variable: foo
;To continue, call RESTART with an option number:
; (RESTART 3) => Specify a value to use instead of foo.
; (RESTART 2) => Set foo to a given value.
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `condition-type:arithmetic-error operator operands` 〔条件型＋〕

これは抽象型です。数値演算が算術エラー（たとえばゼロ除算）のために完了できなかったことを
示します。operator フィールドは演算を実装する手続き（またはその手続きを名指すシンボル）を
含み、operands フィールドは手続きに渡された引数のリストを含みます。

#### `condition-type:divide-by-zero operator operands` 〔条件型＋〕

この型は、プログラムがゼロで割ろうとしたときに生成されます。operator フィールドは失敗した
演算を実装する手続き（またはその手続きを名指すシンボル）を含み、operands フィールドは手続き
に渡された引数のリストを含みます。

```scheme
(/ 1 0)
;Division by zero signalled by /.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:divide-by-zero operator operands` 〔手続き＋〕

この手続きは `condition-type:divide-by-zero` 型の条件を通知します。条件の operator と
operands フィールドは、手続きへの対応する引数から埋められます。

#### `condition-type:floating-point-overflow operator operands` 〔条件型＋〕

この型は、プログラムが浮動小数点のオーバーフローになる算術演算を行ったときに生成されます。
operator フィールドは演算を実装する手続き（またはその手続きを名指すシンボル）を含み、
operands フィールドは手続きに渡された引数のリストを含みます。

#### `condition-type:floating-point-underflow operator operands` 〔条件型＋〕

この型は、プログラムが浮動小数点のアンダーフローになる算術演算を行ったときに生成されます。
operator フィールドは演算を実装する手続き（またはその手続きを名指すシンボル）を含み、
operands フィールドは手続きに渡された引数のリストを含みます。

#### `condition-type:primitive-procedure-error operator operands` 〔条件型＋〕

これは抽象型です。基本手続きの呼び出しによってエラーが生成されたことを示します。基本手続き
は、Scheme ではなく Scheme 実装の基礎となる言語で書かれている点で、ふつうの手続きと区別され
ます。operator フィールドは演算を実装する手続き（またはその手続きを名指すシンボル）を含み、
operands フィールドは手続きに渡された引数のリストを含みます。

#### `condition-type:system-call-error operator operands system-call error-type` 〔条件型＋〕

これは、基本手続きが生成するもっともよくある条件型です。この型の条件は、基本手続きが
オペレーティングシステムへのシステムコールを行い、そのシステムコールがエラーを通知したこと
を示します。システムコールのエラーはこの型の条件として Scheme に反映されますが、多くのよく
あるシステムコールのエラーは、Scheme の実装によってより有用な形に自動的に翻訳されます。たと
えば、ファイルを削除しようとしているあいだに起こるシステムコールのエラーは、
`condition-type:file-operation-error` 型の条件に翻訳されます。operator フィールドは演算を
実装する手続き（またはその手続きを名指すシンボル）を含み、operands フィールドは手続きに
渡された引数のリストを含みます。system-call と error-type フィールドは、それぞれ行われて
いた特定のシステムコールと起こったエラーを記述するシンボルを含みます。これらのシンボルは
完全にオペレーティングシステム依存です。

#### `condition-type:control-error` 〔条件型＋〕

これは抽象型です。プログラムの制御の流れに関するエラーのクラスを記述します。

#### `condition-type:no-such-restart name` 〔条件型＋〕

この型は、名前付き再起動が、有効であると期待されたときに有効でなかったことを示します。この
型の条件は、`muffle-warning` のような、特定の名前付き再起動を探すいくつかの手続きが通知
します。name フィールドは探されていた名前を含みます。

```scheme
(muffle-warning)                         error>
;The restart named muffle-warning is not bound.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `error:no-such-restart name` 〔手続き＋〕

この手続きは `condition-type:no-such-restart` 型の条件を通知します。条件の name フィールド
は、手続きへの対応する引数から埋められます。

#### `condition-type:not-loading` 〔条件型＋〕

この型の条件は、手続き `current-load-pathname` が、読み込まれているファイルの内側以外の
どこかから呼ばれたときに生成されます。

```scheme
(current-load-pathname)                  error>
;No file being loaded.
;To continue, call RESTART with an option number:
; (RESTART 1) => Return to read-eval-print level 1.
```

#### `condition-type:warning` 〔条件型＋〕

これは抽象型です。すべての警告はこの型を継承すべきです。警告は、ふつうユーザに条件を知らせ
て計算をふつうに進めることで処理される条件のクラスです。

#### `condition-type:simple-warning message irritants` 〔条件型＋〕

これは、`warn` 手続きが生成する条件です。フィールド message と irritants は `warn` への引数
から直接取られます。message はオブジェクト（ふつう文字列）を含み、irritants はオブジェクトの
リストを含みます。この型の報告器は、message と irritants から出力を生成するのに
`format-error-message` を使います。

#### `condition-type:simple-condition message irritants` 〔条件型＋〕

これは、標準の条件クラスのどれにも収まらない、特殊化されていない条件です。message フィールド
はオブジェクト（ふつう文字列）を含み、irritants はオブジェクトのリストを含みます。この型の
報告器は、message と irritants から出力を生成するのに `format-error-message` を使います。

#### `condition-type:breakpoint environment message prompt` 〔条件型＋〕

この型の条件はブレークポイントの仕組みが生成します。そのフィールドの内容は本文書の範囲を
超えます。
