# 总体设计

## 系统边界

本轮覆盖 `openharness task-package new` 的创建入口、内部创建 API、任务包模板替换逻辑，以及对应的 CLI/核心测试。具体表面包括：

- `openharness_cli/commands/task_package.py`：移除 `new` 命令的 `--owner` 选项，不再从 CLI 接收 owner。
- `openharness_cli/core/task_packages.py`：保持 owner 解析集中在创建流程内部，并让 `<GIT OWNER>` 成为模板替换键。
- `skills/using-openharness/references/templates/task-package.task-info.yaml`：保留 `owner: <GIT OWNER>` 这个模板事实。
- `tests/openharness_cases/`：覆盖新建任务包时 owner 注入、`--owner` 参数消失和拒绝。

不覆盖历史归档任务包的 owner 修复，不新增其他 owner 来源，不改变 `task-info.yaml` 的字段结构，也不改变任务包编号、阶段流转和模板查找策略。

## 推荐结构

推荐方案是“模板语义不变，代码适配模板”。`get_git_author()` 继续负责读取 Git 有效配置；`create_task_package()` 继续在内部解析 owner；`_create_task_package_document()` 在渲染 `task-info.yaml` 时替换 `<GIT OWNER>`。CLI 层只提供任务名、标题、摘要和状态，不再提供 owner 参数。

责任边界如下：

- Git owner 来源在 `openharness_cli/core/utils.py`，不扩散到 CLI 参数层。
- 创建流程在 `openharness_cli/core/task_packages.py`，负责把解析后的 owner 注入模板。
- 模板仍表达“这里是 Git owner 自动字段”，不改回通用 `<OWNER>`。
- Typer 命令定义只暴露允许用户决定的输入，owner 不属于用户创建时可覆盖输入。

## 关键流程

主流程：

1. 用户执行 `openharness task-package new <name>`。
2. CLI 层不接收 owner，调用 `create_task_package()`。
3. 创建流程调用 `get_git_author()`，由 `git config user.name` 返回当前仓库可见的有效 Git 配置；仓库本地未配置时，Git 会继续读取全局或系统配置。
4. 创建流程渲染 `task-info.yaml`，把 `<GIT OWNER>` 替换成解析后的 owner。
5. 如果 Git 没有可用 `user.name`，现有行为保持为写入 `unassigned`。

关键失败信号有两类：生成文件仍包含 `<GIT OWNER>`，或 CLI 帮助/调用路径仍接受 `--owner`。二者都用测试直接断言。

## 阶段门禁

进入详细设计前必须固定以下条件：

- 模板占位符采用 `<GIT OWNER>`，实现不能改回 `<OWNER>`。
- CLI 用户不能通过 `--owner` 指定 owner。
- Git 配置读取采用 `git config user.name` 的有效结果，不手工拼接本地和全局配置读取逻辑。
- 回退路径保持现有 `unassigned`，不在本轮新增错误中断或交互提示。
- 本地无可用 RWP：已执行 `uv run openharness rwp list`，输出 `No runtime workflow packages found.`；本轮采用 pytest 和 CLI smoke 验证。

## 取舍

选择适配 `<GIT OWNER>` 的原因是它更准确表达模板字段含义，也符合维护者明确边界。代价是需要更新测试里的最小模板样例，避免测试继续使用旧 `<OWNER>` 掩盖真实模板行为。

备选方案一是把真实模板改回 `<OWNER>`。这个方案改动更小，但违背本轮要求，也会让模板失去“自动 Git owner 字段”的表达，因此拒绝。

备选方案二是保留 `--owner`，但默认仍走 Git。这个方案兼容旧命令调用，但会继续允许调用方写入非 Git 来源 owner，和本轮“owner 事实只来自 Git 配置”的目标冲突，因此拒绝。

## 推荐图示

本轮是窄 CLI 与模板修复，不需要图示。流程由“CLI 输入 -> 创建 API -> Git owner 解析 -> 模板替换 -> task-info.yaml”这条文字链路即可准确表达。

## 反思

需要挑战的风险是：移除 `--owner` 是否会破坏内部测试或未来程序化调用。结论是 CLI 表面必须移除；内部 `create_task_package()` 也应收窄 owner 参数，避免普通调用继续绕开 Git 来源。测试中如果需要控制 Git owner，应通过临时仓库的 `git config user.name` 设置，而不是传 `owner=`。这样验证对象和真实用户路径一致。
