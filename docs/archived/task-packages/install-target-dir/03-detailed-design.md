# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
- 用内容检查确认 `README.md` 与 `INSTALL.codex.md` 都已移除默认 `~` 主路径命令，并确认 INSTALL 明确要求 Agent 先询问目标目录。
- Fallback Path:
- 如果任务包校验失败，先修复任务包协议问题；如果任一安装文档仍残留默认 `~` 主路径，则不能宣称完成。
- Planned Evidence:
- `README.md` 与 `INSTALL.codex.md` 的修改内容。
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 的执行结果。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `INSTALL.codex.md`：改安装主路径说明。
- `README.md`：同步外层安装文案与示例。
- `docs/archived/task-packages/install-target-dir/*`：记录本轮需求、设计、验证和证据。

## Interfaces
外部稳定接口仍然是 `INSTALL.codex.md` 这份可抓取安装说明。它现在承诺的不是默认路径，而是一个顺序约束：先询问目标目录，再基于 `<target dir>` 执行命令。

## Stage Gates
- 测试策略：文档内容检查加任务包协议校验。
- 可观测性要求：用户必须能直接看到 “ask first” 与 `<target dir>` 占位符。
- 迁移顺序：先改 INSTALL，再改 README，最后写验证与证据。
- 预期证据类型：文件 diff 和 `check-tasks` 输出。

## Decision Closure
- 接受：使用 `<target dir>` 占位符来表达安装位置，因为这正是用户要求的结果形态。
- 拒绝：继续保留 `~` 作为默认示例路径，因为会与用户要求直接冲突。
- 延期：如果后续要开发真正的安装脚本，应另开 task package 处理。

## Error Handling
主要风险是文档只新增一句“先询问目录”，但命令本身仍残留写死路径。为了避免这种静默回退，本轮会把所有主路径命令和校验命令都切换到 `<target dir>` 形式。

## Migration Notes
这次只有文档迁移，不涉及代码迁移。旧安装用户无需被自动迁移；新安装流程从文档更新起生效。

## Detailed Reflection
本轮不需要补测试文件，因为变更对象是安装说明而不是运行时代码。验证路径虽然轻量，但与这次改动的真实风险是匹配的；扩大到脚本开发只会增加不必要范围。
