# litearm-docs

[English](README.md) | [简体中文](README.zh-CN.md)

The product documentation for the LiteArm robotic manipulator series: the
LITEARM SE product manual and software development manual, each in Simplified
Chinese and in English. Every edition is published as a PDF and as Markdown.

## The manuals

| Manual | Language | Pages | PDF | Source |
| --- | --- | --- | --- | --- |
| LITEARM SE 产品手册 (product manual) | 简体中文 | 12 | [`LITEARM_SE产品手册.pdf`](<LITEARM_SE产品手册.pdf>) | [`LITEARM_SE产品手册.md`](<LITEARM_SE产品手册.md>) |
| LITEARM-SE product manual | English | 13 | [`LITEARM-SE-product-manual.pdf`](LITEARM-SE-product-manual.pdf) | [`LITEARM-SE-product-manual.md`](LITEARM-SE-product-manual.md) |
| LITEARM SE 软件开发手册 (software development manual) | 简体中文 | 28 | [`LITEARM SE软件开发手册.pdf`](<LITEARM SE软件开发手册.pdf>) | [`LITEARM SE软件开发手册.md`](<LITEARM SE软件开发手册.md>) |
| LITEARM-SE software development manual | English | 32 | [`LITEARM-SE-software-development-manual.pdf`](LITEARM-SE-software-development-manual.pdf) | [`LITEARM-SE-software-development-manual.md`](LITEARM-SE-software-development-manual.md) |

All four are revision V1.0.4, dated 2026-10-16. The revision history is the first
page of each.

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
