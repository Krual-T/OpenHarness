# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
让 `openharness update` 支持设置默认更新模式。用户可以把默认模式保存为普通同步或强制同步；之后无参数 `openharness update` 按保存的模式运行，同时仍能用单次参数覆盖默认值。

单一成功指标：自动化测试能证明默认未配置时行为兼容、设置默认模式后无参数 update 使用保存模式、单次参数可以覆盖保存模式，并且非法配置不会触发更新副作用。

## Problem Statement
目标用户是经常维护 OpenHarness 全局安装的使用者。核心场景是：用户已经知道自己希望 `update` 日常采用某种同步策略，例如总是先强制对齐 OpenHarness 源码 clone，再刷新 CLI。

上一轮已经增加了 `openharness update --force-sync`，但它仍要求用户每次记住并输入参数。如果某个安装环境长期需要强制同步，重复输入参数会把“默认操作习惯”留在用户记忆里，而不是进入 CLI 契约。反过来，默认模式又不能直接改成强制同步，因为这会让现有用户在无参数 update 时承担丢弃本地 clone 偏移的风险。

现在做这件事的原因是 update 已经出现两种同步模式；没有默认模式设置时，CLI 只能提供单次选择，不能表达用户级偏好。

## Required Outcomes
1. 支持通过 `openharness update --set-default-mode <mode>` 保存默认模式，最小 `acceptance criteria` 是配置文件被写入，输出说明保存的模式，并且该命令本身不执行 update。
2. 支持 `pull` 和 `force-sync` 两个模式，最小 `acceptance criteria` 是 parser 限制合法值，非法值不能进入 handler。
3. 无参数 `openharness update` 读取保存的默认模式；未保存时仍等价于 `pull`，最小 `acceptance criteria` 是测试能观察到命令序列。
4. 支持单次覆盖默认模式，最小 `acceptance criteria` 是 `--mode pull` 能覆盖保存的 `force-sync`，`--force-sync` 能覆盖保存的 `pull`。
5. 如果配置文件里存在非法模式，命令必须失败并且不执行 `git` 或 `uv` 命令。

## Non-Goals
- 不新增通用 `openharness config` 子命令；本轮只服务 `update` 的默认模式。
- 不做交互式确认、GUI 设置页或跨机器配置同步。
- 不改变 `--force-sync` 的既有语义。
- `counterexample`：支持为 `verify`、`bootstrap` 或 RWP 命令设置默认参数，看起来同属“默认设置”，但不属于本轮。

## Constraints
- 默认未配置时必须保持现有普通 `git pull` 行为。
- 保存位置必须是用户级配置，不能写入 OpenHarness 源码 clone 内的 tracked 文件，否则强制同步可能覆盖或污染仓库状态。
- 测试必须能隔离配置路径，不能读写真实用户家目录。
- `cost cap`：本轮只增加一个最小配置读写层和 update 参数，不引入全局配置系统。
