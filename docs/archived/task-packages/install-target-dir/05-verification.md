# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path: 通过安装文档内容检查确认默认 `~` 主路径已移除，再执行仓库任务包校验确认文档与归档状态合法。
- Executed Path: 先执行 `rg -n "~/.codex/openharness|~/.agents/skills/openharness|ask the user|<target dir>" README.md INSTALL.codex.md docs/archived/task-packages/install-target-dir -S`，确认安装主路径已经切换到先询问目录、再使用 `<target dir>`。首次执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 时，发现无关任务包 `skill-openai-tool-schema-alignment` 的 `STATUS.yaml` 仍保留模板占位路径；修正后再次执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 通过。
- Path Notes: 本轮只涉及文档修改，因此以内容检查和任务包协议校验为主，不涉及运行时安装测试。仓库级校验中的失败点是既有元数据问题，已单独修复后重新验证通过。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- 任务包结构通过校验，且安装主路径不再把 `~` 当作默认目标目录。

## Traceability
- 需求要求去掉默认 `~` 路径并改成主动询问目录；设计把这个要求落到 `README.md` 与 `INSTALL.codex.md`；验证通过文件内容检查与 `check-tasks` 结果确认落地。

## Risk Acceptance
- 接受一个残余风险：Agent 是否严格遵循文档仍取决于其执行质量。若后续发现这类偏差持续发生，再单独引入脚本化安装。

## Latest Result
- 2026-03-25: PASS
- `rg -n "~/.codex/openharness|~/.agents/skills/openharness|ask the user|<target dir>" README.md INSTALL.codex.md docs/archived/task-packages/install-target-dir -S`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- 2026-03-25: PASS after archival
- `uv run python skills/using-openharness/scripts/openharness.py bootstrap`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Latest Artifact: `docs/archived/task-packages/install-target-dir/05-verification.md`
