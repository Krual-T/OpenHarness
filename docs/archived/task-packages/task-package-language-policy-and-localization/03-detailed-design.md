# Detailed Design

## Runtime Verification Plan
- Verification Path:
  - 运行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k 'language_policy or chinese_narrative or repo_protocol_documents_task_package_language_policy'`，先锁定本轮新增约束
  - 运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
  - 运行 `uv run pytest`
- Fallback Path:
  - 如果新增定向测试失败，先修复模板或协议文档，再继续跑全量验证
  - 如果全量验证被无关失败阻塞，就保留包在未归档状态，并明确记录阻塞项，而不是宣称已经完成
- Planned Evidence:
  - 任务包模板明确写出“正文中文优先、结构英文保留”的规则
  - `AGENTS.md` 与 `using-openharness` 入口协议显式记录该策略
  - `OH-015` 自身补齐实现、验证、证据并归档

Move to `in_progress` only when detailed design is concrete enough to execute.
If design is complete but implementation has not started yet, stay at `detailed_ready`.

## Testing-First Design
本轮不再只是设计包，而是直接完成第一阶段落地。测试先行策略如下：

- 先新增失败测试，约束模板和入口协议文档必须声明中文优先叙述策略
- 再实现模板、协议说明和 `OH-015` 自身文档改动
- 最后用 `check-tasks` 与 `pytest` 验证仓库协议和回归都仍然成立

## Files Added Or Changed
- 更新 `AGENTS.md`，把 task package 语言策略写进仓库协议
- 更新 `skills/using-openharness/SKILL.md`，让入口 skill 显式教这条规则
- 更新 `skills/using-openharness/references/templates/task-package.*`，让新包默认输出中文正文引导
- 更新 `skills/using-openharness/tests/test_openharness.py`，给模板与协议文档加回归测试
- 更新 `docs/archived/task-packages/task-package-language-policy-and-localization/*`，把本包补成已实现、可验证、可归档状态

## Interfaces
- Language policy interface:
  - task package Markdown 正文默认中文
  - 英文章节标题、命令、状态值、YAML 键名、文件名和路径保持不变
- Repository protocol interface:
  - `AGENTS.md` 和 `using-openharness` 必须让协作者一进入仓库就看到这条规则
- Validator interface:
  - 第一阶段不修改校验器，继续沿用现有英文章节锚点
- Template interface:
  - 模板继续输出英文标题，同时把正文提示语改成中文

## Error Handling
- 如果有人在没有改校验器的情况下直接把标题翻成中文，`check-tasks` 会失败；这类改动必须在单独实现包里一次性完成。
- 如果有人把命令、状态值或 YAML 键名也本地化，就会破坏协议表面；这些元素必须继续保留英文。
- 如果仓库在第一阶段之后仍然觉得英文标题阅读成本高，就开启第二阶段实现包，而不是在各个任务里零散混改。

## Migration Notes
- Recommended rollout order:
  1. 先把 task package 的正文写法、入口协议和模板切到中文优先
  2. 保留英文标题、文件名、状态值、命令和键名
  3. 完成一轮实际使用后，再评估标题本地化是否值得单独实现
- 本轮完成第一阶段产品化，但不会进入第二阶段的标题本地化实现。

## Detailed Reflection
- 我再次挑战了“要不要现在就决定中文标题方案”。结论仍然是不需要；仓库可以先拿到主要收益，再决定要不要承担第二阶段改造成本。
- 我也检查了第一阶段会不会过于保守。答案是它确实保守，但这是有意为之，因为它在解决核心阅读问题的同时，把迁移风险压到最低。
- 我还检查了本包是不是应该顺手把整个仓库都本地化。结论仍然是否定的；task package 及其写作协议才是这一轮最关键、最高频的目标表面。
