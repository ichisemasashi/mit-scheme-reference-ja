# -*- coding: utf-8 -*-
"""底本（pdftotext の全文）をページ装飾を除いて章ごとに分ける。

  python3 tools/split.py

読み書き用の中間ファイルを src/NN-slug.txt に書く。これらは機械抽出であり
公開しない（.gitignore で /src/ を除外）。翻訳の底本として手元で読むだけに使う。

ページ装飾とは、Texinfo が各ページの上下に入れる次の行を指す。

  Chapter 1: Overview                                     11   （奇数ページの柱）
  12                                MIT Scheme Reference        （偶数ページの柱）

これらは本文ではないので落とす。行末のハイフン分割（mu-\ntation）は、この段階では
つながず残す。訳文は英文を1行ずつ置き換えるのではなく読んで書き起こすので、
つなぐ必要がない。むしろ元の姿を保つほうが、原文を照合するとき行がずれない。
"""
import re

SRC = 'src/full.txt'

# 章の大見出し（^N Title、ページ番号を伴わない）。行番号は split() で確かめる
CHAPTERS = [
    (1, 'overview', 'Overview'),
    (2, 'special-forms', 'Special Forms'),
    (3, 'equivalence-predicates', 'Equivalence Predicates'),
    (4, 'numbers', 'Numbers'),
    (5, 'characters', 'Characters'),
    (6, 'strings', 'Strings'),
    (7, 'lists', 'Lists'),
    (8, 'vectors', 'Vectors'),
    (9, 'bit-strings', 'Bit Strings'),
    (10, 'misc-datatypes', 'Miscellaneous Datatypes'),
    (11, 'associations', 'Associations'),
    (12, 'procedures', 'Procedures'),
    (13, 'environments', 'Environments'),
    (14, 'io', 'Input/Output'),
    (15, 'os-interface', 'Operating-System Interface'),
    (16, 'error-system', 'Error System'),
    (17, 'graphics', 'Graphics'),
    (18, 'win32', 'Win32 Package Reference'),
]

# ページの柱。奇数ページ = 「Chapter N: Title    page」、偶数ページ = 「page    MIT Scheme Reference」
HEADER_ODD = re.compile(r'^Chapter \d+: .+?\s+\d+\s*$')
HEADER_EVEN = re.compile(r'^\d+\s+MIT Scheme Reference\s*$')
# 章の大見出しそのもの
HEAD = re.compile(r'^(1[0-8]|[1-9]) ([A-Z].*)$')


def clean(lines):
    out = []
    for l in lines:
        if HEADER_ODD.match(l) or HEADER_EVEN.match(l):
            continue
        out.append(l.rstrip('\n'))
    # 柱を抜いた跡に空行が3つ以上続くことがある。2つまでに詰める
    res = []
    blank = 0
    for l in out:
        if l.strip():
            blank = 0
            res.append(l)
        else:
            blank += 1
            if blank <= 2:
                res.append(l)
    return res


def main():
    lines = open(SRC, encoding='utf-8').read().split('\n')
    # 各章の開始行を大見出しで探す
    starts = {}
    for i, l in enumerate(lines):
        m = HEAD.match(l)
        if m:
            n = int(m.group(1))
            title = m.group(2).strip()
            # 目次や参照でなく、章題そのもの（既知の題と一致）だけ拾う
            for cn, slug, ct in CHAPTERS:
                if cn == n and title == ct and n not in starts:
                    starts[n] = i
    # 本体の終わり = GFDL ライセンス節の開始
    end = next(i for i, l in enumerate(lines)
               if l.strip() == 'GNU Free Documentation License')

    order = sorted(starts)
    bounds = []
    for k, n in enumerate(order):
        s = starts[n]
        e = starts[order[k + 1]] if k + 1 < len(order) else end
        bounds.append((n, s, e))

    for (n, slug, title), (nn, s, e) in zip(CHAPTERS, bounds):
        assert n == nn, (n, nn)
        body = clean(lines[s:e])
        path = f'src/{n:02d}-{slug}.txt'
        open(path, 'w', encoding='utf-8').write('\n'.join(body) + '\n')
        print(f'{path}  {len(body)}行  ({title})')

    # 前付け（先頭〜第1章の手前）と GFDL 節も切り出しておく
    front = clean(lines[:starts[1]])
    open('src/00-front.txt', 'w', encoding='utf-8').write('\n'.join(front) + '\n')
    print(f'src/00-front.txt  {len(front)}行  (前付け)')
    gfdl_end = next(i for i, l in enumerate(lines)
                    if l.strip() == 'Binding Index' and i > end)
    lic = clean(lines[end:gfdl_end])
    open('src/99-gfdl.txt', 'w', encoding='utf-8').write('\n'.join(lic) + '\n')
    print(f'src/99-gfdl.txt  {len(lic)}行  (GFDL)')


if __name__ == '__main__':
    main()
