# litearm-docs

[English](README.md) | [简体中文](README.zh-CN.md)

LiteArm 机械臂系列的产品文档源：LITEARM SE 两本手册的 PDF、生成它们的
Markdown、正文里的插图，以及把 Markdown 变成 PDF 和变成可离线浏览的一份
网页的两条流水线。改手册之前先读这份说明；要安装或编程机械臂，请直接读
手册本身。

两本手册正文都是简体中文，因为产品就是以中文交付的。本仓库的英文文档只有
两份 README。

## 两本手册

| 手册 | 页数 | 源文件 | PDF |
| --- | --- | --- | --- |
| LITEARM SE 产品手册 | 12 | [`LITEARM_SE产品手册.md`](<LITEARM_SE产品手册.md>) | [`LITEARM_SE产品手册.pdf`](<LITEARM_SE产品手册.pdf>) |
| LITEARM SE 软件开发手册 | 29 | [`LITEARM SE软件开发手册.md`](<LITEARM SE软件开发手册.md>) | [`LITEARM SE软件开发手册.pdf`](<LITEARM SE软件开发手册.pdf>) |

两本都是 V1.0.4 版，日期 2026-10-16，首页即修订记录。

**不要改 PDF。** PDF 由 Markdown 生成，下次构建就会覆盖。改一次手册在一个
提交里落两个文件——Markdown 和重新生成的 PDF。中间产物 `.tex` 同样是生成的，
已在 `.gitignore` 里，也不要改它。

**产品手册**给开箱、安装、接线和选型的人看：硬件组成、单位说明、安全须知、
通用规格与控制板规格、关节参数、标注图，以及常见问题。机械臂的安装步骤是
另一份文档《LITEARM-SE 机械臂安装教程》，在
[litearm-setup](https://github.com/nexform-tech/litearm-setup) 仓库里，不在
这里。

**软件开发手册**给用电脑驱动机械臂的人看：SDK 使用指南，以 Python 库为主线，
另有其他语言与软件生态概述、ROS 2 环境的使用、上位机软件 LiteArm Studio 与
实机安全操作建议，以及两个附录——机器人状态与报错、机械臂连接。

## 插图

`LITEARM_SE_images/` 共 59 张图，两本手册、离线站点和还没画完的插图共用：

| 目录 | 内容 |
| --- | --- |
| `safety/` | 四张安全图标：危险、警告、高温、注意 |
| `litearm_studio/` | 上位机界面截图 |
| `placeholders/` | 占位图，`ph_pm_*` 属产品手册，`ph_sd_*` 属开发手册 |
| `control_board/` | 控制板实拍 |
| `LITEARM_SE_images/` 本级 | 两张封面图和三张机械臂标注图 |

两本手册目前引用了其中 9 张，其余是尚未排进正文的图的工作集，所以这个目录比
手册实际用到的要大。

插图在 Markdown 里以相对路径引用，排版流程和站点生成脚本都从仓库根目录解析。
改图名就会让引用失效，提交前先跑 `python3 build/check_docs.py`，别等 CI 报红。

## 生成 PDF

在仓库根目录执行：

```bash
bash build/build_a3.sh                       # 两本都构建
bash build/build_a3.sh LITEARM_SE产品手册     # 只构建产品手册
```

每本手册都经过 pandoc 转 TeX、两遍 Python 后处理、三遍 xelatex，产物落在仓库
根目录、与源文件同级。随之出现的 `.tex`、`.aux`、`.log`、`.toc` 都是中间产物，
已在 `.gitignore` 里。

| 依赖 | 说明 |
| --- | --- |
| `pandoc` | Markdown 转 TeX，实测版本 pandoc 2.9.2.1 |
| `xelatex` | 实测 TeX Live 2022，需要 `xeCJK`、`tikz`、`booktabs` |
| `python3` | 运行 `zebra.py` 和 `breaktt.py` |
| 字体 | Lato、Noto Sans Mono、Noto Sans CJK SC，以及 Noto Serif CJK SC 的单地区 `.otf` 文件 |

中文字体是**按文件而不是按字体名**指定的：向系统索取 `Noto Serif CJK SC` 时，
共享字体集可能落到日文那一面，字形会悄悄变掉。`build/build_a3.sh` 把目录代入
`build/a3_layout.tex`，目录取自环境变量 `LITEARM_CJK_FONT_DIR`，默认
`~/.local/share/fonts/NotoSerifSC`。这两个 `.otf` 放在别处时，构建会直接停下
并说明原因：

```bash
LITEARM_CJK_FONT_DIR=/path/to/NotoSerifSC bash build/build_a3.sh
```

## 离线浏览手册

```bash
python3 build/make_wiki.py
```

生成 `manual_site/index.html`，它是入库的：单页、每本手册一个标签页、左侧可
折叠的章节树、顶部对当前手册的搜索框。用浏览器直接打开即可，不需要起服务。

站点里的图以 `../LITEARM_SE_images/...` 引用，和 PDF 读的是同一份目录，仓库里
因此不用再存一份 7 MB 的副本。**index.html 要留在仓库里的原位**——单独拷出去，
所有插图都会失效。也不要手改它，下次生成会覆盖。

## 检查源文件

```bash
python3 build/check_docs.py
```

它读两本手册和已入库的 `manual_site/index.html`，把每条 `LITEARM_SE_images/...`
引用解析到工作区里的真实路径，解析不到就报错。这个检查在 CI 里跑。缺图对排版
流程和浏览器都不是错误——图只是不见了，PDF 的 diff 和人工评审都很难发现。

## 仓库结构

```text
litearm-docs/
├── LITEARM_SE产品手册.md         # 产品手册源文件——改这个，不要改 PDF
├── LITEARM_SE产品手册.pdf        # 由 build/build_a3.sh 生成
├── LITEARM SE软件开发手册.md      # 软件开发手册源文件
├── LITEARM SE软件开发手册.pdf     # 由 build/build_a3.sh 生成
├── LITEARM_SE_images/           # 插图，手册和站点共用
├── manual_site/index.html       # 可浏览的一份，由 build/make_wiki.py 生成
└── build/
    ├── build_a3.sh              # Markdown -> PDF，每本手册三遍 xelatex
    ├── a3_layout.tex            # 页面尺寸、标题与目录度量、图注格式
    ├── a3_style_prod.tex        # 产品手册额外追加的表格样式
    ├── zebra.py                 # 表格数据行的灰色斑马纹
    ├── breaktt.py               # 给 \texttt 里的长标识符插 \allowbreak
    ├── make_wiki.py             # Markdown -> manual_site/index.html
    └── check_docs.py            # 测试
```

## 相关仓库

文档与开箱安装：

| 仓库 | 作用 |
| --- | --- |
| [litearm-setup](https://github.com/nexform-tech/litearm-setup) | 机械臂安装教程，含生成它的文档源 |
| [litearm-description](https://github.com/nexform-tech/litearm-description) | 各 LiteArm 型号的 URDF 描述 |

SDK 与上位机：

| 仓库 | 作用 |
| --- | --- |
| [litearm-python](https://github.com/nexform-tech/litearm-python) | Python SDK |
| [litearm-cpp](https://github.com/nexform-tech/litearm-cpp) | C++ SDK |
| [litearm-js](https://github.com/nexform-tech/litearm-js) | JavaScript / TypeScript SDK |
| [litearm-studio](https://github.com/nexform-tech/litearm-studio) | 跨平台上位机与桌面工作台 |

ROS：

| 仓库 | 作用 |
| --- | --- |
| [litearm-ros1](https://github.com/nexform-tech/litearm-ros1) | ROS 1 驱动 |
| [litearm-ros2](https://github.com/nexform-tech/litearm-ros2) | ROS 2 驱动 |
| [litearm-ros2-control](https://github.com/nexform-tech/litearm-ros2-control) | ros2_control 硬件接口 |
| [litearm-moveit1](https://github.com/nexform-tech/litearm-moveit1) | MoveIt 1 配置与 catkin launch |
| [litearm-moveit2](https://github.com/nexform-tech/litearm-moveit2) | MoveIt 2 功能包与 MoveGroup 节点配置 |

仿真：

| 仓库 | 作用 |
| --- | --- |
| [litearm-mujoco](https://github.com/nexform-tech/litearm-mujoco) | MuJoCo 动力学仿真环境 |
| [litearm-pybullet](https://github.com/nexform-tech/litearm-pybullet) | PyBullet 物理仿真环境 |
| [litearm-isaacsim](https://github.com/nexform-tech/litearm-isaacsim) | NVIDIA Isaac Sim 环境 |

遥操作与学习：

| 仓库 | 作用 |
| --- | --- |
| [litearm-teleop-vr](https://github.com/nexform-tech/litearm-teleop-vr) | VR 遥操作 |
| [litearm-teleop-isomorphic](https://github.com/nexform-tech/litearm-teleop-isomorphic) | 同构主从遥操作 |
| [litearm-lerobot](https://github.com/nexform-tech/litearm-lerobot) | LeRobot 驱动 |
| [litearm-vla](https://github.com/nexform-tech/litearm-vla) | VLA 具身与数据适配 |

智能体集成：

| 仓库 | 作用 |
| --- | --- |
| [litearm-dsh](https://github.com/nexform-tech/litearm-dsh) | DeepSeek Harness 集成 |
| [litearm-hermes](https://github.com/nexform-tech/litearm-hermes) | Hermes 智能体平台集成 |
| [litearm-openclaw](https://github.com/nexform-tech/litearm-openclaw) | OpenClaw 驱动与工具绑定 |

同一组织下还有 W1 轮式移动机器人（`w1-*`）和 LiteGrip 夹爪（`litegrip-*`）
两个系列，完整列表见
[nexform-tech 组织](https://github.com/nexform-tech)。

## 仓库规范

本仓库遵循 NEXFORM ROBOTICS 的共享仓库规范：智能体操作规则见
[AGENTS.md](AGENTS.md)，提交信息遵循 Conventional Commits，合并进 `main` 后由
semantic-release 自动发版。

## 许可证

Copyright © 2026 NEXFORM ROBOTICS，采用
[Apache License 2.0](LICENSE) 许可。
