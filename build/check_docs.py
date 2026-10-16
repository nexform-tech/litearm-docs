#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查手册正文引用的图片是否都在仓库里。

读四份手册的 markdown（中英文各两份）和已提交的 manual_site/index.html，把
LITEARM_SE_images/ 形式的引用一条条解析成真实路径，逐个确认文件存在。

英文手册引用 safety/en/ 与 litearm_studio/en/ 下的英文图，与中文手册引用的
不是同一批文件，所以两份都要查。

用途：图片改名、漏拷、或删图而没改正文时，这里会红 —— 排版流程不会报错，只是
PDF 和站点里少一张图，人工评审很难发现。

用法：python3 build/check_docs.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (待检查的文件, 该文件的引用相对谁解析)
TARGETS = [
    ("LITEARM_SE产品手册.md", ROOT),
    ("LITEARM SE软件开发手册.md", ROOT),
    ("LITEARM-SE-product-manual.md", ROOT),
    ("LITEARM-SE-software-development-manual.md", ROOT),
    (os.path.join("manual_site", "index.html"), os.path.join(ROOT, "manual_site")),
]

# 引用出现在 markdown 图片语法 ![](...) 里，也出现在 ```{=latex} 块的
# \includegraphics{...} 里；站点里的引用还带 ../ 前缀。
REF_RE = re.compile(r"(?:\.\./)*LITEARM_SE_images/[A-Za-z0-9_./-]+\.(?:png|jpe?g|webp|svg|gif)")


def refs_in(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return sorted(set(REF_RE.findall(f.read())))


def main():
    checked = 0
    problems = []
    for path, base in TARGETS:
        if not os.path.isfile(os.path.join(ROOT, path)):
            problems.append("missing file: %s" % path)
            continue
        for ref in refs_in(path):
            checked += 1
            resolved = os.path.normpath(os.path.join(base, ref))
            if not os.path.isfile(resolved):
                problems.append("%s -> %s" % (path, ref))

    print("checked %d image reference(s) across %d file(s)" % (checked, len(TARGETS)))
    if problems:
        print("\nunresolved:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
