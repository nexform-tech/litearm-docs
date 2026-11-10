# Contributing

How to edit, rebuild and check the LITEARM SE documents. Read this before
changing one; to read a document rather than work on one, the
[README](README.md) is enough.

## Sources and generated files

Only the Markdown is a source. Everything beside it in the repository root is
generated, and the next build overwrites it:

| File | Generated from | By |
| --- | --- | --- |
| `LITEARM_SE产品手册.pdf` | `LITEARM_SE产品手册.md` | `build/build_a3.sh` |
| `LITEARM-SE-product-manual.pdf` | `LITEARM-SE-product-manual.md` | `build/build_a3.sh` |
| `LITEARM SE软件开发手册.pdf` | `LITEARM SE软件开发手册.md` | `build/build_a3.sh` |
| `LITEARM-SE-software-development-manual.pdf` | `LITEARM-SE-software-development-manual.md` | `build/build_a3.sh` |
| `相机支架安装使用方式.pdf` | `相机支架安装使用方式.md` | `build/build_a3.sh` |
| `camera-bracket-guide.pdf` | `camera-bracket-guide.md` | `build/build_a3.sh` |
| `manual_site/index.html` | the two Chinese manuals | `build/make_wiki.py` |

**Do not edit a PDF.** The PDFs are generated from the Markdown, and the next
build overwrites them. A change to a manual lands as two files in one commit —
the Markdown and the rebuilt PDF. The intermediate `.tex`, `.aux`, `.log` and
`.toc` files that appear alongside it are generated too and are git-ignored;
never edit them either.

**No document is source-less.** A PDF whose text is drawn into the figures is
the one case where that looks tempting, and it is still the wrong answer. The
camera bracket guide was three CAD pages with the callouts burnt in; its figures
are now those same pages with the callout text blanked out and only the red
circled numeral left, indexing the row in the table beneath the figure. Every
word moved into the Markdown, so the guide builds like the manuals, and one set
of figures serves both editions — an English reader sees the same drawings with
English tables. Blanking a callout means painting over it: sample the plate
colour on either side of the text and interpolate across, rather than smearing
the glyphs, or the retouch shows as coloured speckle against the CAD grey.

`manual_site/index.html` is committed, so it is easy to mistake for a source.
**Keep it where it is in the repository** — its figures are referenced as
`../LITEARM_SE_images/...`, so copying the file out on its own makes every
figure disappear. Do not edit it by hand either; the next run overwrites it.

## The two editions

The Chinese sources carry CJK filenames because they are the files that ship;
the English ones use ASCII names, so a tool that mangles an encoding cannot lose
them.

The Chinese editions are the ones the product goes out with, so they are the
authority. The English editions are translations of the same revision — same
structure, same tables, same code — and are corrected to match the Chinese. Do
not generate one edition from the other: prose does not translate by
substitution, and the tables and code blocks have to be read to be right.

## Building the PDFs

From the repository root:

```bash
bash build/build_a3.sh                            # all six documents
bash build/build_a3.sh LITEARM_SE产品手册          # just the Chinese product manual
bash build/build_a3.sh LITEARM-SE-product-manual  # just the English one
bash build/build_a3.sh camera-bracket-guide       # just the English camera bracket guide
```

Each document goes through pandoc to TeX, two Python post-processing passes, and
three xelatex passes, and the result lands next to its source in the repository
root. The `.tex`, `.aux`, `.log` and `.toc` files that appear alongside it are
intermediates and are git-ignored.

| Requirement | Notes |
| --- | --- |
| `pandoc` | Markdown to TeX. Verified with pandoc 2.9.2.1 |
| `xelatex` | Verified with TeX Live 2022; needs `xeCJK`, `tikz` and `booktabs` |
| `python3` | runs `zebra.py` and `breaktt.py` |
| Fonts | Lato, Noto Sans Mono, DejaVu Sans Mono, Noto Sans CJK SC, and the Noto Serif CJK SC single-region `.otf` files |

`build/a3_layout.tex` is one layout for all six documents, with placeholders
`build_a3.sh` fills per language: the CJK line-breaking and `\setCJKmainfont`
block, the table-of-contents title (目录 or Contents), and the figure caption
format (图 or Figure). The English builds load **no** CJK package, so their
fonts, line breaking and page counts are genuinely independent of the Chinese
ones; `dejavu` is the one extra dependency they carry, for the U+2500 box
drawing in the directory-tree and link diagrams that Latin Modern Mono lacks.

A document that needs a different page can add a style fragment under `build/`
and name it as the fourth argument to `build_one`; the fragment is appended to
the layout, so it overrides by later definition. `a3_style_prod.tex` gives the
product manual its looser tables and its taller orphan threshold.
`a3_style_guide.tex` gives the camera bracket guide full-width figures at 0.72
text heights and tighter space above each table: that document is three figures,
one per page, and a table that misses the page by a line costs a whole blank
page. Anything shared by two documents belongs in `a3_layout.tex`; a fragment is
for what only one document wants.

The CJK body font is pinned **by file, not by family name**, because asking the
system for `Noto Serif CJK SC` can resolve to the Japanese face in the shared
collection and silently change glyphs. `build/build_a3.sh` substitutes the
directory into `build/a3_layout.tex` from `LITEARM_CJK_FONT_DIR`, which defaults
to `~/.local/share/fonts/NotoSerifSC`. On a machine where those two `.otf` files
live elsewhere, the build stops and says so:

```bash
LITEARM_CJK_FONT_DIR=/path/to/NotoSerifSC bash build/build_a3.sh
```

**Do not put a placeholder name in a comment.** The substituted blocks are
multi-line, so one landing inside a TeX comment ends the comment and turns the
rest of the block into live TeX, which fails as a `Missing \begin{document}`
pointing at a line nobody wrote. The build checks for both this and any
placeholder left unconsumed, so the mistake is caught before pandoc runs.

## Browsing the manuals offline

```bash
python3 build/make_wiki.py
```

This writes `manual_site/index.html`: one page, a tab per manual, a collapsible
section tree on the left and a search box over the current manual. Open it in a
browser, no server needed.

The site has **two tabs, one per Chinese manual**. The English editions are not
in it yet: `build/make_wiki.py` loads two files by name. Adding them is a change
to that script, not a change to the Markdown.

## Checking the sources

```bash
python3 build/check_docs.py
```

It reads all six documents and the committed `manual_site/index.html`, resolves
every `LITEARM_SE_images/...` reference against the working tree, and fails on
the ones that do not exist. This runs in CI. A missing figure is not an error to
either the typesetter or the browser — the image is simply absent, and neither
the PDF diff nor a review catches that reliably. The English manuals need this
as much as the Chinese ones do: they point at `litearm_studio/en/`, which a
reorganisation of the figure tree can easily leave behind.

## The figures

`LITEARM_SE_images/` holds 63 images, shared by the six documents, the site, and
the next figure still to be drawn:

| Directory | Contents |
| --- | --- |
| `safety/` | the four hazard pictograms: danger, warning, high temperature, notice |
| `litearm_studio/` | screenshots of the host application |
| `litearm_studio/en/` | the English-UI counterpart of the screenshot the manuals use |
| `placeholders/` | stand-in figures, `ph_pm_*` for the product manual and `ph_sd_*` for the software one |
| `control_board/` | photographs of the control board |
| `camera_bracket/` | the three camera bracket figures: numbered callouts only, every word in the tables |
| `LITEARM_SE_images/` itself | the two cover images and three annotated arm figures |

The documents reference thirteen of them today. The two editions of a manual share
every language-independent figure, hazard pictograms included; only a screenshot
of the user interface needs one file per language. The rest are the working set
for figures that are not placed yet, which is why the directory is larger than
the manuals need.

**A hazard icon carries no word.** The pictograms are bare triangles, and each
manual sets its own label under them — `危险` in the Chinese sources, `DANGER` in
the English ones. Do not bake a word into the PNG: the two editions of a manual
would then need two files, and the Chinese product manual draws the label in
LaTeX already, so a word in the bitmap appears twice on the page.

Figure files are referenced from the Markdown by relative path, and both the
typesetter and the site builder resolve them from the repository root. Rename one
and those references break: run `python3 build/check_docs.py` to find out before
CI does.

## The STEP models

A STEP file is text, and SolidWorks writes the part name into its `FILE_NAME`
header in the system code page — GBK on a Chinese Windows. Those bytes are not
valid UTF-8, and a tool that reads the file as text and re-encodes it will
change it: the contents API on GitHub returns such a blob as UTF-8 of its
Latin-1 reading, longer than the file in the repository and with no error. It
cost one mangled copy of the column model to learn; the sync now fetches from
`raw`, which does not touch the bytes.

Still, **commit only a UTF-8 STEP file**. `LITEARM-SE-column-model.STEP` was
re-encoded once to get there — GBK in, UTF-8 out, same 282,893 entities and the
same characters in every name, four bytes longer for 总装配体 and one more per
single character elsewhere. The arm model has always been UTF-8. A re-export
from a Chinese-locale SolidWorks will come back as GBK, so check before
committing:

```bash
python3 -c "open('LITEARM-SE-step-model.STEP','rb').read().decode('utf-8')"
```

## Repository layout

```text
litearm-docs/
├── LITEARM_SE产品手册.md                        # product manual source — edit this, not the PDF
├── LITEARM_SE产品手册.pdf                       # built by build/build_a3.sh
├── LITEARM-SE-product-manual.md                # its English edition
├── LITEARM-SE-product-manual.pdf
├── LITEARM SE软件开发手册.md                     # software development manual source
├── LITEARM SE软件开发手册.pdf                    # built by build/build_a3.sh
├── LITEARM-SE-software-development-manual.md   # its English edition
├── LITEARM-SE-software-development-manual.pdf
├── 相机支架安装使用方式.md                       # camera bracket guide source
├── 相机支架安装使用方式.pdf                      # built by build/build_a3.sh
├── camera-bracket-guide.md                     # its English edition
├── camera-bracket-guide.pdf
├── LITEARM_SE_images/           # figures, shared by the documents and the site
├── manual_site/index.html       # browsable copy, built by build/make_wiki.py
└── build/
    ├── build_a3.sh              # Markdown -> PDF, three xelatex passes per document
    ├── a3_layout.tex            # page geometry, heading, TOC and caption metrics
    ├── a3_style_prod.tex        # extra table style the product manual adds
    ├── a3_style_guide.tex       # full-width figures and tight tables, camera bracket guide
    ├── zebra.py                 # grey striping on table body rows
    ├── breaktt.py               # \allowbreak inside \texttt, for long identifiers
    ├── make_wiki.py             # Markdown -> manual_site/index.html
    └── check_docs.py            # the test
```

## Repository standards

This repository follows the shared NEXFORM ROBOTICS repository standards: the
agent operating rules in [AGENTS.md](AGENTS.md), Conventional Commits, and
automated semantic-release versioning on every merge to `main`.
