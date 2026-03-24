# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮设计覆盖 `skills/using-openharness/scripts/` 与 `skills/using-openharness/tests/` 的结构重组，以及与之对应的任务包文档、验证命令和证据文件。

不纳入范围的部分包括：
- `references/` 下模板与说明文档的语义扩展。
- task package 历史归档内容的批量迁移。
- 仓库其他 skill 的实现重构。

## Proposed Structure
推荐方案是“稳定入口 + 内聚实现包 + 按职责测试分层”：

1. 保留 `scripts/openharness.py` 作为唯一脚本入口和兼容导出层。
2. 在 `skills/using-openharness/scripts/` 下新增实现包，例如 `openharness_cli/`，把数据模型、manifest 与 package 发现、校验、脚手架、状态流转、验证执行、CLI parser/command handlers 按模块拆开。
3. `openharness.py` 只负责从实现包导入公共常量、数据类、函数和 `main()`，维持现有导入习惯。
4. 在 `skills/using-openharness/tests/` 下新增测试子包，例如 `openharness_cases/`，按领域拆分测试模块；`test_openharness.py` 只保留共享导入准备和对子模块的聚合。

这样做的主路径最短：外部仍只看到旧入口文件，但维护者可以直接在包内部找到对应职责模块。

## Key Flows
主流程分成三层：

1. 入口层：
   `scripts/openharness.py` 暴露现有公共符号，CLI 运行时调用实现包中的 `main(argv)`。
2. 领域层：
   实现包内部按职责调用，例如 parser 将命令路由到 command handlers，handlers 再调用 task package、validation、verification、archival 等模块。
3. 测试层：
   `tests/test_openharness.py` 提供共享导入上下文，随后导入拆分后的测试模块；每个测试模块只覆盖一组职责。

关键数据流保持不变：
- `load_manifest` 仍从 repo 根定位 manifest。
- `discover_task_packages` 仍负责构造 `TaskPackage`。
- `validate_task_package` 仍作为校验聚合入口。
- `cmd_*` 处理器仍是 CLI 命令的主要对外语义边界。

## Stage Gates
- 需要明确新增包放在 `scripts/` 下，而不是 skill 根或仓库根，避免入口执行时额外改 `sys.path`。
- 需要明确入口文件只做重导出与 `main()` 转发，不保留业务实现。
- 需要明确测试拆分采用“入口聚合 + 子模块承载用例”的方式，避免 pytest 因双重发现导致重复执行。
- 需要明确失败模式与回滚方向：如果拆分过程中出现导入兼容问题，可以先保持旧顶层符号名不变，通过 `__init__` 和入口重导出来兜底。

## Trade-offs
考虑过三种方案：

1. 只在单文件内部做注释分段，不拆文件。
   收益最小，几乎不降低维护成本，直接排除。
2. 保留入口文件，在 `scripts/` 下新增实现包，并在 `tests/` 下新增测试子包。
   兼顾入口稳定、运行路径简单和后续扩展性，是推荐方案。
3. 在 skill 根新增通用包，例如 `skills/using-openharness/openharness/`，再让入口脚本额外改导入路径。
   结构看上去更“标准”，但脚本直跑时要处理路径问题，增加不必要的脆弱性。

因此选方案 2。它的代价是短期会有一轮较多的搬移与重导出，但收益是以后新增命令或校验逻辑时不必再进入大文件中心地带。

## Overview Reflection
架构反思后确认了两个约束：

1. 不应把实现包放到 skill 根目录。因为 `python skills/using-openharness/scripts/openharness.py ...` 运行时默认只保证 `scripts/` 在导入路径里，把包放到 `scripts/` 下可以避免再引入路径魔法。
2. 不应让测试拆分依赖 pytest 的隐式发现顺序。入口测试文件保留，子模块命名与导入方式要明确，避免既被入口导入又被 pytest 自动重复收集。

被拒绝的挑战：
- “按命令拆模块就够了，不用拆领域模块。”拒绝原因是很多逻辑跨命令复用，例如校验、归档与验证，不应被命令层复制。
- “把所有公共符号都留在入口文件，包只藏私有实现。”拒绝原因是这会让入口文件重新膨胀，违反本轮目标。
