# Verification

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Verification Path
- Planned Path:
  - `uv run pytest skills/using-openharness/tests/test_openharness.py -k "openai_metadata"`
  - `uv run pytest skills/using-openharness/tests/test_openharness.py`
  - `uv run python skills/using-openharness/scripts/openharness.py check-tasks`
- Executed Path:
  - 已执行 `uv run pytest skills/using-openharness/tests/test_openharness.py -k "openai_metadata"`，结果为 5 passed。
  - 已执行 `uv run pytest skills/using-openharness/tests/test_openharness.py`，结果为 73 passed。
  - 已执行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks`，结果为通过，校验了 active 与 archived 共 27 个任务包。
- Path Notes:
  - 本轮除了本地验证，还额外核对 OpenAI 官方仓库中的公开示例与参考说明，作为“与官方对齐”的外部证据。

只有当实现已经完成到足以采集新证据时，才进入 `verifying`。
如果实现仍然延期到后续轮次，就不要使用 `archived`。

## Required Commands
- `uv run pytest skills/using-openharness/tests/test_openharness.py -k "openai_metadata"`
- `uv run pytest skills/using-openharness/tests/test_openharness.py`
- `uv run python skills/using-openharness/scripts/openharness.py check-tasks`

## Expected Outcomes
- metadata 相关用例通过。
- 完整 harness 测试入口通过。
- `check-tasks` 通过，且任务包结构完整。
- 仓库内不再出现 `dependencies.tools` 的字符串数组写法。

## Traceability
- `01-requirements.md` 定义了“消除字符串数组与非官方 `shell` 依赖”的完成条件。
- `02-overview-design.md` 解释了为什么本轮必须删除 `shell` 而不是结构化保留。
- `03-detailed-design.md` 把修改文件、测试策略和验证路径具体化。
- 本文件与 `05-evidence.md` 将承接命令结果和外部官方依据。

## Risk Acceptance
- 当前接受的残余风险是：若 OpenAI 很快公开支持 `shell` 依赖，本仓库会暂时显得比官方能力更保守。
- 这个风险可以接受，因为保守缺失优于错误宣称支持；一旦官方文档明确新增类型，应重新开任务包跟进。

## Latest Result
- 2026-03-25 已完成本轮全部必需验证，结果通过。
- Latest Artifact:
  - 官方外部依据：
    - `https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/skill-creator/references/openai_yaml.md`
    - `https://raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/assets/samples/openai-docs/agents/openai.yaml`
    - `https://raw.githubusercontent.com/openai/codex/main/codex-rs/app-server-protocol/schema/typescript/v2/SkillToolDependency.ts`
