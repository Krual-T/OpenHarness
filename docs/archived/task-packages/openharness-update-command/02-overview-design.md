# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖：

- `openharness` CLI 的 parser 和 command handler。
- 更新命令使用的运行命令抽象。
- 安装与技能文档中的更新说明。

本轮不覆盖：

- 首次安装流程重构。
- Git 冲突解决、stash、强制 reset 等复杂仓库状态处理。
- 其他工具命令的自动更新。

## Proposed Structure
推荐在现有 CLI 中新增 `update` 子命令：

- parser 层暴露 `openharness update`。
- command handler 层计算 OpenHarness 仓库根目录，并顺序调用：
  - `git pull`
  - `uv tool upgrade openharness`
- 运行命令继续走统一的 `_run_command`，这样测试可以通过 monkeypatch 验证顺序和失败传播。

仓库根目录不从 `cwd` 推断，而是从当前安装包文件位置向上定位，确保命令在任意目录执行都更新 OpenHarness 自身仓库。

## Key Flows
成功流：

1. 用户执行 `openharness update`
2. CLI 解析到 `update`
3. 命令计算 OpenHarness repo root
4. 在 repo root 执行 `git pull`
5. 若成功，则执行 `uv tool upgrade openharness`
6. 输出完成提示并返回 0

失败流：

1. `git pull` 非 0 退出
2. 命令直接返回 1
3. 不执行 `uv tool upgrade openharness`

## Stage Gates
- 必须明确更新目标仓库的定位方式。
- 必须明确顺序依赖和失败中断语义。
- 必须明确文档中如何替换手工更新命令。

## Trade-offs
收益：

- 用户记忆成本进一步降低，更新流程与安装流程一样可文档化。
- 命令集中到 `openharness` 下，避免把运维知识散落在 README 和聊天里。

代价：

- CLI 需要对自身安装源目录有一个稳定判断。
- 如果用户是非标准安装路径，命令行为仍依赖当前安装包位置是否可映射到 git 克隆目录。

不选的方案：

- 不继续保留纯文档手工更新，因为这正是用户当前想消除的摩擦。
- 不把 `upgrade` 作为对外主命令，因为从用户视角这是“更新 OpenHarness”，而不是理解底层 `uv` 术语。

## Overview Reflection
反思结论：

- 从用户视角，`update` 比 `upgrade` 更贴近意图，因此对外命名应使用 `update`。
- 从架构视角，最关键的不是“能不能跑 `git pull`”，而是“默认更新正确的仓库”；因此 repo root 解析比简单用 `cwd` 更重要。
- 从验证视角，必须把失败中断写成测试，否则很容易出现 `git pull` 失败后仍继续运行 `uv tool upgrade` 的隐性错误。
