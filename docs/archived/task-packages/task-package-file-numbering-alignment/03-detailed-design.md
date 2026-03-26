# Detailed Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Runtime Verification Plan
- Verification Path:
  - 先修改协议测试和 task package 校验测试，让它们对新编号产生明确期待。
  - 执行 `uv run pytest tests/openharness_cases/test_protocol_docs.py`
  - 执行 `uv run pytest tests/openharness_cases/test_task_package_core.py`
  - 执行 `uv run pytest tests/openharness_cases/test_cli_workflows.py`
  - 执行 `uv run openharness check-tasks`
- Fallback Path:
  - 如果批量重命名后出现大量路径失败，需要继续把遗漏引用补齐；在 `check-tasks` 没有回绿之前不能宣称完成。
- Planned Evidence:
  - 新编号模板与协议测试通过记录。
  - 仓库内 task package 文件名批量切换后的 diff。
  - `openharness check-tasks` 通过记录。

只有当详细设计已经具体到可以执行时，才进入 `in_progress`。
如果设计已经完成但实现尚未开始，应保持在 `detailed_ready`。

## Files Added Or Changed
- `skills/using-openharness/references/manifest.yaml`：更新 required files 与 discovery order。
- `skills/using-openharness/references/templates/`：模板文件改名与内容改号。
- `openharness_cli/constants.py`、相关实现与测试：切到新编号。
- `docs/task-packages/` 与 `docs/archived/task-packages/`：真实文件批量改名和引用修正。
- `AGENTS.md` 与相关协议文档：同步更新阅读顺序和说明。

## Interfaces
- task package 的稳定文件接口改为 `04-verification.md` 与 `05-evidence.md`。
- `STATUS.yaml.evidence.docs`、`entrypoints` 与文档正文中的路径引用都必须遵守新接口。
- `validate_task_package` 与测试断言将只承认新编号。

## Stage Gates
- 必须先有测试对新编号的失败信号，再写实现。
- 必须完成真实文件重命名，而不是只改字符串常量。
- 必须保证 active 和 archived task package 都能通过校验。

## Decision Closure
- 接受：整仓一次性切换到连续编号。
- 拒绝：保留双编号或别名文件。
- 拒绝：只更新模板、不更新现有 task package。

## Error Handling
- 如果某个 task package 重命名后路径引用漏改，`check-tasks` 应显式报错。
- 如果测试仍然引用旧编号，应优先修测试与协议源，不允许靠兼容逻辑吞掉错误。

## Migration Notes
- 先改协议和测试，再做批量重命名与文本替换，最后跑整仓校验。
- 本轮没有兼容策略；切换完成后仓库以新编号为唯一现行协议。
- 如果需要回滚，应整体回滚，不做局部回退。

## Detailed Reflection
- 这轮最容易出错的地方不是改模板，而是遗漏 archived package 中的路径引用，所以最终验证必须依赖整仓 `check-tasks`。
- 只要协议测试、task package 核心测试和 `check-tasks` 都通过，就说明新编号已经真正落地，而不是停留在表面文案。
