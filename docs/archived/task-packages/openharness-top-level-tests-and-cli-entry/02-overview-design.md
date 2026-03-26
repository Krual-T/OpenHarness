# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
- 覆盖范围包括三类表面：顶层测试目录结构、正式 CLI 入口与导出、以及引用这些路径的活跃文档和验证命令。
- 不纳入范围的是历史归档任务包中的旧证据回写，以及业务项目使用 OpenHarness 时的运行时逻辑。

## Proposed Structure
- 仓库自测统一落在顶层 `tests/`，其中保留 `openharness_cases/` 作为领域分组。
- 测试直接导入 `openharness_cli` 包，不再通过 `skills/.../scripts/openharness.py` 做桥接。
- `pyproject.toml` 的 `pytest` 配置改成指向顶层 `tests/`。
- 删除 `skills/using-openharness/scripts/openharness.py`，并同步清理活跃文档中对这个路径的依赖。
- 在 `docs/archived/legacy/skills/using-openharness/...` 下保留被移除旧树的历史快照，并让 archived package 校验支持这个回退位置。

## Key Flows
1. 顶层 `tests/` 负责 OpenHarness 仓库自测。
2. 测试通过正常 Python 包导入访问 `openharness_cli`。
3. CLI 自验证使用 `uv run openharness ...`。
4. `skills/using-openharness/` 只保留真正属于 skill runtime 的文档与 references，不再承载自测和脚本兼容层。
5. archived package 在校验引用路径时，优先检查仓库真实路径；若旧路径已被移除，再回退到 `docs/archived/legacy/<原路径>`。

## Stage Gates
- 需要明确哪些文件迁到顶层 `tests/`，哪些 runtime 资产仍留在 skill 目录。
- 需要明确删除脚本后测试如何获得同样的 CLI 访问能力。
- 需要明确活跃文档与 `pytest` 配置的落点，避免迁目录后继续引用旧路径。
- 需要明确 archived package 的历史引用如何保持可验证，而不逐个修改旧包。

## Trade-offs
- 收益是职责更清晰：skill 目录只放运行时资产，仓库自测回到顶层工程结构。
- 代价是会改动多处测试导入、验证命令和部分协议文档。
- 加入 legacy 快照的代价是会保留一份历史镜像，但它只用于 archived 证据校验，不参与 runtime。
- 不选“保留脚本但只是不推荐”，因为你已经明确要求不要兼容层。
- 不选“测试继续留在 skill 目录”，因为这会继续混淆“仓库自测”和“skill 分发内容”。

## Overview Reflection
- 挑战过的备选方案一是只删脚本、不迁测试，但这样测试目录仍然挂在 skill 下面，职责仍然不清。
- 备选方案二是只迁测试、不删脚本，但这样正式入口和兼容入口仍然并存，也没有达到你的目标。
- 备选方案三是逐个修改 archived task package 的旧路径引用，但这会对历史包做大量机械性改写，因此改为用 `docs/archived/legacy/` 承接历史快照。
- 因此这轮把测试迁移、兼容层删除、legacy 快照三件事绑定处理，边界才真正收敛。
