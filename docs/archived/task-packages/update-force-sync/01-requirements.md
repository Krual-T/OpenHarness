# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
让 `openharness update` 支持一个显式参数来控制强制同步，使用户在 OpenHarness 源码 clone 与上游不一致、普通 `git pull` 无法满足更新需求时，可以通过 CLI 完成一次有意的强制同步并刷新已安装工具。

单一成功指标：自动化测试能证明默认更新行为不变，并能证明 `openharness update --force-sync` 会按预期执行强制同步路径后才运行 `uv tool upgrade openharness`。

## Problem Statement
目标用户是通过全局 `openharness` 命令维护 OpenHarness 自身安装的使用者。核心场景是：用户在任意业务仓库中执行 `openharness update`，希望更新的是 OpenHarness 源码 clone 和已安装 CLI，而不是当前业务仓库。

现有 `update` 只执行普通 `git pull`。这对干净 clone 是安全默认值，但在本地 clone 出现偏离上游、普通 pull 无法完成、或用户明确希望丢弃本地 clone 偏移时，仍然需要手工回到 OpenHarness clone 里执行强制同步步骤。这个手工路径重新暴露了原本 `update` 命令要隐藏的安装源路径和命令顺序。

现在做这件事的原因是 `update` 已经成为官方更新入口；强制同步如果继续留在聊天或手工经验里，会让用户在最需要恢复一致状态时绕开 CLI 契约。

## Required Outcomes
1. CLI 增加显式 `--force-sync` 参数，最小 `acceptance criteria` 是 parser 能解析该参数，且 `update --help` 解释它会覆盖 OpenHarness 源码 clone 的本地偏移。
2. 默认 `openharness update` 行为保持兼容，最小 `acceptance criteria` 是现有成功路径仍然只按 `git pull`、`uv tool upgrade openharness` 的顺序执行。
3. `openharness update --force-sync` 走强制同步路径，最小 `acceptance criteria` 是测试能观察到强制同步命令先于 `uv tool upgrade openharness`，并且任一强制同步步骤失败时不会继续升级工具。
4. 文档或帮助面必须让用户看见强制同步是显式选择，而不是默认行为。

## Non-Goals
- 不做通用 git 修复器；`--force-sync` 只服务 OpenHarness 自身源码 clone。
- 不自动处理未跟踪文件清理、stash、冲突诊断或分支选择交互。
- 不改变首次安装流程，也不改变 `uv tool upgrade openharness` 作为刷新已安装 CLI 的底层步骤。
- `counterexample`：给任意业务项目增加类似 `openharness update --force-sync --repo <project>` 的强制同步能力，看起来相关，但不属于本轮。

## Constraints
- 默认路径必须保持非破坏性，不能让现有 `openharness update` 隐式丢弃本地 clone 改动。
- 强制同步参数必须足够显式，避免用户把它误认为普通更新。
- 测试不能真实执行用户环境中的 `git pull`、`git reset` 或 `uv tool upgrade`，必须通过 monkeypatch 的命令记录验证顺序和失败中断。
- `cost cap`：本轮只修改 CLI parser、update handler、相关测试和面向安装/帮助的文案，不重构通用命令运行层。
