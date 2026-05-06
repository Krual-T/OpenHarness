# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先运行聚焦测试：`uv run pytest tests/openharness_cases/test_cli_workflows.py -q`。
  - 再运行全量测试：`uv run pytest -q`。
- Fallback Path:
  - 如果全量测试被无关历史失败阻塞，至少必须保留聚焦测试结果和失败摘要；不能宣称全量通过。
- Planned Evidence:
  - `04-verification.md` 记录实际执行命令和结果；`05-evidence.md` 记录改动文件、测试文件和残余风险。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `openharness_cli/cli.py`：注册 `init` 子命令和 `--repo` 参数。
- `openharness_cli/commands.py`：新增命令实现，负责创建 `.harness/.gitignore`。
- `openharness_cli/main.py` 与 `openharness_cli/__init__.py`：暴露命令包装，保持测试和公共入口一致。
- `tests/openharness_cases/test_cli_workflows.py`：增加解析和文件生成行为测试。

## Interfaces
新增用户接口为 `openharness init [--repo <repo>]`。稳定契约是目标仓库下 `.harness/.gitignore` 内容为 `*\n`。可观测入口是命令输出的初始化路径和测试直接读取生成文件。

## Module Internals
`cli.py` 只做 argparse 编排；`commands.py` 承担文件系统副作用；`main.py` 只转发到命令实现，避免命令注册和行为实现交叉。

## Data Semantics
唯一新增持久数据是文本文件 `.harness/.gitignore`，语义是忽略 `.harness` 目录内所有内容。内容必须保持为单行 `*` 加换行，避免不同平台读取时出现不稳定断言。

## Stage Gates
进入实现前必须有失败测试覆盖 parser handler 和生成文件内容；实现后必须看到聚焦测试变绿。

## Decision Closure
接受覆盖写入 `*\n`，因为本轮目标是确保 `.harness` 默认不被提交。拒绝完整初始化模板系统，触发条件是后续用户明确列出更多 `init` 初始化项。

## Error Handling
静默出错风险是命令成功但写到错误仓库。通过 `--repo` 解析为绝对路径并在输出里打印 `.harness` 路径降低该风险。文件系统异常本轮不吞掉，避免误报成功。

## Migration Notes
迁移顺序是先测试、再命令注册、再命令实现、最后导出入口。该命令是新增入口，不改变已有命令，回滚时删除新增 handler 和测试即可。

## Recommended Diagrams
不需要图。

## Detailed Reflection
测试策略聚焦真实文件系统副作用，比只断言 handler 更能捕捉实际价值。接口边界保持在 CLI 和目标仓库路径，不提前承诺后续初始化项。验证路径足以覆盖本轮风险。
