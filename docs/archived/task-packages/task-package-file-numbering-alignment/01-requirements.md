# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
把 task package 文件编号收敛成连续序列，消除当前缺失 `04-*` 的结构噪音，并让 OpenHarness 协议、模板、测试和现有 task package 都稳定落在同一套编号上。

## Problem Statement
- 当前协议实际使用的文件是 `01-requirements.md`、`02-overview-design.md`、`03-detailed-design.md`、`04-verification.md`、`05-evidence.md`，编号不连续，维护者会自然怀疑是否缺文件或是否还有隐藏协议。
- 这个空洞不是功能问题，而是历史演化遗留，但只要协议仍然暴露这组编号，认知成本就会持续存在。
- 由于 manifest、模板、校验器、测试和现有 task package 都已绑定这组旧编号，不能只改其中一层；否则仓库会进入半新半旧状态。

## Required Outcomes
1. 协议源统一改为连续编号：`04-verification.md` 和 `05-evidence.md` 取代旧的 `04-verification.md` 和 `05-evidence.md`。
2. `manifest.yaml`、模板、`openharness_cli/constants.py`、协议文档和测试全部切到新编号。
3. 现有 active 与 archived task package 的真实文件名需要完成重命名，并同步修正内部引用和 `STATUS.yaml` 中的路径。
4. 不保留双编号兼容模式，也不依赖 legacy 回退来掩盖编号切换。
5. 成功标准（single success metric）：仓库中不存在仍被协议引用的 `04-verification.md` / `05-evidence.md` 作为现行编号，且 `openharness check-tasks` 仍然通过。

## Non-Goals
- 不改变 task package 的阶段语义或章节内容。
- 不修改 `README.md`、`STATUS.yaml`、`01`、`02`、`03` 的职责划分。
- 不通过增加“别名文件”来保留旧编号。

## Constraints
- 仓库协议要求 task package、模板、校验器和测试保持一致，不能只改文档不改实现。
- 编号调整会触达 active 和 archived task package，因此需要批量重命名文件并同步路径引用。
- 由于 archived package 也是当前协议校验的一部分，这轮不能只改 active 包。
- 反例（counterexample）：如果最终只是模板改成 `04/05`，但仓库里现有 task package 还停留在 `05/06`，那就是半迁移状态，不可接受。
