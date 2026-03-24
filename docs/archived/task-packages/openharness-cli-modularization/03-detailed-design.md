# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 先新增结构兼容性测试并执行单测，确认在旧入口导入路径下能访问 `build_parser`、`main` 和核心公共符号。
- 再迁移实现代码，执行 `uv run pytest skills/using-openharness/tests/test_openharness.py`。
- 最后执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，确认 CLI 入口可用且仓库任务包协议未被破坏。
- Fallback Path:
- 如果拆分后的测试入口出现导入问题，先只保留入口重导出与少量模块迁移，确保行为稳定后再继续拆剩余模块。
- 如果 `check-tasks` 因任务包文档不完整失败，先补齐 task package 再继续，不得在验证失败时宣称完成。
- Planned Evidence:
- pytest 通过输出。
- `check-tasks` 通过输出。
- 任务包中的 `05-verification.md`、`06-evidence.md` 和自动生成的验证记录。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/scripts/openharness.py`：保留为薄入口与兼容导出层。
- `skills/using-openharness/scripts/<new-package>/*.py`：新增实现包，承载核心逻辑。
- `skills/using-openharness/tests/test_openharness.py`：保留为测试入口与聚合层。
- `skills/using-openharness/tests/<test-package>/*.py`：新增按职责拆分的测试模块。
- `docs/archived/task-packages/openharness-cli-modularization/*`：记录设计、验证和证据。

## Interfaces
稳定接口：
- CLI 入口路径仍是 `skills/using-openharness/scripts/openharness.py`。
- 顶层公开符号继续可通过 `import openharness` 访问。
- 测试入口文件仍是 `skills/using-openharness/tests/test_openharness.py`。

内部接口约束：
- 包内模块之间通过显式函数调用和数据类交互，不引入隐式全局状态。
- 命令处理器只组合领域函数，不直接操作文件系统细节以外的隐藏状态。

## Stage Gates
- 测试策略要先覆盖入口兼容性，再覆盖迁移后的主命令路径。
- 迁移顺序必须先建包和测试，再搬实现，最后收口入口文件。
- 需要保留可观测性：命令输出、验证产物和状态写回行为不能变化。
- 预期证据类型包括：失败后转绿的测试、完整 pytest 输出、`check-tasks` 输出、git diff。

## Decision Closure
接受：
- 入口文件保留但瘦身，作为兼容层存在。
- 实现包按领域模块拆分，而不是只按命令机械切块。

拒绝：
- 拒绝把实现包放到 skill 根目录，因为会增加脚本执行时的导入复杂度。
- 拒绝只拆测试不拆实现，因为无法解决主要维护成本来源。

延期：
- 是否进一步把测试中的共享 fixture 抽到 `conftest.py`，本轮视拆分后重复度再决定；如果拆完仍有明显重复，再单独开后续任务。

## Error Handling
需要防止三类失败：

1. 入口兼容失败：
   通过结构兼容性测试与保留顶层符号重导出来避免。
2. 包内循环依赖：
   通过把数据模型与基础工具放在低层模块，命令层只向下依赖来避免。
3. 测试重复收集或漏收集：
   通过明确的测试子包命名与入口聚合方式避免静默重复执行或完全不执行。

## Migration Notes
推荐迁移顺序：

1. 新增实现包骨架与测试子包骨架。
2. 新增入口兼容性测试，并先观察失败。
3. 按模块搬移 `openharness.py` 中的实现。
4. 调整入口脚本改为重导出和 `main()` 转发。
5. 拆分测试到子模块，保留入口文件作为聚合层。
6. 跑完整验证并更新 task package。

回滚注意事项：
- 如果中途发现公共符号兼容面判断错误，优先恢复入口文件导出面，再继续内部搬移。
- 不对外修改命令参数或输出语义，避免把结构重构升级成行为变更。

## Detailed Reflection
详细设计反思后，最关键的风险不是代码搬移量，而是入口兼容面和测试收集方式。如果先搬代码再想办法补兼容，很容易在中途把脚本和测试同时打碎；因此必须用测试先钉住入口导出面，再做内部重组。

测试视角挑战后补充了一个要求：测试拆分不能仅靠文件长度来判断，而要以职责边界分组，例如 manifest/task discovery、validation、task scaffolding、transition/archive、verify/CLI。这样未来新增测试才有稳定归属，不会再次退化成单文件堆积。
