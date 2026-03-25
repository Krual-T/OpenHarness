# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把仓库内 `agents/openai.yaml` 的工具依赖声明从仓库自定义写法收敛到 OpenAI 当前公开支持的形状，避免测试继续把非官方 schema 当成“正确协议”。

## Problem Statement
当前多个技能把 `dependencies.tools` 写成字符串数组，例如 `["shell"]`，并且测试直接断言这一形状成立。用户指出 OpenAI 当前 Codex skills 示例使用的是结构化工具声明，这意味着仓库可能在给本地约定做回归，而不是给官方约定做回归。

外部核查后，问题进一步明确为两层：

1. 官方 `openai.yaml` 示例与官方代码中的 `SkillToolDependency` 都要求 `dependencies.tools` 是对象数组，而不是字符串数组。
2. 官方 skill 编写说明当前公开支持的工具依赖类型只有 `mcp`。仓库把 `shell` 写进 `dependencies.tools`，既不符合官方示例形状，也超出了当前公开支持范围。

## Required Outcomes
1. 找到仓库内所有使用字符串数组 `dependencies.tools` 的 `openai.yaml` 并完成收敛。
2. 基于 OpenAI 当前公开文档与官方代码，给出本仓库应采用的最保守兼容结论。
3. 移除或改写不符合官方当前支持范围的工具依赖声明，避免继续发布伪官方 schema。
4. 更新自动化测试，确保后续不会再把 `["shell"]` 这种本地写法当成正确结果。
5. 完成本任务声明的验证命令，并把外部核查证据写回任务包。

单一成功指标是：仓库 live repo skills 中不再存在字符串数组形式的 `dependencies.tools`，协议测试也不再断言 `["shell"]`。

Acceptance Criteria:
1. `skills/*/agents/openai.yaml` 中不再存在 `tools: - shell` 这种声明。
2. 测试会在 `dependencies.tools` 被写回字符串数组，或被写成当前官方未公开支持的类型时失败。
3. 任务包中记录了本轮采用的官方依据，包括公开示例和官方仓库中的解析类型。

Counterexample:
- 如果只是把测试从 `["shell"]` 改成别的本地约定，但仍然保留 `shell` 作为 `dependencies.tools` 的正式声明，本任务不算完成。

## Non-Goals
- 不重写技能正文，不改变隐式触发策略分层。
- 不新增本地私有解析器或 metadata 生成器。
- 不在本轮扩展到图标、品牌色等与本问题无关的 `interface` 字段优化。
- 不主动发明“shell 工具”的官方兼容形状；若官方未来公布，再单独跟进。

## Constraints
- 外部依据必须优先采用 OpenAI 官方公开文档与 OpenAI 官方代码仓库，不能用社区帖子代替。
- 仓库协议与任务包流程仍需遵守 `using-openharness` 约束。
- 本轮应以最保守兼容为准：对当前官方未公开支持的工具依赖，不做猜测性保留。
- 完成前至少运行 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 与本包声明的测试命令。
