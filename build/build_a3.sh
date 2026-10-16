#!/usr/bin/env bash
# Rebuild both LITEARM SE manual PDFs from their Markdown sources.
#
# Pipeline, per manual: Markdown -> pandoc (TeX) -> zebra.py / breaktt.py
# post-processing -> three xelatex passes. The PDF lands in the repository root,
# next to its source; the intermediate .tex/.aux/.log/.toc files land there too
# and are git-ignored.
#
# Usage:
#   bash build/build_a3.sh                       # both manuals
#   bash build/build_a3.sh LITEARM_SE产品手册     # one of them
#
# Requirements: pandoc, xelatex (TeX Live with xeCJK and tikz), python3, and the
# CJK fonts described in the repository README.
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

build_one () {
  name="$1"; docshort="$2"; style="${3:-}"
  if [ -n "$WANT" ] && [ "$WANT" != "$name" ]; then
    return 0
  fi
  echo "===== build $name ====="

  # Drop the emoji the PDF cannot typeset; the Markdown keeps them for the site.
  python3 - "$SRC/$name.md" "$GEN/$name.md" <<'PY'
import sys
t=open(sys.argv[1],encoding="utf-8").read()
for a,b in (("✅","✓"),("⚠️","⚠"),("📐","图"),("️","")): t=t.replace(a,b)
open(sys.argv[2],"w",encoding="utf-8").write(t)
PY

  sed -e "s/@DOCSHORT@/${docshort}/g" -e "s|@CJKFONTDIR@|${CJK_FONT_DIR}/|g" \
    "$B/a3_layout.tex" > "$GEN/layout_$name.tex"
  # Append the per-document style fragment, e.g. the product manual's table alignment.
  if [ -n "$style" ] && [ -f "$B/$style" ]; then cat "$B/$style" >> "$GEN/layout_$name.tex"; fi

  pandoc "$GEN/$name.md" -o "$GEN/$name.tex" \
    --pdf-engine=xelatex --include-in-header="$GEN/layout_$name.tex" --columns=50 \
    -N \
    -V mainfont="Lato" -V sansfont="Lato" -V monofont="Noto Sans Mono" \
    -V CJKmainfont="Noto Serif CJK SC" -V CJKsansfont="Noto Sans CJK SC" \
    -V CJKmonofont="Noto Sans Mono CJK SC" \
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

build_one "LITEARM_SE产品手册" "LITEARM SE 产品手册" "a3_style_prod.tex"
build_one "LITEARM SE软件开发手册" "LITEARM SE 软件开发手册"
echo "ALL DONE"
