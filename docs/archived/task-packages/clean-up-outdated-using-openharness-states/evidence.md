# 验证证据

## 文件

| 文件 | 改动 |
|------|------|
| `skills/using-openharness/states/brainstorming/scripts/` | 删除（5 个文件，旧可视化配套脚本） |
| `skills/using-openharness/states/brainstorming/references/spec-document-reviewer-prompt.md` | 删除（仅考古引用） |
| `skills/using-openharness/states/brainstorming/references/visual-companion.md` | 删除（零外部引用） |
| `skills/using-openharness/states/brainstorming/references/` | 删除（空目录） |
| `skills/using-openharness/states/*/agents/openai.yaml` | 删除（6 个文件，CLI 不消费） |
| `skills/using-openharness/states/*/agents/` | 删除（6 个空目录） |
| `tests/openharness_cases/test_protocol_docs.py` | 移除 state skills 的 openai.yaml 检查和不再使用的常量 |

## 测试结果

### RED

```
uv run pytest tests/openharness_cases/test_protocol_docs.py
```
退出码 1 — 6 个测试失败（4 个 agents/openai.yaml 相关 + 2 个预存 README 失败）

### GREEN

```
uv run pytest tests/openharness_cases/test_protocol_docs.py
```
退出码 1 — 4 个相关测试修复通过，2 个预存 README 失败（`test_readme_describes_plug_and_play_harness_and_python_pytest_floor`、`test_readme_describes_runtime_capability_contract`）与本次改动无关

### REFACTOR

清理了 `test_protocol_docs.py` 中不再使用的常量（`STATE_SKILLS`、`STATE_SKILLS_IMPLICIT`、`STATE_SKILLS_EXPLICIT`、`STATES_BASE`），测试结果不变。

## 验收标准覆盖

| 需求 | 状态 |
|------|------|
| 删除 brainstorming/scripts/ | 通过 |
| 删除 brainstorming/references/ 下 2 个文件 | 通过 |
| 删除 6 个 agents/openai.yaml | 通过 |
| test_protocol_docs.py 适配 | 通过 |
| pytest（本次相关）通过 | 通过 |

## 验证结果

**有条件通过。**

本次 5 项需求全部满足，相关 17 个测试通过。2 个预存 README 测试失败（`test_readme_describes_plug_and_play_harness_and_python_pytest_floor`、`test_readme_describes_runtime_capability_contract`）与本次改动无关，属 README 内容更新后测试未同步。

## 残余风险

- 2 个预存 README 测试失败未被修复——不在本轮范围，已在 `verification-design.md` 风险接受中声明
- 已归档任务包中引用被删文件的路径保持原样——历史记录，不影响功能

## 后续事项

- `test_protocol_docs.py` 中 2 个 README 测试需单独处理，建议新建任务包修复或更新 README 使其与测试对齐
