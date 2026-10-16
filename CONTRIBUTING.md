# Contributing

How to edit, rebuild and check the LITEARM SE manuals. Read this before changing
a manual; to read a manual rather than work on one, the [README](README.md) is
enough.

## Sources and generated files

Only the Markdown is a source. Everything beside it in the repository root is
generated, and the next build overwrites it:

| File | Generated from | By |
| --- | --- | --- |
| `LITEARM_SE产品手册.pdf` | `LITEARM_SE产品手册.md` | `build/build_a3.sh` |
| `LITEARM-SE-product-manual.pdf` | `LITEARM-SE-product-manual.md` | `build/build_a3.sh` |
| `LITEARM SE软件开发手册.pdf` | `LITEARM SE软件开发手册.md` | `build/build_a3.sh` |
| `LITEARM-SE-software-development-manual.pdf` | `LITEARM-SE-software-development-manual.md` | `build/build_a3.sh` |
| `manual_site/index.html` | the two Chinese manuals | `build/make_wiki.py` |
| `LITEARM_SE_images/safety/en/*.png` | the four Chinese hazard icons | `build/make_safety_icons.py` |

**Do not edit a PDF.** The PDFs are generated from the Markdown, and the next
build overwrites them. A change to a manual lands as two files in one commit —
the Markdown and the rebuilt PDF. The intermediate `.tex`, `.aux`, `.log` and
`.toc` files that appear alongside it are generated too and are git-ignored;
never edit them either.

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
bash build/build_a3.sh                            # all four manuals
bash build/build_a3.sh LITEARM_SE产品手册          # just the Chinese product manual
bash build/build_a3.sh LITEARM-SE-product-manual  # just the English one
```

Each manual goes through pandoc to TeX, two Python post-processing passes, and
three xelatex passes, and the result lands next to its source in the repository
root. The `.tex`, `.aux`, `.log` and `.toc` files that appear alongside it are
intermediates and are git-ignored.

| Requirement | Notes |
| --- | --- |
| `pandoc` | Markdown to TeX. Verified with pandoc 2.9.2.1 |
| `xelatex` | Verified with TeX Live 2022; needs `xeCJK`, `tikz` and `booktabs` |
| `python3` | runs `zebra.py` and `breaktt.py` |
| Fonts | Lato, Noto Sans Mono, DejaVu Sans Mono, Noto Sans CJK SC, and the Noto Serif CJK SC single-region `.otf` files |

`build/a3_layout.tex` is one layout for all four manuals, with placeholders
`build_a3.sh` fills per language: the CJK line-breaking and `\setCJKmainfont`
block, the table-of-contents title (目录 or Contents), and the figure caption
format (图 or Figure). The English builds load **no** CJK package, so their
fonts, line breaking and page counts are genuinely independent of the Chinese
ones; `dejavu` is the one extra dependency they carry, for the U+2500 box
drawing in the directory-tree and link diagrams that Latin Modern Mono lacks.

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

It reads all four manuals and the committed `manual_site/index.html`, resolves
every `LITEARM_SE_images/...` reference against the working tree, and fails on
the ones that do not exist. This runs in CI. A missing figure is not an error to
either the typesetter or the browser — the image is simply absent, and neither
the PDF diff nor a review catches that reliably. The English manuals need this
as much as the Chinese ones do: they point at `safety/en/` and
`litearm_studio/en/`, which a reorganisation of the figure tree can easily leave
behind.

## The figures

`LITEARM_SE_images/` holds 64 images, shared by the four manuals, the site, and
the next figure still to be drawn:

| Directory | Contents |
| --- | --- |
| `safety/` | the four hazard icons: danger, warning, high temperature, notice |
| `safety/en/` | the same four pictograms relabelled in English, used by the English manuals |
| `litearm_studio/` | screenshots of the host application |
| `litearm_studio/en/` | the English-UI counterpart of the screenshot the manuals use |
| `placeholders/` | stand-in figures, `ph_pm_*` for the product manual and `ph_sd_*` for the software one |
| `control_board/` | photographs of the control board |
| `LITEARM_SE_images/` itself | the two cover images and three annotated arm figures |

The four manuals reference fourteen of them today; the two editions of a manual
share the language-independent figures and each has its own screenshots and
hazard icons. The rest are the working set for figures that are not placed yet,
which is why the directory is larger than the manuals need.

`safety/en/` is generated by `build/make_safety_icons.py`, which crops the
Chinese word off each pictogram and sets the English one below it. The Chinese
originals are never touched. Rerunning the script overwrites the English files,
so **do not edit them by hand** — edit the script.

Figure files are referenced from the Markdown by relative path, and both the
typesetter and the site builder resolve them from the repository root. Rename one
and those references break: run `python3 build/check_docs.py` to find out before
CI does.

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
├── LITEARM_SE_images/           # figures, shared by the manuals and the site
├── manual_site/index.html       # browsable copy, built by build/make_wiki.py
└── build/
    ├── build_a3.sh              # Markdown -> PDF, three xelatex passes per manual
    ├── a3_layout.tex            # page geometry, heading, TOC and caption metrics
    ├── a3_style_prod.tex        # extra table style the product manual adds
    ├── zebra.py                 # grey striping on table body rows
    ├── breaktt.py               # \allowbreak inside \texttt, for long identifiers
    ├── make_safety_icons.py     # hazard icons relabelled in English
    ├── make_wiki.py             # Markdown -> manual_site/index.html
    └── check_docs.py            # the test
```

## Repository standards

This repository follows the shared NEXFORM ROBOTICS repository standards: the
agent operating rules in [AGENTS.md](AGENTS.md), Conventional Commits, and
automated semantic-release versioning on every merge to `main`.
