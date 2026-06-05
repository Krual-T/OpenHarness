# 详细设计

## 可观察性与验证准备

主验证路径：

- `uv run pytest tests/openharness_cases/test_task_package_core.py -q`：覆盖核心创建 API 和模板替换。
- `uv run pytest tests/openharness_cases/test_protocol_docs.py -q`：覆盖 CLI 帮助表面不再暴露 `--owner`。
- `uv run pytest tests/openharness_cases -q`：覆盖 OpenHarness 行为回归。
- `uv run openharness task-package list` 与 `uv run openharness task-package view TASK-022`：确认当前任务包可被 CLI 发现和查看。

降级路径：如果 Typer 对未知参数的错误文本在不同版本中不稳定，测试只断言命令退出非零和未创建任务包，不依赖完整错误文案。不能验证生成文件 owner 值和 CLI 参数移除时，不得宣称完成。

预期证据：

- 临时仓库中设置 `git config user.name "Temp Owner"` 后，新建任务包生成 `owner: "Temp Owner"`。
- `task-package new --help` 不包含 `--owner`。
- 传入 `--owner` 的调用失败，且不会创建任务包。
- 生成的 `task-info.yaml` 不残留 `<GIT OWNER>`。

## 新增或修改文件

- `openharness_cli/commands/task_package.py`：删除 `new_package()` 的 `owner` Typer 选项，调用核心创建时不再传 owner。
- `openharness_cli/core/task_packages.py`：删除或收窄 `create_task_package()` 的 owner 参数，创建时始终调用 `_resolve_owner()`；`task-info.yaml` 替换表新增 `<GIT OWNER>`。
- `openharness_cli/models/create_task_input.py`：如果仍保留 `owner` 字段，只作为内部已解析值；不再表示用户可传入值。
- `tests/openharness_cases/test_task_package_core.py`：把最小模板改为 `owner: <GIT OWNER>`，新增默认 Git owner 注入和 `--owner` 拒绝测试。
- `tests/openharness_cases/test_protocol_docs.py`：帮助文本断言改为不包含 `--owner`。
- `pyproject.toml`：patch 版本递增。
- `docs/archived/task-packages/git-owner-task-package-creation/`：记录需求、设计、验证和证据。

## 接口

CLI 接口：

- `openharness task-package new TASK_NAME [--title ...] [--summary ...] [--status ...]`
- 不再支持 `--owner`。Typer 对未知参数的默认错误传播即可，不增加自定义兼容提示。

核心接口：

- `create_task_package(ctx, *, task_name, title, summary="", status="proposing") -> tuple[Path, str]`
- owner 不再是公开输入；函数内部调用 `_resolve_owner()`。
- `_resolve_owner()` 不再需要接收候选 owner，直接返回 `get_git_author()`。

边界条件：

- `git config user.name` 返回空时，`get_git_author()` 继续回退 `unassigned`。
- Git 命令不可用、超时或 OS 调用异常时，继续回退 `unassigned`。
- 传入 `--owner` 是 CLI 误用，应失败而不是静默忽略。

## 模块内部设计

CLI 层只做人机接口适配：解析任务名、标题、摘要、状态，调用核心创建函数。

核心创建层负责编排：解析 owner、申请任务 ID、定位模板、渲染文件。`_create_task_package_unlocked()` 接收的 `CreateTaskInput.owner` 是已经解析后的内部值。

模板渲染层负责替换：普通 Markdown 文件使用原始替换值；`task-info.yaml` 使用 JSON 字符串包装，保证含空格、标点或非 ASCII 的 Git author 能生成合法 YAML。

测试层通过临时仓库控制 Git 配置，而不是传 owner 参数。这样测试观察点和真实 CLI 行为一致。

## 数据语义

`task-info.yaml.owner` 表示创建任务包时 Git 有效配置中的 `user.name`。它不是任务包后续认领机制，也不是命令行可覆盖字段。

模板占位符 `<GIT OWNER>` 表示“创建时自动注入 Git owner”。生成后的文件不得包含该占位符。`CreateTaskInput.owner` 如果保留，只表示内部已经解析完成的 owner 值，不表示外部输入。

## 阶段门禁

实施前已确定：

- 实现落点是 CLI 命令定义、核心创建流程、模板替换测试和帮助文本测试。
- owner 来源固定为 `git config user.name` 的有效结果。
- `<GIT OWNER>` 是唯一被支持的 owner 模板占位符。
- `--owner` 作为误用路径必须失败。
- 验证必须同时覆盖核心 API 和 CLI 表面。

## 决策闭合

接受：内部创建 API 收窄 owner 参数。理由是如果核心 API 继续暴露 owner，测试和未来调用仍可能绕开 Git 来源，和需求不一致。

拒绝：保留 `--owner` 作为兼容参数但忽略它。理由是静默忽略会让调用方误以为 owner 已生效，反而更难排查。

延期：是否把 `owner: <GIT OWNER>` 的历史归档包批量修正。本轮不处理，只有当后续校验要求历史包 owner 不得为占位符时再单独建包。

## 错误处理

主要静默出错风险是模板替换遗漏后仍生成合法 YAML，但 owner 值是 `<GIT OWNER>`。测试必须直接读取生成文件，断言 owner 等于 Git 配置值，并断言文本中没有 `<GIT OWNER>`。

CLI 误用 `--owner` 由 Typer 未知参数处理，错误向命令行调用者暴露。Git 配置缺失仍按现有行为写入 `unassigned`，不改变错误等级。

## 迁移说明

实施顺序：

1. 修改测试最小模板为 `<GIT OWNER>`，新增 owner 注入和 `--owner` 移除断言。
2. 修改核心创建流程和 CLI 命令签名。
3. 运行聚焦测试，再运行 OpenHarness case 回归和任务包校验。
4. 修正当前任务包文档状态和证据。

切换点是 `new_package()` 不再接受 `owner` 参数，以及 `create_task_package()` 不再允许外部传 owner。回滚触发点是现有测试或 CLI 新建流程无法创建任务包；回滚时恢复接口参数并重新评估 owner 来源策略。

## 推荐图示

不需要图示。函数调用链和数据语义都可以用本文件文字准确表达。

## 反思

验证策略必须覆盖真实模板，而不是测试自造的旧 `<OWNER>` 模板。否则即使测试通过，真实 `skills/using-openharness/references/templates/task-package.task-info.yaml` 仍可能留下 `<GIT OWNER>`。本轮测试样例需要同步改成 `<GIT OWNER>`，并增加直接文本断言。
