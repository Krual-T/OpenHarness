# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖：

- `openharness_cli/cli.py` 中 `update` 子命令的参数和帮助文案。
- `openharness_cli/commands.py` 中 `cmd_update` 的分支编排。
- `tests/openharness_cases/` 中对 update 行为和帮助输出的断言。
- `INSTALL.codex.md` 中安装后更新说明。

本轮不覆盖：

- 任意业务仓库的同步或修复。
- 自动清理未跟踪文件、stash 本地改动、分支选择或鉴权处理。
- 首次安装命令和 project memory、RWP、task package 等其他 CLI 子命令。

## Proposed Structure
推荐在现有 `update` 子命令上增加布尔选项 `--force-sync`。

模块边界保持不变：

- parser 层只负责把用户意图转成 `args.force_sync`，并在帮助文案里说明风险。
- command handler 层根据 `args.force_sync` 选择普通同步或强制同步命令序列。
- `_run_command(repo_root, command)` 仍然是唯一外部命令执行适配层，测试继续通过 monkeypatch 观察命令序列。

关键状态模型只有一个布尔意图：`force_sync=False` 表示安全默认路径，`force_sync=True` 表示用户显式授权覆盖 OpenHarness 源码 clone 本地偏移。该状态不写入磁盘，也不影响其他命令。

## Key Flows
默认流：

1. 用户执行 `openharness update`。
2. handler 定位 OpenHarness repo root。
3. 在 repo root 执行 `git pull`。
4. `git pull` 成功后执行 `uv tool upgrade openharness`。
5. 任一步失败时返回 1，并打印失败步骤。

强制同步流：

1. 用户执行 `openharness update --force-sync`。
2. handler 定位 OpenHarness repo root。
3. 先执行强制同步命令序列，把本地 clone 对齐到上游跟踪分支。
4. 强制同步全部成功后才执行 `uv tool upgrade openharness`。
5. 强制同步任一步失败时返回 1，不继续刷新已安装 CLI。

关键失败信号来自 `_run_command` 的非 0 返回值；handler 不吞掉失败，也不把失败路径误报为成功。

## Stage Gates
- 已明确默认路径和强制路径的边界：默认不破坏，强制只在显式参数下发生。
- 已明确状态模型是单个 parser 布尔参数，不引入配置文件或持久状态。
- 已明确关键失败模式：强制同步失败、工具升级失败、帮助文案未提示风险。
- 已明确降级方向：如果强制同步路径不可用，用户仍可使用普通 `openharness update` 或手工处理 clone。

## Trade-offs
收益：

- 保持 `update` 作为单一更新入口，用户不需要回忆 OpenHarness clone 路径。
- 默认兼容现有安全行为，把破坏性操作限制在显式参数下。
- 命令序列可通过现有测试替身观察，不需要真实触碰用户 git 状态。

代价：

- `--force-sync` 需要清楚表达它可能丢弃 OpenHarness clone 的本地偏移。
- 强制同步依赖 clone 已有上游跟踪分支；没有上游时应失败并停止，而不是猜测远端分支。

备选方案一：把默认 `git pull` 改为强制同步。拒绝，因为这会让现有用户在无参数更新时承担丢弃本地 clone 改动的风险。

备选方案二：新增独立命令 `openharness force-update`。拒绝，因为这会把更新入口拆成两个命令，增加发现成本；布尔参数更贴合“同一更新流程的同步策略”。

## Recommended Diagrams
不需要新增图示。当前交互是单个 CLI 参数驱动的线性命令序列，文字和测试断言足以稳定表达。

## Overview Reflection
反思结论：

- 接受：强制同步必须显式 opt in，因为它有覆盖本地 clone 状态的风险。
- 接受：强制同步应发生在工具升级之前，否则已安装 CLI 可能刷新到未同步的本地源码状态。
- 拒绝：在本轮实现分支推断或冲突修复；如果 clone 没有上游跟踪分支，命令失败并把问题留给用户手工处理更清晰。
- 延期：如果未来需要支持未跟踪文件清理或更强的恢复流程，应单独设计交互和风险确认，而不是塞进这个参数。
