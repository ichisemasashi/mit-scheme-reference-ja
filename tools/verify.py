# -*- coding: utf-8 -*-
"""訳文の構造を原文と突き合わせる。

  python3 tools/verify.py ja/01-functions-and-data.md src/01-functions-and-data.txt

原文を省くと、訳し残しと異言語混入の走査だけを行う。
"""
import re
import sys
import unicodedata

JA = re.compile(r'[ぁ-んァ-ヴー一-龥々]')
FOREIGN = re.compile(r'[а-яА-Я가-힣ᄀ-ᇿㄱ-ㆎ]')
# 訳出対象外として許してよい英語（人名・製品名・コード片など）
ALLOW = re.compile(r'Lisp|Common|Scheme|Emacs|Java|Python|MIT|CLOS|ANSI|'
                   r'Touretzky|Steele|Sussman|Hanson|McCarthy')


def width(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)


def strip_quote(s):
    """引用の中のコードもコードとして扱う。練習問題は > で引用しているので、
    これを剥がさないとフェンスが追えず、中のコードが訳し残しと誤報される"""
    while True:
        t = re.sub(r'^(\s*)>\s?', r'\1', s)
        if t == s:
            return s
        s = t


def kind(s):
    t = s.strip()
    if not t:
        return '_'
    if t.startswith('```'):
        return 'F'
    if re.match(r'^#{1,6}\s', t):
        return 'H'
    if re.match(r'^([*+-]\s|\d+\.\s)', t):
        return 'L'
    return 'P'


def main(ja_path, src_path=None):
    L = open(ja_path, encoding='utf-8').read().split('\n')
    ok = True

    print(f"{ja_path}: {len(L)-1}行  空行{sum(1 for l in L if not l.strip())}")

    if src_path:
        S = open(src_path, encoding='utf-8').read().split('\n')
        same = len(L) == len(S)
        print(f"  行数 {len(L)-1}/{len(S)-1}  {'一致' if same else '不一致'}")
        if not same:
            ok = False
        b0 = [i for i, l in enumerate(S) if not l.strip()]
        b1 = [i for i, l in enumerate(L) if not l.strip()]
        if b0 != b1:
            print(f"  空行の位置が違う: {sorted(set(b0) ^ set(b1))[:10]}")
            ok = False
        a, b = ''.join(map(kind, L)), ''.join(map(kind, S))
        print(f"  行種の並び {'完全一致' if a == b else '不一致'}")
        if a != b:
            ok = False
        for label, pat in [("コードフェンス", r'^```'), ("リンク", r'\]\(')]:
            n1 = sum(len(re.findall(pat, l)) for l in L)
            n0 = sum(len(re.findall(pat, l)) for l in S)
            print(f"  {label} {n1}/{n0}  {'一致' if n1 == n0 else '不一致'}")
            if n1 != n0:
                ok = False

    # 開きと閉じが交互に並んでいるか。分割して訳しているとページ跨ぎのコードで
    # 閉じフェンスが余りやすく、それ以降の走査がすべて内外反転する
    st = None
    bad = []
    for i, l in enumerate(L, 1):
        l = strip_quote(l).lstrip()
        if not l.startswith('```'):
            continue
        opening = len(l.strip()) > 3
        if st is None:
            if not opening:
                bad.append((i, '閉じが先行'))
            st = i
        else:
            if opening:
                bad.append((i, f'{st}行が閉じられていない'))
            st = None
    if st is not None:
        bad.append((st, '閉じられていない'))
    print(f"  コードフェンスの対応 {'正しい' if not bad else '崩れている'}")
    for i, why in bad[:5]:
        print(f"    {i}| {why}")
    if bad:
        ok = False

    inf = False
    left = []
    for i, l in enumerate(L, 1):
        if strip_quote(l).lstrip().startswith('```'):
            inf = not inf
            continue
        l = strip_quote(l)
        if inf or not l.strip() or JA.search(l):
            continue
        s = re.sub(r'`[^`]*`|\[[^\]]*\]\([^)]*\)|https?://\S+|<[^>]+>', '', l)
        s = ALLOW.sub('', s)
        if re.search(r'\b[a-z]{3,}\b(\s+\b[a-z\']{2,}\b){2,}', s):
            left.append((i, l))
    print(f"  訳し残しの英語散文 {len(left)}行")
    for i, l in left[:10]:
        print(f"    {i}| {l[:72]}")
    if left:
        ok = False

    fo = [i for i, l in enumerate(L, 1) if FOREIGN.search(l)]
    print(f"  異言語の混入 {len(fo)}行 {fo[:8] if fo else ''}")
    if fo:
        ok = False

    over = [(i, width(l)) for i, l in enumerate(L, 1) if width(l) > 100]
    if over:
        print(f"  表示幅100超 {len(over)}行 {over[:5]}")

    print("  => " + ("OK" if ok else "要確認"))
    return 0 if ok else 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
