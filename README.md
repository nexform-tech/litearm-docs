# litearm-docs

Product documentation source, built and published as the public documentation
site for the **LiteArm robotic manipulator series**.

> **Status:** the LITEARM SE manuals are committed. The documentation toolchain
> and the published site have not landed yet.

## Scope

| | |
| --- | --- |
| Product | LiteArm robotic manipulator series |
| Repository role | Product documentation source, built and published as the public documentation site |
| Status | Initializing — LITEARM SE manuals committed, toolchain not yet chosen |

## Manuals

Both manuals are revision V1.0.4, dated 2026-10-16, and are written in
Simplified Chinese.

| Manual | Document | Pages |
| --- | --- | --- |
| Product manual | [LITEARM_SE产品手册.pdf](<LITEARM_SE产品手册.pdf>) | 12 |
| Software development manual | [LITEARM SE软件开发手册.pdf](<LITEARM SE软件开发手册.pdf>) | 29 |

The product manual covers hardware composition, safety notices, electrical
interfaces and frequently asked questions. Robot installation lives in a
separate document, 《LITEARM-SE 机械臂安装教程》, that is not in this repository.

The software development manual covers the SDK usage guide and the host
tooling.

Do not read the PDFs as the documentation source: they are rendered output and
no build pipeline in this repository regenerates them.

## Related repositories

| Repository | Role |
| --- | --- |
| [litearm-python](https://github.com/nexform-tech/litearm-python) | Python SDK |
| [litearm-cpp](https://github.com/nexform-tech/litearm-cpp) | C++ SDK |
| [litearm-ros2](https://github.com/nexform-tech/litearm-ros2) | ROS 2 driver |
| [litearm-ros1](https://github.com/nexform-tech/litearm-ros1) | ROS 1 driver |

## Repository standards

This repository follows the shared NEXFORM ROBOTICS repository standards: the
agent operating rules in [AGENTS.md](AGENTS.md), Conventional Commits, and
automated semantic-release versioning on every merge to `main`.

## License

Copyright © 2026 NEXFORM ROBOTICS. Licensed under the
[Apache License 2.0](LICENSE).
