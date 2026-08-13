# -*- coding: utf-8 -*-
"""訳文そのものの傷を走査する。原文とは突き合わせない。

  python3 tools/lint-ja.py ja/*.md
  python3 tools/lint-ja.py --self-test

`verify.py` が構造（行数・フェンス・リンク）を見るのに対し、こちらは日本語の
中身を見る。狙いは**一括置換の後始末**である。

Software Design for Flexibility の翻訳では、原文由来の問題7件に対して、自分で
壊した箇所が25件あった。敬体から常体への一括変換、ページ参照の一括削除、記号の
一括置換。どれも本文をまとめて書き換えたあとの取りこぼしである。

同じ失敗を3度繰り返した原因ははっきりしている。**壊れ方の型を想像で列挙して
確認していた**ことだ。第5章では14件を2回に分けて直しており、1回目は「働きる」
「使いる」など思いついた語幹だけを探して8件を取りこぼした。2回目に文法の形
（五段連用形＋る）で網羅的に走査して、ようやく残存0を確認できた。

そこでこの道具は、語彙ではなく**文法の形**で走査する。
"""
import re
import sys
import glob

JA = r'[ぁ-んァ-ヴー一-龥々]'

# --- 検査1: 五段動詞の活用の破壊 ------------------------------------------
#
# 敬体→常体の一括変換で「働きます」が「働きる」になる。五段動詞の常体は
# 「働く」であって、連用形に「る」は付かない。
#
# 素朴に「連用形＋る」を引くと一段動詞（起きる・足りる）と補助的な語尾
# （〜できる・〜すぎる・〜てみる）が大量に引っかかる。実際の訳文を数えたところ、
# この形は83種あり、その大半が「〜できる」だった。よって両者を除いてから引く。
# 「い」を含めるのは、う段の五段動詞（使う・言う・買う）の連用形が「い」だから。
# これを落とすと「使いる」が素通りする（実際に取りこぼした）。
GODAN = re.compile(r'[一-龥々][ぁ-ん]{0,2}[きぎしちにびみりい]る')
# 補助的な語尾。語幹ではなく直前の1〜2字で判別できる。
# 「てい／でい」は進行の「〜ている」。これを除かないと「見ている」が誤検出される
# 「[助詞]＋いる」は存在の「居る」。「段にいる」「そこにいる」を誤検出しないため
AUX = re.compile(r'(でき|すぎ|てみ|ておき|ていき|でみ|てい|でい|[にがはもとでを]い)る$')
# 一段動詞。閉じた小さな集合なので列挙してよい
ICHIDAN = {
    '起きる', '生きる', '飽きる', '尽きる', '突きる', '足りる', '借りる',
    '降りる', '下りる', '懲りる', '伸びる', '延びる', '浴びる', '帯びる',
    '詫びる', '落ちる', '満ちる', '朽ちる', '過ぎる', '報いる', '用いる',
    '強いる', '率いる', '老いる', '悔いる',
}

# --- 検査2: サ変の取り違え -------------------------------------------------
#
# 同じ一括変換で「返します」が「返する」になる。五段動詞「返す」の連用形に
# 「する」を付けてしまう誤り。サ変動詞の語幹はほぼ漢字2字以上なので、
# 漢字1字＋する を疑い、正当なものだけ除く。
SAHEN1 = re.compile(r'(?<![一-龥々])([一-龥])する')
SAHEN_OK = {
    '関', '反', '適', '面', '察', '属', '帰', '期', '価', '介', '因',
    '達', '接', '課', '訳', '要', '証', '生', '死', '愛', '解', '和',
    '対', '乗', '徹', '任', '模', '博',
    # 「〜化する」は生産的な接尾辞。カタカナ＋化する（モデル化する）は否定先読みを
    # すり抜けるので明示的に許す。「視する」「類する」も同様
    '化', '視', '類',
}

# --- 検査3: 文体の混在 -----------------------------------------------------
#
# 本文は敬体、練習問題と脚注は常体。一括変換は本文だけを対象にしがちで、
# 脚注が敬体のまま残る。
#
# **練習問題は対象にしない。** 始まりは「### 練習問題」で分かるが、終わりに
# 印がなく、本文は見出しなしで再開するため、区切りを機械で決められない。
# SDF で試したところ、練習問題の直後の本文を練習問題と誤って数え、10件の
# 誤検出を出した。誤検出の多い検査は読み飛ばされる。それが25件を見逃した
# 原因そのものなので、確実に区切れる脚注だけを見る。
KEITAI = re.compile(r'(ます|ました|ません|です|でした|でしょう)[。、）」]|'
                    r'(ます|です)$')

# --- 検査4: コード span の字間 ---------------------------------------------
#
# ページ参照の一括削除で「`foo` の定義（123ページ）を見よ」から括弧を外すと、
# 前後の空白まで巻き込んで「`foo`の定義」と詰まる。SDF では空白ありが1752箇所、
# なしが0箇所で、約束は統一されていた。
SPACING = re.compile(r'`[^`\n]+`(?=' + JA + r')|(?<=' + JA + r')`[^`\n]+`')


def blocks(lines):
    """行ごとに、そこが本文か脚注かコードかを返す。

    脚注は [^N]: で始まり、次の見出しまで続く。章の末尾にまとめてあることが
    多いが、SDF の前付けのように本文の途中に置かれ、次の見出しから本文に
    戻る場合もある。見出しを終わりの印として扱う。
    """
    mode = []
    cur = 'body'
    in_fence = False
    for l in lines:
        s = re.sub(r'^\s*>\s?', '', l)
        if s.lstrip().startswith('```'):
            in_fence = not in_fence
            mode.append('fence')
            continue
        if in_fence:
            mode.append('fence')
            continue
        if re.match(r'^\[\^[^\]]+\]:', s):
            cur = 'note'
        elif re.match(r'^#{1,6}\s', s):
            cur = 'body'
        mode.append(cur)
    return mode


def check(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    mode = blocks(lines)
    hits = []

    for i, (l, m) in enumerate(zip(lines, mode), 1):
        if m == 'fence':
            continue
        body = re.sub(r'`[^`\n]*`', '', l)  # コード span の中は日本語ではない

        for w in GODAN.findall(body):
            if AUX.search(w) or w in ICHIDAN:
                continue
            hits.append((i, '活用', f'{w} — 五段動詞に「る」が付いている'))

        for k in SAHEN1.findall(body):
            if k not in SAHEN_OK:
                hits.append((i, '活用', f'{k}する — サ変でない語に「する」が付いている'))

        if m == 'note':
            mk = KEITAI.search(body)
            if mk:
                hits.append((i, '文体', f'{mk.group(0)} — 脚注は常体'))

        for s in SPACING.findall(l):
            hits.append((i, '字間', f'{s} — コード span と日本語が詰まっている'))

    return hits


SELF_TEST = [
    # (行, 期待する検出の種別)  実際に SDF で作り込んだ傷から取った
    ('この手続きは環境の中で働きる。', '活用'),
    ('引数をそのまま返する。', '活用'),
    ('第2引数として渡された値を使いる。', '活用'),
    ('これは正しく起きる現象である。', None),
    ('この式は評価できる。', None),
    ('単純すぎる仮定は危うい。', None),
    ('総称手続きを実行する。', None),
    ('この点に関する議論は次章に譲る。', None),
    ('`assoc` の定義を見よ。', None),
    ('`assoc`の定義を見よ。', '字間'),
]


def self_test():
    bad = 0
    for text, want in SELF_TEST:
        import tempfile, os
        fd, p = tempfile.mkstemp(suffix='.md')
        os.write(fd, text.encode('utf-8'))
        os.close(fd)
        got = {k for _, k, _ in check(p)}
        os.unlink(p)
        ok = (want in got) if want else not got
        if not ok:
            bad += 1
        print(f"  {'OK ' if ok else '失敗'} {text}  → {got or '検出なし'}")
    print(f"自己検査 {len(SELF_TEST)-bad}/{len(SELF_TEST)}")
    return 1 if bad else 0


def main(paths):
    total = 0
    for p in paths:
        h = check(p)
        total += len(h)
        print(f"{p}: {len(h)}件")
        for i, kind, why in h[:20]:
            print(f"    {i}| [{kind}] {why}")
        if len(h) > 20:
            print(f"    ... 他{len(h)-20}件")
    print(f"=> 合計 {total}件")
    return 1 if total else 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == '--self-test':
        sys.exit(self_test())
    files = [f for a in sys.argv[1:] for f in glob.glob(a)]
    sys.exit(main(files))
