# 需求

## 背景

OpenHarness 通过 `openharness task-package new` 创建任务包，并从 `skills/using-openharness/references/templates/task-package.task-info.yaml` 生成 `task-info.yaml`。当前创建流程已经会调用 Git 配置解析 owner：未传入 owner 时读取 `git config user.name`，该命令会按 Git 的有效配置链读取仓库本地、全局和系统配置。

本轮排查发现，真实模板中的字段是 `owner: <GIT OWNER>`，但创建代码替换的是 `<OWNER>`。因此新建任务包会保留占位符，当前任务包自身的 `task-info.yaml` 也生成了 `owner: <GIT OWNER>`，说明自动注入没有生效。

## 问题陈述

维护者或 agent 新建任务包时，期望 `task-info.yaml.owner` 自动写入当前 Git 作者，作为任务包的机器可读事实。现在模板占位符和代码替换键不一致，新建结果留下 `<GIT OWNER>`，后续列表、查看、校验和归档都会带着错误事实继续流转。

同时 CLI 仍暴露 `--owner` 参数，允许调用方绕开 Git 作者来源手工指定 owner。这和本轮期望的事实来源不一致：任务包 owner 应来自当前仓库可见的 Git 配置，而不是每次创建时由命令行任意覆盖。

## 目标

完成后，新建任务包时 `task-info.yaml.owner` 必须来自 `git config user.name` 的有效结果；当仓库本地没有 `user.name` 时，应自然读取全局或系统配置。模板继续使用 `<GIT OWNER>`，代码负责替换该占位符。

完成后，`openharness task-package new --help` 不再出现 `--owner`，调用者不能通过该命令参数手工指定 owner。

## 交付物

- 修复任务包创建代码，使 `task-info.yaml` 模板中的 `<GIT OWNER>` 被解析后的 Git 作者替换。
- 移除 `task-package new` 命令的 `--owner` 参数，并调整内部创建 API，避免普通 CLI 路径继续传入 owner。
- 更新测试覆盖默认 Git owner 注入、显式 `--owner` 被拒绝，以及帮助文本不再展示 `--owner`。
- 记录验证命令和结果，证明修复覆盖新建任务包的实际行为。

## 非目标

- 本轮不重写历史归档任务包中的旧 owner 值；历史包里保留 `<GIT OWNER>`、`codex` 或其他值不属于本轮清理范围。
- 本轮不新增环境变量、配置文件或交互式提示来决定 owner；owner 来源限定为 Git 有效配置。
- 本轮不改变 `task-info.yaml` 的字段结构，也不重命名 `owner` 键。

## 约束

- 模板占位符必须采用 `<GIT OWNER>`，不能退回 `<OWNER>`。
- Python 命令继续使用 `uv run ...`。
- 版本号需要在提交前按 patch 版本递增。
- 变更必须保持现有 task package 创建、自动编号和阶段指令注入流程可用。

## 自检

- [x] 不了解本轮对话的人，读完「背景」和「问题陈述」，能知道当前需要做什么、为什么现在做。
- [x] 「目标」和「交付物」能直接判断完成状态。
- [x] 「非目标」包含了历史 owner 清理和新增 owner 来源这两个具体反例。
- [x] 「约束」写清了 `<GIT OWNER>`、Git 配置来源、版本号和现有流程兼容边界。
