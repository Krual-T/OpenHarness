# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
让 OpenHarness 的仓库自测和正式运行时入口按职责拆开：测试属于仓库顶层 `tests/`，正式 CLI 入口属于 `openharness_cli` 和控制台命令 `openharness`，不再通过 skill 目录里的脚本做兼容过渡。

## Problem Statement
- 现在的 `skills/using-openharness/tests/` 看起来像 skill 随仓库分发的一部分，但这些测试实际是在验证 OpenHarness 这个仓库自身的 CLI、协议文档和 task package 行为，不是给其他项目安装 skill 后运行的内容。
- `skills/using-openharness/scripts/openharness.py` 是历史兼容层，会让仓库同时存在“正式 CLI 入口”和“脚本兼容入口”两套路径，继续增加理解成本。
- 只要这两层还在，维护者就会继续在“仓库自测”和“skill runtime 资产”之间混淆边界。

## Required Outcomes
1. OpenHarness 自测迁移到项目顶层 `tests/`，包括测试聚合文件、测试用例、共享 `common.py` 和 `pytest` 配置。
2. `skills/using-openharness/scripts/openharness.py` 被彻底删除，仓库只保留 `openharness_cli` 和 `project.scripts` 暴露出来的 CLI 入口。
3. 所有仓库内活跃文档、测试导入和验证命令都改到新入口或新测试路径，不再依赖被删除的脚本路径。
4. 归档 task package 不需要逐个修改旧路径引用；旧测试和脚本路径通过 `docs/archived/legacy/` 中的历史快照继续满足证据校验。
5. 成功标准（single success metric）：仓库在没有 `skills/using-openharness/scripts/openharness.py` 的情况下，仍然可以通过顶层测试路径和 `uv run openharness` 完成自验证。

## Non-Goals
- 不批量重写历史归档 task package 中的旧证据内容；归档材料保留历史真实性。
- 不改变 `openharness` CLI 的命令集或行为语义。
- 不把 OpenHarness 自测纳入业务项目的 `openharness verify` 语义。

## Constraints
- 仓库协议要求先更新 task package，再做实现，再补验证与证据。
- 迁移后顶层测试路径必须仍然可以用 `uv run pytest ...` 独立执行，不能依赖已删除脚本去注入路径。
- `pyproject.toml` 的 `testpaths` 需要与新顶层测试路径一致。
- archived task package 的状态引用仍需要通过校验，因此必须为被删除的旧路径提供非运行时的历史快照落点。
- 反例（counterexample）：不能只是把文件物理挪到顶层，却仍然让测试通过 `skills/using-openharness/scripts/openharness.py` 间接导入 CLI；那样只是换目录，没有真正去掉兼容层。
