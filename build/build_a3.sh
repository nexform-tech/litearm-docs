#!/usr/bin/env bash
# Rebuild the LITEARM SE manual PDFs from their Markdown sources.
#
# Pipeline, per manual: Markdown -> pandoc (TeX) -> zebra.py / breaktt.py
# post-processing -> three xelatex passes. The PDF lands in the repository root,
# next to its source; the intermediate .tex/.aux/.log/.toc files land there too
# and are git-ignored.
#
# Each manual is built in a language: the Chinese sources need xeCJK and the
# pinned CJK font, the English ones must not load xeCJK at all. build_one takes
# the language and substitutes the matching strings into a3_layout.tex.
#
# Usage:
#   bash build/build_a3.sh                            # all four manuals
#   bash build/build_a3.sh LITEARM_SE产品手册          # one of them
#   bash build/build_a3.sh LITEARM-SE-product-manual
#
# Requirements: pandoc, xelatex (TeX Live with xeCJK and tikz), python3, and the
# CJK fonts described in the repository README. The English manuals need DejaVu
# Sans Mono, which ships with Linux distributions and with TeX Live's font set.
set -e

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
B="$ROOT/build"
SRC="$ROOT"
GEN="$B/gen"
mkdir -p "$GEN"
WANT="${1:-}"

# a3_layout.tex pins the CJK font by absolute path, because letting the system
# pick a Noto Serif CJK face can resolve to the Japanese one and change glyphs.
# Point LITEARM_CJK_FONT_DIR elsewhere when the single-region files live
# somewhere other than the default location.
CJK_FONT_DIR="${LITEARM_CJK_FONT_DIR:-$HOME/.local/share/fonts/NotoSerifSC}"
if [ ! -f "$CJK_FONT_DIR/NotoSerifCJKSC-Regular.otf" ]; then
  echo "CJK font not found: $CJK_FONT_DIR/NotoSerifCJKSC-Regular.otf" >&2
  echo "Set LITEARM_CJK_FONT_DIR to the directory holding the Noto Serif CJK SC single-region .otf files." >&2
  exit 1
fi

# Per-language strings substituted into a3_layout.tex. The Chinese sources are
# typeset by xeCJK against the pinned font file; the English ones load no CJK
# package at all and only swap the monospace font, because the directory-tree
# and link diagrams use U+2500 box drawing that Latin Modern Mono lacks.
build_layout () {   # in-layout, out-layout, lang, docshort, style
  python3 - "$1" "$2" "$3" "$4" "$5" "$CJK_FONT_DIR" <<'PY'
import os, sys

src, dst, lang, docshort, style, cjkdir = sys.argv[1:7]

BY_LANG = {
    "zh": {
        "language": '\\XeTeXlinebreaklocale "zh"\n\\XeTeXlinebreakskip = 0pt plus 1pt',
        "cjkfont": ("\\setCJKmainfont[Path=@CJKFONTDIR@,\n"
                    "  UprightFont=NotoSerifCJKSC-Regular.otf,\n"
                    "  BoldFont=NotoSerifCJKSC-Bold.otf]{LITEARM CJK SC}"),
        "contentsname": "目录",
        "captionlabel": "图#2. ",
        "figname": "图",
    },
    "en": {
        "language": "% No CJK line breaking: this edition is Latin text.",
        "cjkfont": "\\setmonofont{DejaVu Sans Mono}",
        "contentsname": "Contents",
        "captionlabel": "Figure #2. ",
        "figname": "Figure",
    },
}

try:
    strs = BY_LANG[lang]
except KeyError:
    raise SystemExit("unknown language: %s" % lang)

sub = {
    "@DOCLANGUAGEBLOCK@": strs["language"],
    "@CJKFONTBLOCK@": strs["cjkfont"],
    "@CJKFONTDIR@": os.path.join(cjkdir, ""),
    "@CONTENTSNAME@": strs["contentsname"],
    "@CAPTIONLABEL@": strs["captionlabel"],
    "@FIGNAME@": strs["figname"],
    "@DOCSHORT@": docshort,
}

t = open(src, encoding="utf-8").read()

# A placeholder inside a TeX comment is a trap: the substituted blocks are
# multi-line, so one landing after a % ends the comment and the rest of the
# block becomes live TeX in the preamble. That fails as "Missing
# \begin{document}" pointing at a line the author never wrote.
for lineno, line in enumerate(t.splitlines(), 1):
    code = line.split("%", 1)[0]
    for key in sub:
        if key in line and key not in code:
            raise SystemExit("%s:%d: %s appears inside a comment" % (src, lineno, key))

# Two passes: the substituted blocks may themselves carry a placeholder.
for _ in range(2):
    for key, value in sub.items():
        t = t.replace(key, value)

leftover = [k for k in sub if k in t]
if leftover:
    raise SystemExit("%s: unsubstituted %s" % (src, ", ".join(leftover)))

# Append the per-document style fragment, e.g. the product manual's table alignment.
if style and os.path.isfile(os.path.join(os.path.dirname(src), style)):
    t += "\n" + open(os.path.join(os.path.dirname(src), style), encoding="utf-8").read()

open(dst, "w", encoding="utf-8").write(t)
PY
}

build_one () {
  name="$1"; docshort="$2"; lang="$3"; style="${4:-}"
  if [ -n "$WANT" ] && [ "$WANT" != "$name" ]; then
    return 0
  fi
  echo "===== build $name ($lang) ====="

  case "$lang" in
    zh) emojifig="图" ;;
    en) emojifig="Figure" ;;
    *) echo "unknown language: $lang" >&2; return 1 ;;
  esac

  # Drop the emoji the PDF cannot typeset; the Markdown keeps them for the site.
  python3 - "$SRC/$name.md" "$GEN/$name.md" "$emojifig" <<'PY'
import sys
t = open(sys.argv[1], encoding="utf-8").read()
for a, b in (("✅", "✓"), ("⚠️", "⚠"), ("📐", sys.argv[3]), ("️", "")):
    t = t.replace(a, b)
open(sys.argv[2], "w", encoding="utf-8").write(t)
PY

  build_layout "$B/a3_layout.tex" "$GEN/layout_$name.tex" "$lang" "$docshort" "$style"

  cjk_vars=()
  if [ "$lang" = zh ]; then
    cjk_vars=(-V CJKmainfont="Noto Serif CJK SC" -V CJKsansfont="Noto Sans CJK SC"
              -V CJKmonofont="Noto Sans Mono CJK SC")
  fi

  pandoc "$GEN/$name.md" -o "$GEN/$name.tex" \
    --pdf-engine=xelatex --include-in-header="$GEN/layout_$name.tex" --columns=50 \
    -N \
    -V mainfont="Lato" -V sansfont="Lato" -V monofont="Noto Sans Mono" \
    "${cjk_vars[@]}" \
    -V geometry:"a4paper,left=15mm,right=12mm,top=38mm,bottom=30mm,headheight=18pt,headsep=20pt,footskip=10mm" \
    -V fontsize=11pt -V colorlinks=true --standalone
  cp "$GEN/$name.tex" "$SRC/$name.tex"
  python3 "$B/zebra.py" "$SRC/$name.tex"
  python3 "$B/breaktt.py" "$SRC/$name.tex"
  for pass in 1 2 3; do
    (cd "$SRC" && xelatex -interaction=nonstopmode -halt-on-error "$name.tex" > /dev/null 2>&1) \
      || { echo "xelatex FAIL $name pass$pass"; (cd "$SRC" && tail -n 30 "$name.log"); return 1; }
  done
  echo "ok: $name -> $SRC/$name.pdf"
}

build_one "LITEARM_SE产品手册" "LITEARM SE 产品手册" zh "a3_style_prod.tex"
build_one "LITEARM SE软件开发手册" "LITEARM SE 软件开发手册" zh
build_one "LITEARM-SE-product-manual" "LITEARM SE Product Manual" en "a3_style_prod.tex"
build_one "LITEARM-SE-software-development-manual" "LITEARM SE Software Development Manual" en
echo "ALL DONE"
