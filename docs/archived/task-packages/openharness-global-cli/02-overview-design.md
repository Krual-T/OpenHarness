# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖以下表面：

- OpenHarness 自身的 Python 打包元数据。
- `using-openharness` 当前 CLI 实现及其兼容入口。
- 安装与升级文档。
- 与 CLI 入口有关的自动化测试。

本轮不覆盖：

- 其他技能的脚本统一收口。
- 原生二进制构建链。
- 面向 PyPI 的正式发布流程。

## Proposed Structure
推荐采用“双层安装、单一命令入口”的结构：

- 技能层继续通过 `.agents/skills/openharness` 软链接让 Codex 发现技能。
- 工具层把当前 `using-openharness` CLI 抽成正式 Python 包 `openharness_cli`，并在仓库根 `pyproject.toml` 中暴露 `openharness` console script。
- 兼容层保留 `skills/using-openharness/scripts/openharness.py`，让历史路径继续工作，同时把实现依赖切换到正式包。

主路径是：

1. 用户克隆 OpenHarness 仓库。
2. 用户通过 `uv tool install --editable <repo>` 安装工具命令。
3. 用户通过软链接安装技能目录。
4. 智能体和维护者统一使用 `openharness <cmd>`；若命令不可用，再退回旧脚本路径。

## Key Flows
命令安装流：

- `uv tool install --editable ~/.agents/skill-hub/openharness`
- `uv` 读取 OpenHarness 仓库自身的 `pyproject.toml`
- 安装 `project.scripts` 暴露出的 `openharness` 命令
- 用户 PATH 中出现 `openharness`

兼容执行流：

- 旧入口 `skills/using-openharness/scripts/openharness.py`
- 导入正式包 `openharness_cli`
- 继续复用同一套 parser 和 command handler

文档迁移流：

- 新用户按照更新后的 `INSTALL.codex.md` 一次完成仓库克隆、技能软链接和工具安装
- 已安装用户执行补充命令启用 `openharness`

## Stage Gates
- 明确为何不选 shell alias、原生二进制作为本轮主方案。
- 明确 CLI 正式包与脚本兼容层的边界。
- 明确安装命令、升级命令和已安装用户的迁移路径。
- 明确命令不存在时的回退方向：旧脚本入口仍可使用。

## Trade-offs
收益：

- 用户与智能体都能使用短命令，显著降低使用摩擦。
- 复用现有 Python CLI，改动成本可控。
- `--editable` 安装方便仓库自更新，与当前 `git pull` 模式兼容。

代价：

- 需要把 CLI 代码整理为正式可安装包。
- 命令安装与技能安装仍然是两步，不会像某些单体发行物那样“一条命令全包”。

为什么不选其他方案：

- 不选 shell alias：对交互式 shell 友好，但对 agent 运行环境和跨平台文档都不稳定。
- 不选原生二进制：当前需求只是提供统一命令入口，原生构建链会显著增加维护负担。
- 不选要求业务项目改 `pyproject.toml`：与“即插即用”目标冲突，也会污染接入仓库。

## Overview Reflection
反思结论：

- 从产品视角看，用户真正要解决的是“命令太长、安装后不会直接获得命令”，而不是“必须原生二进制”；因此全局命令比原生形态更接近问题本身。
- 从架构视角看，CLI 已经有清晰 parser 和 commands 分层，抽成正式包的风险低于继续堆叠脚本入口。
- 从测试视角看，必须保留旧脚本兼容层，否则现有测试和技能引用会同时断裂。
- 最大残余风险是打包配置调整后可能影响测试导入路径，因此需要用测试先锁定入口行为，再做迁移。
