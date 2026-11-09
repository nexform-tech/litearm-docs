# litearm-docs

[English](README.md) | [简体中文](README.zh-CN.md)

LiteArm 机械臂系列的产品文档：LITEARM SE 的产品手册、软件开发手册和相机支架
安装使用方式，各有简体中文和英文两版，每版都提供 PDF 和 Markdown 两种形式。

## 文档

| 文档 | 语言 | 页数 | PDF | 源文件 |
| --- | --- | --- | --- | --- |
| LITEARM SE 产品手册 | 简体中文 | 12 | [`LITEARM_SE产品手册.pdf`](<LITEARM_SE产品手册.pdf>) | [`LITEARM_SE产品手册.md`](<LITEARM_SE产品手册.md>) |
| LITEARM-SE product manual | English | 13 | [`LITEARM-SE-product-manual.pdf`](LITEARM-SE-product-manual.pdf) | [`LITEARM-SE-product-manual.md`](LITEARM-SE-product-manual.md) |
| LITEARM SE 软件开发手册 | 简体中文 | 28 | [`LITEARM SE软件开发手册.pdf`](<LITEARM SE软件开发手册.pdf>) | [`LITEARM SE软件开发手册.md`](<LITEARM SE软件开发手册.md>) |
| LITEARM-SE software development manual | English | 32 | [`LITEARM-SE-software-development-manual.pdf`](LITEARM-SE-software-development-manual.pdf) | [`LITEARM-SE-software-development-manual.md`](LITEARM-SE-software-development-manual.md) |
| 相机支架安装使用方式 | 简体中文 | 3 | [`相机支架安装使用方式.pdf`](<相机支架安装使用方式.pdf>) | [`相机支架安装使用方式.md`](<相机支架安装使用方式.md>) |
| Camera bracket mounting and use | English | 3 | [`camera-bracket-guide.pdf`](camera-bracket-guide.pdf) | [`camera-bracket-guide.md`](camera-bracket-guide.md) |

四本手册都是 V1.0.4 版，日期 2026-10-16，首页即修订记录。相机支架安装使用方式
是 V1.0.0 版，日期 2026-11-06。

**产品手册**给开箱、安装、接线和选型的人看：硬件组成、单位说明、安全须知、
通用规格与控制板规格、关节参数、标注图，以及常见问题。机械臂的安装步骤是
另一份文档 `LITEARM-SE机械臂安装教程`（英文版
`LITEARM-SE-installation-guide`），在
[litearm-setup](https://github.com/nexform-tech/litearm-setup) 仓库里，不在
这里。

**软件开发手册**给用电脑驱动机械臂的人看：SDK 使用指南，以 Python 库为主线，
另有其他语言绑定与 ROS 2 环境概述、上位机软件 LiteArm Studio 与实机安全操作
建议，以及两个附录——机器人状态与报错、机械臂连接。

**相机支架安装使用方式**是最短的一份：相机支架怎样把相机固定在 LiteGrip 夹爪或
夹持器上，以及怎样固定在立柱上，三幅标注图说清楚。图里的标注只留编号，文字在
图下的表格里，所以中英两版共用同一组图。

## 文档中心

这里的每一份 PDF 和 STEP 模型都会同步到飞书上的 NEXFORM 文档中心。不需要人工
上传：把文件合并进 `main` 就是全部流程，几分钟内站点就会更新。

1. 推送到 `main` 且改动 `*.pdf`、`*.STEP` 或 `*.step` 时，触发
   `.github/workflows/notify-docs.yml`；它用 `nexform-docs-dispatch` 这个
   GitHub App 换取短期令牌，向
   [nexform-guide](https://github.com/nexform-tech/nexform-guide) 发送
   `docs-updated` 事件。
2. `nexform-guide` 运行 `scripts/sync_files.py`，按它 `files.yaml` 的清单从
   拥有该文件的仓库下载，只提交字节有变化的那些。
3. 它的 `Publish` 流程逐个比对飞书文件块与本地副本的 SHA-256，只重传不同的
   那些，然后回读文档校验。

每天 03:00 UTC 还会跑一遍第 2 步，所以即使某次事件丢了，最多晚一天。你这边
不需要任何飞书凭据：跟飞书打交道的任务都在 CI 里跑。

文件名是这两个仓库之间的关联键。原地替换一份手册或模型不需要别的操作；新增、
改名或删除则需要同时在 `nexform-guide` 开 PR，改 `files.yaml` 和页面链接两处，
否则站点会继续指向旧文件。

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

## 许可证

Copyright © 2026 NEXFORM ROBOTICS，采用
[Apache License 2.0](LICENSE) 许可。
