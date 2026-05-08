# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖：

- `openharness_cli/cli.py` 的 `update` 参数表面。
- `openharness_cli/commands.py` 的 update 模式解析、配置读写和命令编排。
- `tests/openharness_cases/` 中对默认模式、单次覆盖、非法配置和帮助页的断言。
- `INSTALL.codex.md` 中面向用户的默认模式说明。

本轮不覆盖：

- 通用配置子系统或 `openharness config` 命令。
- 其他子命令的默认参数设置。
- 强制同步命令本身的语义扩展。

## Proposed Structure
推荐在 `update` 子命令内新增三类接口：

- `--set-default-mode {pull,force-sync}`：写入用户级配置并退出，不执行 update。
- `--mode {pull,force-sync}`：只影响本次 update。
- 既有 `--force-sync`：保留为单次强制同步快捷参数，等价于 `--mode force-sync`。

配置保存到用户级路径，优先使用 `XDG_CONFIG_HOME`，否则使用 `~/.config/openharness/config.yaml`。为了测试隔离，允许通过环境变量覆盖配置文件路径。

关键状态模型是 `update.default_mode`，合法值只有 `pull` 和 `force-sync`。解析优先级为：`--force-sync` 或 `--mode` 单次覆盖 > 保存的默认模式 > 内建默认 `pull`。

## Key Flows
设置默认模式：

1. 用户执行 `openharness update --set-default-mode force-sync`。
2. parser 限制 mode 只能是合法枚举。
3. handler 写入用户级配置。
4. 命令打印保存结果并返回 0，不执行 `git` 或 `uv`。

使用默认模式：

1. 用户执行 `openharness update`。
2. handler 读取用户级配置。
3. 如果 `update.default_mode` 是 `force-sync`，走强制同步路径；如果是 `pull` 或未配置，走普通 pull 路径。
4. 任一同步或升级命令失败时保持既有失败中断语义。

单次覆盖：

1. 用户执行 `openharness update --mode pull` 或 `openharness update --force-sync`。
2. handler 不采用保存默认值，而是按单次参数执行。

## Stage Gates
- 已明确配置范围只属于 `update.default_mode`。
- 已明确模式合法值和优先级。
- 已明确配置路径必须用户级并可测试隔离。
- 已明确非法配置必须失败且不执行副作用命令。
- 已明确默认未配置时兼容现有普通更新行为。

## Trade-offs
收益：

- 用户可以保存长期偏好，减少重复输入 `--force-sync`。
- 默认无配置仍保持安全兼容。
- 单次覆盖保留灵活性，避免默认设置变成隐式锁死。

代价：

- 引入了第一块 OpenHarness 用户级配置读取逻辑。
- 需要处理配置损坏或非法值，避免静默回退到错误模式。

备选方案一：只支持环境变量设置默认模式。拒绝，因为环境变量不够可发现，且难以通过 CLI 告知当前设置已保存。

备选方案二：新增全局 `openharness config set update.default_mode ...`。延期，因为这会变成通用配置系统设计，超出本轮成本上限。

## Recommended Diagrams
不需要新增图示。模式优先级和线性命令流程由文字和测试断言表达即可。

## Overview Reflection
反思结论：

- 接受：默认模式必须持久化到用户级配置，否则不算“设置默认”。
- 接受：非法配置不能静默回退到 `pull`，否则用户可能误以为强制同步已经生效。
- 拒绝：把配置写进 OpenHarness repo，因为强制同步本身会改变这个 repo 的状态。
- 延期：通用配置命令和查看全部配置的能力，等出现多个配置项后再设计。
