# litearm-docs

[English](README.md) | [简体中文](README.zh-CN.md)

The product documentation for the LiteArm robotic manipulator series: the
LITEARM SE product manual and software development manual, and the camera
bracket guide, each in Simplified Chinese and in English. Every edition is
published as a PDF and as Markdown.

## The documents

| Document | Language | Pages | PDF | Source |
| --- | --- | --- | --- | --- |
| LITEARM SE 产品手册 (product manual) | 简体中文 | 12 | [`LITEARM_SE产品手册.pdf`](<LITEARM_SE产品手册.pdf>) | [`LITEARM_SE产品手册.md`](<LITEARM_SE产品手册.md>) |
| LITEARM-SE product manual | English | 13 | [`LITEARM-SE-product-manual.pdf`](LITEARM-SE-product-manual.pdf) | [`LITEARM-SE-product-manual.md`](LITEARM-SE-product-manual.md) |
| LITEARM SE 软件开发手册 (software development manual) | 简体中文 | 28 | [`LITEARM SE软件开发手册.pdf`](<LITEARM SE软件开发手册.pdf>) | [`LITEARM SE软件开发手册.md`](<LITEARM SE软件开发手册.md>) |
| LITEARM-SE software development manual | English | 32 | [`LITEARM-SE-software-development-manual.pdf`](LITEARM-SE-software-development-manual.pdf) | [`LITEARM-SE-software-development-manual.md`](LITEARM-SE-software-development-manual.md) |
| 相机支架安装使用方式 (camera bracket guide) | 简体中文 | 3 | [`相机支架安装使用方式.pdf`](<相机支架安装使用方式.pdf>) | [`相机支架安装使用方式.md`](<相机支架安装使用方式.md>) |
| Camera bracket mounting and use | English | 3 | [`camera-bracket-guide.pdf`](camera-bracket-guide.pdf) | [`camera-bracket-guide.md`](camera-bracket-guide.md) |

All four manuals are revision V1.0.4, dated 2026-10-16, and their first page is
the revision history. The camera bracket guide is V1.0.0, dated 2026-11-06.

The **product manual** is for whoever unpacks, mounts, wires or specifies the
arm: hardware composition, units, safety notices, general and control-board
specifications, joint parameters, annotated figures, and a Q&A. Mounting the arm
is a separate document, `LITEARM-SE-installation-guide` and its Chinese edition
`LITEARM-SE机械臂安装教程`, which live in
[litearm-setup](https://github.com/nexform-tech/litearm-setup) rather than here.

The **software development manual** is for whoever drives the arm from a
computer: the SDK usage guide, with the Python library as the main line, a
survey of the other language bindings and the ROS 2 environment, the LiteArm
Studio host application and safe operation on real hardware, and two appendices
— robot state and error codes, and connecting over serial.

The **camera bracket guide** is the short one: how the bracket holds the camera
on a LiteGrip gripper or holder and how it fixes to the column, in three
annotated figures. The callouts in a figure are numbered, and the table under it
carries the words, so the same figures serve both editions.

## Models

| File | Contents |
| --- | --- |
| [`LITEARM-SE-step-model.STEP`](LITEARM-SE-step-model.STEP) | STEP model of the LITEARM SE arm |
| [`LITEARM-SE-column-model.STEP`](LITEARM-SE-column-model.STEP) | STEP model of the vertical column the arm mounts on |
| [`LITEARM-SE末端连接件.STEP`](<LITEARM-SE末端连接件.STEP>) | STEP model of the end connector |

## The documentation centre

Every PDF and STEP model here is also published to the NEXFORM documentation
centre in Feishu. Nobody uploads it by hand: merging a file to `main` is the
whole procedure, and the site catches up within minutes.

1. A push to `main` that touches `*.pdf`, `*.STEP` or `*.step` starts
   `.github/workflows/notify-docs.yml`. It mints a short-lived token for the
   `nexform-docs-dispatch` GitHub App and sends a `docs-updated` dispatch to
   [nexform-guide](https://github.com/nexform-tech/nexform-guide).
2. `nexform-guide` runs `scripts/sync_files.py`, which downloads each file its
   `files.yaml` lists from the repository that owns it, and commits only the
   copies whose bytes changed.
3. Its `Publish` workflow compares the SHA-256 of every Feishu file block with
   the local copy, re-uploads the ones that differ, then reads the document back
   and verifies it.

A nightly run at 03:00 UTC repeats step 2, so a missed dispatch costs at most a
day. No Feishu credentials are needed on your side: the jobs that talk to Feishu
run in CI.

The file name is the join key between the two repositories. Replacing a manual or
a model in place needs nothing else; adding, renaming or removing one needs a
pull request in `nexform-guide` that changes `files.yaml` and the page link in
the same round, or the site keeps serving the old file.

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

## License

Copyright © 2026 NEXFORM ROBOTICS. Licensed under the
[Apache License 2.0](LICENSE).
