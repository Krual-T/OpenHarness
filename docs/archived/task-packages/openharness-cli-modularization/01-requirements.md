# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 `using-openharness` 的核心实现与测试从单一超大文件拆成可维护的模块结构，同时保持现有 CLI 行为、脚本入口路径和测试入口文件可继续使用。

## Problem Statement
当前 `skills/using-openharness/scripts/openharness.py` 同时承担 manifest 发现、task package 解析、文档校验、状态流转、归档、验证执行和 CLI 入口装配，职责边界已经混在一起。`skills/using-openharness/tests/test_openharness.py` 也把全部行为测试放在一个文件里，新增用例时难以定位归属，失败时很难快速建立问题范围。

如果继续在这两个大文件上迭代，后续每次加新命令、改校验逻辑或调状态流都容易扩大改动面，也会让测试冲突、阅读成本和回归风险持续上升。这轮需要先把结构理顺，再继续承接后续功能演进。

## Required Outcomes
1. 保留 `skills/using-openharness/scripts/openharness.py` 作为 CLI 入口和兼容导出面，但把主要实现迁移到新增包中。
2. 保留 `skills/using-openharness/tests/test_openharness.py` 作为测试入口，但把实际测试按职责拆到多个文件或子包中。
3. 模块边界至少要把数据模型与仓库发现、文档校验、任务脚手架、状态流转与归档、验证执行、CLI 装配区分开，避免再次回到单文件堆叠。
4. 现有对外行为保持稳定，至少覆盖 `bootstrap`、`check-tasks`、`new-task`、`transition`、`verify` 相关回归测试，并证明入口文件仍可工作。
5. 文档与任务包需要同步记录新的结构决策、验证命令和残余风险。

成功度量（success metric）：
1. `scripts/openharness.py` 与 `tests/test_openharness.py` 明显瘦身，核心实现和核心测试不再集中于单文件。
2. 现有核心测试命令通过，且新增结构相关回归测试能覆盖入口兼容性。

## Non-Goals
- 不在这轮修改 task package 协议语义、CLI 命令集或状态机规则。
- 不顺带重写所有文案、模板或历史 task package。
- 不为了拆文件而引入新的外部依赖或复杂插件机制。
- 不把入口文件彻底删除或改成不同调用方式。

## Constraints
- 必须遵守仓库协议：任务包正文使用中文，状态流与验证流程保持既有约束。
- 用户已经明确要求保留两个现有 `py` 文件作为入口，因此只能做薄入口适配，不能破坏原路径。
- Python 命令统一通过 `uv run ...` 执行。
- 重构应尽量保持公开符号兼容，因为现有测试和仓库内脚本可能直接 `import openharness` 并访问顶层函数。
- 需要用测试先行方式推进，至少先写会失败的结构兼容性测试，再做实现迁移。
- 反例（counterexample）：如果只是把单文件切成几个名字不同但仍强耦合的文件，入口仍需跨模块回收全部细节才能工作，这不算成功；如果测试只是机械拆文件而没有按职责分组，也不算成功。
