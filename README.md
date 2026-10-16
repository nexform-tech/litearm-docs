# litearm-docs

[English](README.md) | [简体中文](README.zh-CN.md)

The product documentation source for the LiteArm robotic manipulator series: the
two LITEARM SE manuals as PDFs, the Markdown they are built from, the figures
behind them, and the two pipelines that turn that Markdown into a PDF and into a
browsable offline copy. Read this before editing a manual. If you are installing
or programming an arm, read the manual itself.

Both manuals are written in Simplified Chinese, because that is the language the
product is delivered in. The two READMEs are the only English documents here.

## The manuals

| Manual | Pages | Source | PDF |
| --- | --- | --- | --- |
| LITEARM SE 产品手册 (product manual) | 12 | [`LITEARM_SE产品手册.md`](<LITEARM_SE产品手册.md>) | [`LITEARM_SE产品手册.pdf`](<LITEARM_SE产品手册.pdf>) |
| LITEARM SE 软件开发手册 (software development manual) | 29 | [`LITEARM SE软件开发手册.md`](<LITEARM SE软件开发手册.md>) | [`LITEARM SE软件开发手册.pdf`](<LITEARM SE软件开发手册.pdf>) |

Both are revision V1.0.4, dated 2026-10-16. The revision history is the first
page of each.

**Do not edit a PDF.** The PDFs are generated from the Markdown, and the next
build overwrites them. A change to a manual lands as two files in one commit —
the Markdown and the rebuilt PDF. The intermediate `.tex` is generated too, and
is git-ignored; never edit it.

The **product manual** is for whoever unpacks, mounts, wires or specifies the
arm: hardware composition, units, safety notices, general and control-board
specifications, joint parameters, annotated figures, and a Q&A. Mounting the arm
is a separate document, `LITEARM-SE机械臂安装教程`, which lives in
[litearm-setup](https://github.com/nexform-tech/litearm-setup) rather than here.

The **software development manual** is for whoever drives the arm from a
computer: the SDK usage guide, with the Python library as the main line, a
survey of the other language bindings and the ROS 2 environment, the LiteArm
Studio host application and safe operation on real hardware, and two appendices
— robot state and error codes, and connecting over serial.

## The figures

`LITEARM_SE_images/` holds 59 images, shared by both manuals, the site, and the
next figure still to be drawn:

| Directory | Contents |
| --- | --- |
| `safety/` | the four hazard icons: danger, warning, high temperature, notice |
| `litearm_studio/` | screenshots of the host application |
| `placeholders/` | stand-in figures, `ph_pm_*` for the product manual and `ph_sd_*` for the software one |
| `control_board/` | photographs of the control board |
| `LITEARM_SE_images/` itself | the two cover images and three annotated arm figures |

The two manuals reference nine of them today. The rest are the working set for
figures that are not placed yet, which is why the directory is larger than the
manuals need.

Figure files are referenced from the Markdown by relative path, and both the
typesetter and the site builder resolve them from the repository root. Rename one
and those references break: run `python3 build/check_docs.py` to find out before
CI does.

## Building the PDFs

From the repository root:

```bash
bash build/build_a3.sh                       # both manuals
bash build/build_a3.sh LITEARM_SE产品手册     # just the product manual
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
| Fonts | Lato, Noto Sans Mono, Noto Sans CJK SC, and the Noto Serif CJK SC single-region `.otf` files |

The CJK body font is pinned **by file, not by family name**, because asking the
system for `Noto Serif CJK SC` can resolve to the Japanese face in the shared
collection and silently change glyphs. `build/build_a3.sh` substitutes the
directory into `build/a3_layout.tex` from `LITEARM_CJK_FONT_DIR`, which defaults
to `~/.local/share/fonts/NotoSerifSC`. On a machine where those two `.otf` files
live elsewhere, the build stops and says so:

```bash
LITEARM_CJK_FONT_DIR=/path/to/NotoSerifSC bash build/build_a3.sh
```

## Browsing the manuals offline

```bash
python3 build/make_wiki.py
```

This writes `manual_site/index.html`, which is committed: one page, a tab per
manual, a collapsible section tree on the left and a search box over the current
manual. Open it in a browser, no server needed.

Its figures are referenced as `../LITEARM_SE_images/...`, so the page reads the
same directory the PDFs are built from and the repository does not carry a second
7 MB copy of it. **Keep the file where it is in the repository** — copy
`index.html` out on its own and every figure disappears. Do not edit it by hand
either; the next run overwrites it.

## Checking the sources

```bash
python3 build/check_docs.py
```

It reads both manuals and the committed `manual_site/index.html`, resolves every
`LITEARM_SE_images/...` reference against the working tree, and fails on the ones
that do not exist. This runs in CI. A missing figure is not an error to either
the typesetter or the browser — the image is simply absent, and neither the PDF
diff nor a review catches that reliably.

## Repository layout

```text
litearm-docs/
├── LITEARM_SE产品手册.md         # product manual source — edit this, not the PDF
├── LITEARM_SE产品手册.pdf        # built by build/build_a3.sh
├── LITEARM SE软件开发手册.md      # software development manual source
├── LITEARM SE软件开发手册.pdf     # built by build/build_a3.sh
├── LITEARM_SE_images/           # figures, shared by the manuals and the site
├── manual_site/index.html       # browsable copy, built by build/make_wiki.py
└── build/
    ├── build_a3.sh              # Markdown -> PDF, three xelatex passes per manual
    ├── a3_layout.tex            # page geometry, heading and TOC metrics, captions
    ├── a3_style_prod.tex        # extra table style the product manual adds
    ├── zebra.py                 # grey striping on table body rows
    ├── breaktt.py               # \allowbreak inside \texttt, for long identifiers
    ├── make_wiki.py             # Markdown -> manual_site/index.html
    └── check_docs.py            # the test
```

## Related repositories

Documentation and setup reads:

| Repository | Role |
| --- | --- |
| [litearm-setup](https://github.com/nexform-tech/litearm-setup) | Installation guide for the arm, with the document source that builds it |
| [litearm-description](https://github.com/nexform-tech/litearm-description) | URDF description of every LiteArm model |

SDKs and host software:

| Repository | Role |
| --- | --- |
| [litearm-python](https://github.com/nexform-tech/litearm-python) | Python SDK |
| [litearm-cpp](https://github.com/nexform-tech/litearm-cpp) | C++ SDK |
| [litearm-js](https://github.com/nexform-tech/litearm-js) | JavaScript and TypeScript SDK |
| [litearm-studio](https://github.com/nexform-tech/litearm-studio) | Cross-platform host application and desktop studio |

ROS:

| Repository | Role |
| --- | --- |
| [litearm-ros1](https://github.com/nexform-tech/litearm-ros1) | ROS 1 driver |
| [litearm-ros2](https://github.com/nexform-tech/litearm-ros2) | ROS 2 driver |
| [litearm-ros2-control](https://github.com/nexform-tech/litearm-ros2-control) | ros2_control hardware interface |
| [litearm-moveit1](https://github.com/nexform-tech/litearm-moveit1) | MoveIt 1 configurations and catkin launch pipelines |
| [litearm-moveit2](https://github.com/nexform-tech/litearm-moveit2) | MoveIt 2 packages and MoveGroup node configurations |

Simulation:

| Repository | Role |
| --- | --- |
| [litearm-mujoco](https://github.com/nexform-tech/litearm-mujoco) | MuJoCo dynamics simulation environment |
| [litearm-pybullet](https://github.com/nexform-tech/litearm-pybullet) | PyBullet physics simulation environment |
| [litearm-isaacsim](https://github.com/nexform-tech/litearm-isaacsim) | NVIDIA Isaac Sim environment |

Teleoperation and learning:

| Repository | Role |
| --- | --- |
| [litearm-teleop-vr](https://github.com/nexform-tech/litearm-teleop-vr) | VR teleoperation stack |
| [litearm-teleop-isomorphic](https://github.com/nexform-tech/litearm-teleop-isomorphic) | Isomorphic leader-follower teleoperation stack |
| [litearm-lerobot](https://github.com/nexform-tech/litearm-lerobot) | LeRobot driver |
| [litearm-vla](https://github.com/nexform-tech/litearm-vla) | VLA embodiment and data adaptation |

Agent integrations:

| Repository | Role |
| --- | --- |
| [litearm-dsh](https://github.com/nexform-tech/litearm-dsh) | DeepSeek Harness integration |
| [litearm-hermes](https://github.com/nexform-tech/litearm-hermes) | Hermes agent platform integration |
| [litearm-openclaw](https://github.com/nexform-tech/litearm-openclaw) | OpenClaw driver and tool binding |

The same organisation publishes the W1 wheeled mobile robot (`w1-*`) and the
LiteGrip gripper (`litegrip-*`). See the
[nexform-tech organisation](https://github.com/nexform-tech) for the full list.

## Repository standards

This repository follows the shared NEXFORM ROBOTICS repository standards: the
agent operating rules in [AGENTS.md](AGENTS.md), Conventional Commits, and
automated semantic-release versioning on every merge to `main`.

## License

Copyright © 2026 NEXFORM ROBOTICS. Licensed under the
[Apache License 2.0](LICENSE).
