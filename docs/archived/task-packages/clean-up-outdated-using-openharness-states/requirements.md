# 需求

## 目标

清除 `skills/using-openharness/states/` 下已无引用的过时文件和目录，减少代码库噪音。

**单一成功指标**：4 个目标路径全部删除，`uv run pytest` 通过。

## 问题陈述

`skills/using-openharness/states/brainstorming/` 下残留了旧版可视化配套脚本（`scripts/`），以及仅被已归档任务包引用的参考资料（`references/spec-document-reviewer-prompt.md`、`references/visual-companion.md`）。同时，6 个 `states/*/agents/openai.yaml` 文件只有测试在检查其存在性，CLI 运行时完全不消费它们。这些文件增加阅读负担，让人误以为它们还在使用。

目标用户是 OpenHarness 维护者，核心场景是阅读和修改 `states/` 下的 SKILL.md 时不被已经死掉的文件干扰。

## 必须交付的结果

1. 删除 `skills/using-openharness/states/brainstorming/scripts/` 整个目录（含 5 个文件）
2. 删除 `skills/using-openharness/states/brainstorming/references/spec-document-reviewer-prompt.md`
3. 删除 `skills/using-openharness/states/brainstorming/references/visual-companion.md`
4. 删除 6 个 `states/*/agents/openai.yaml` 文件及其父 `agents/` 目录
5. 更新 `tests/openharness_cases/test_protocol_docs.py`，移除对 `agents/openai.yaml` 存在性的断言
6. `uv run pytest` 全部通过

## 非目标

- 不重命名任何目录或 SKILL.md 文件
- 不修改 `exploring-solution-space/` 的命名（名字与功能一致）
- 不增加新功能或新文件
- 不修改 CLI 代码

## 约束

- 删除后 `brainstorming/references/` 若为空目录，一并删除
- 删除操作后 `uv run pytest` 必须通过
- 不改变 CLI 的状态加载行为
