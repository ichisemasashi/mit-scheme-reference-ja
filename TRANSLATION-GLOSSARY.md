# 用語集と翻訳方針 — MIT Scheme リファレンス・マニュアル

訳語を記憶ではなくこのファイルで担保する。新しく訳語を決めたら、ここに追記して
から使う。実際に使った訳語だけを載せる（先回りで「使いそうな語」を入れない）。

## 底本

*MIT Scheme Reference Manual*, Edition 1.94, for Scheme Release 7.5, 2001年。
原著PDFから `pdftotext` で抽出し、`tools/split.py` で章ごとに分けたものを底本と
する。これは現行の MIT/GNU Scheme（12.x 系）のマニュアルではなく、2001年の版で
あることに注意する。SDF（『Software Design for Flexibility』）が読者に薦めるのは
現行版だが、手元にあるのはこの版なので、この版を訳す。

### 抽出の傷（底本を読むときの注意）

- **ページの柱**（`Chapter 1: Overview   11` や `12   MIT Scheme Reference`）は
  `tools/split.py` で除いてある
- **行末のハイフン分割**（`mu-` 改行 `tation`）は底本に残っている。訳すときに
  1語として読む
- **コード周りの引用符** — Texinfo の `@code{}`・`@samp{}` が、抽出では
  `‘...’`（曲がった引用符）になる。これは原文がコードとして示した部分の目印。
  訳文では Markdown のコードスパン `` `...` `` にする
- **評価の矢印** `⇒` は原文の `@result{}`。訳文でもそのまま `⇒` を使う
- **`Revised^4`** のような上付きは失われる。`Revised^4 Report` は
  「Revised⁴ Report（R4RS）」と書く

## 訳すもの・訳さないもの

### 訳さない（既定）

| 対象 | 例 |
|---|---|
| コード本体、識別子、手続き名、特殊形式名 | `car`、`call-with-current-continuation`、`let` |
| コードの出力例、評価結果 | `⇒ ("Hi" "max" 3)` |
| 型・条件型の名前 | `condition-type:wrong-number-of-arguments` |
| 言語名・処理系名・規格名 | Scheme、MIT Scheme、R4RS、IEEE、ASCII、Unicode |
| 人名・機関名 | Chris Hanson、MIT、Free Software Foundation |
| ライセンス名 | GNU Free Documentation License |

### 訳す

- 本文の説明、注記、例の前後の説明文
- エントリ（手続き・特殊形式・変数）の**説明本文**。シグネチャ行は訳さない

## エントリの書式

このマニュアルの中心は、Texinfo の `@deffn` 由来のエントリである。底本では
シグネチャが左、分類が右寄せで現れる。

```
lambda formals expression expression . . .                          special form
      A lambda expression evaluates to a procedure. ...
```

訳文では次の形にする。**シグネチャは見出しのコードスパンに入れて訳さず**、分類を
〔〕で添え、説明を続ける。

```markdown
#### `lambda formals expression expression …` 〔特殊形式〕

lambda 式は手続きに評価される。……
```

分類語は6種。末尾の `+` は **MIT Scheme の拡張**（R4RS にない）を表す、というのが
原著 1.1.3 の規約である。`+` なしは R4RS で定義されている項目を指す。訳では `+` を
`＋` として残し、その意味は第1章 1.1.3 で説明する。

| 原文（右寄せの分類） | 訳 | 意味 |
|---|---|---|
| procedure | 〔手続き〕 | R4RS の手続き |
| procedure+ | 〔手続き＋〕 | MIT Scheme が加えた手続き |
| special form | 〔特殊形式〕 | R4RS の特殊形式 |
| special form+ | 〔特殊形式＋〕 | MIT Scheme が加えた特殊形式 |
| variable | 〔変数〕 | R4RS の変数 |
| variable+ | 〔変数＋〕 | MIT Scheme が加えた変数 |

## 確定した訳語

### Scheme の基本概念

| 原語 | 訳語 | 備考 |
|---|---|---|
| expression | 式 | |
| evaluate | 評価する | |
| procedure | 手続き | 「関数」ではなく「手続き」。Scheme の用語法に従う |
| special form | 特殊形式 | |
| binding | 束縛 | |
| environment | 環境 | |
| closing environment | 閉包環境 | lambda が作られたときの環境 |
| invocation environment | 呼び出し環境 | |
| formal parameter | 仮引数 | |
| lambda list | ラムダリスト | |
| argument | 引数 | |
| required parameter | 必須引数 | |
| optional parameter | 省略可能引数 | `#!optional` |
| rest parameter | 残余引数 | `#!rest` |
| default object | デフォルトオブジェクト | 省略された省略可能引数に束縛される特別な対象 |
| predicate | 述語 | 真偽値を返す手続き。名前が `?` で終わる慣習 |
| mutation procedure | 変更手続き | データ構造を書き換える。名前が `!` で終わる慣習 |
| boolean | 真偽値 | |
| true / false | 真／偽 | |
| symbol | シンボル | |
| pair | ペア | |
| list | リスト | |
| vector | ベクタ | |
| string | 文字列 | |
| character | 文字 | |

### 字句・記法

| 原語 | 訳語 | 備考 |
|---|---|---|
| identifier | 識別子 | |
| syntactic keyword | 構文キーワード | |
| delimiter | 区切り文字 | |
| whitespace | 空白 | |
| comment | コメント | |
| external representation | 外部表現 | |
| literal | リテラル | |
| case-insensitive | 大文字小文字を区別しない | |
| naming convention | 命名規約 | |

## 文体

- 本文・説明文は敬体（です・ます調）
- 見出し・箇条書きの項目は体言止めまたは常体
- 脚注があれば常体（〜である）
- 英数字・記号は半角。英数と日本語のあいだに空白を入れない（例外: コードスパンの
  前後には空白を置く。読みやすさのため）
- 日本語文中の括弧は全角（）、引用符は「」。ただしエントリの分類は〔〕で囲む

## 進捗

| 章 | 訳題 | 状態 |
|---|---|---|
| 前付け | 前付け（表題・謝辞・許諾表示） | 完了 |
| 1 | 概観 | 完了 |
| 2 | 特殊形式 | — |
| 3 | 同値述語 | — |
| 4 | 数 | — |
| 5 | 文字 | — |
| 6 | 文字列 | — |
| 7 | リスト | — |
| 8 | ベクタ | — |
| 9 | ビット列 | — |
| 10 | その他のデータ型 | — |
| 11 | 連想 | — |
| 12 | 手続き | — |
| 13 | 環境 | — |
| 14 | 入出力 | — |
| 15 | オペレーティングシステムインタフェース | — |
| 16 | エラーシステム | — |
| 17 | グラフィックス | — |
| 18 | Win32 パッケージリファレンス | — |
