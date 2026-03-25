# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 live skill surface 中残留的旧路径和失效引用收敛到当前仓库真实存在、可解析、可验证的状态，避免协作者在读取 skill 文档时被错误路径误导。

## Problem Statement
当前 `OH-022` 面向的是“skill 路径与引用漂移”问题，但仓库里并不是所有旧路径都同样重要。探索结果显示，active task packages 本身没有真实缺失路径；更突出的 live 问题集中在两类位置：

1. `skills/using-openharness/references/` 内部文档的交叉引用。
2. `skills/systematic-debugging/` 下维护者可见的测试与说明材料中，仍然保留旧入口 `skills/debugging/systematic-debugging`。

例如这些文档当前写着 `references/project-runtime-surface-map.md`、`references/adding-project-runtime-helper.md`、`references/runtime-capability-contract.md`。由于它们自己已经位于 `skills/using-openharness/references/` 目录下，这种写法会被解析成 `references/references/...`，实际指向不存在的路径。结果是维护者明明在读 live protocol docs，却会碰到会误导导航的失效引用。

例如 `skills/systematic-debugging/test-pressure-1.md`、`test-pressure-2.md`、`test-pressure-3.md`、`test-academic.md` 以及 `CREATION-LOG.md` 里，当前仍写着 `skills/debugging/systematic-debugging`。这个路径在仓库里已经不存在，会让后续 agent 或维护者误判真实 skill 入口。

如果这类问题继续存在，OpenHarness 的 live protocol surface 和维护材料就会逐步失去“仓库即事实源”的可信度：文档看起来完整，但引用链无法落到真实文件；后续再做 skill 元数据或协议整理时，也会继续在错误路径之上叠加修改。

## Target User And Scenario
- 目标用户是进入本仓库执行任务的协作者，以及维护 `using-openharness` 协议文档的人。
- 核心场景一是协作者从 `using-openharness`、`skill-hub` 或 runtime capability 相关参考文档继续跳转阅读时，能直接到达真实文件，而不是落到不存在的相对路径。
- 核心场景二是协作者阅读 `systematic-debugging` 的配套测试或创建说明时，不会再被旧 skill 路径误导。

## Success Metric
- 在本轮完成后，live skill surface 中的关键 reference docs 不再解析到不存在路径，且 `systematic-debugging` 的维护者可见材料不再保留旧 skill 入口，并有自动校验防止同类问题重新引入。

## Required Outcomes
1. 明确区分 live protocol surface 与 archived evidence，只把 live surface 里的真实失效路径纳入本轮修复范围。
2. 修复 `skills/using-openharness/references/` 下 runtime capability 相关文档之间的错误相对路径写法，使其在当前目录结构下可正确解析。
3. 修复 `skills/systematic-debugging/` 下维护者可见材料中的旧入口路径，使其与当前 skill 目录结构一致。
4. 审核与本轮主题直接相关的活跃文档表面，避免继续保留旧别名、失效 sibling path 或会误导执行的过期引用。
5. 增加一层轻量自动校验，覆盖 live skill docs 中的关键引用路径，防止未来再次写出同类失效路径。

## Acceptance Criteria
1. `skills/using-openharness/references/runtime-capability-contract.md` 中对 surface map 与 helper-addition 文档的引用，必须使用当前目录可解析的路径写法。
2. `skills/using-openharness/references/project-runtime-surface-map.md` 中对 helper-addition 文档的引用，必须使用当前目录可解析的路径写法。
3. `skills/using-openharness/references/skill-hub.md` 中对 runtime capability 相关参考文档的引用，必须使用当前目录可解析的路径写法。
4. 新增或扩展的 `pytest` 文本测试，能够在这些 live docs 再次写入失效 sibling path 时直接失败。
5. `skills/systematic-debugging/` 下已确认的旧入口引用全部改为当前有效路径，不再保留 `skills/debugging/systematic-debugging`。
6. 至少通过一次 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 和目标 `pytest` 校验。

## Non-Goals
- 不把所有 archived task package 中的历史路径文本都改成当前路径；归档材料保留历史证据属性，不作为本轮主修复面。
- 不在本轮重写整个 skill taxonomy、skill 元数据或所有文档风格。
- 不新增新的运行时 helper、运行时 surface，或改变 runtime capability contract 的语义边界；本轮只修路径与引用有效性。
- 不把占位符路径、通配路径或模板变量一律当成缺陷，例如 `docs/task-packages/<task>/`、`skills/<project-api-runtime>/SKILL.md` 不属于本轮 bug。

## Constraints
- 必须以 `AGENTS.md`、`skills/using-openharness/SKILL.md`、`skills/using-openharness/references/skill-hub.md` 为 live protocol surface 的主要事实来源。
- task package 正文保持中文，章节标题、状态值、YAML 键名、文件名与路径保持英文。
- 设计必须把“真实失效路径”和“示意占位路径”区分开，否则会误清理模板与归档证据。
- 防回归方案应优先复用现有 `skills/using-openharness/tests/openharness_cases/test_protocol_docs.py` 文本测试体系，而不是为文档问题引入重型新框架。

## Effort Boundary
- 本轮覆盖 `using-openharness` runtime capability 文档链路中的失效引用，以及 `systematic-debugging` 目录下已确认的旧入口路径清理，并配套必要的测试补强。
- 如果后续发现更大范围的路径治理需求，例如 archived package 批量重写或全仓库统一链接校验器，应拆成独立 task package。

## Counterexample
- 如果只是把失效路径改成另一种看起来更像路径的文本，但它在当前目录下仍然不存在，这不算完成。
- 如果只修正文档正文而不补自动校验，那么同类错误仍可能在后续编辑中再次出现，也不算真正闭环。
