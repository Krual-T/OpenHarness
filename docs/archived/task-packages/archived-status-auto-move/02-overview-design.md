# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
覆盖 `openharness_cli` 读取 task package 时的目录规范化行为，以及对应 CLI workflow 测试。不覆盖任务完成判定、验证 artifact 生成规则、`verify` 命令是否自动推进状态，也不覆盖 project-memory 的 archive 语义。

## Proposed Structure
推荐把“active 根目录中出现 `status: archived` 包”的规范化放在 repository discovery 边界：`discover_task_packages` 在返回包列表前先把这类包移动到 archived 根目录，然后再按正常发现逻辑返回。

关键边界是：
- `repository.py` 负责发现目录和触发位置规范化。
- `lifecycle.py` 继续负责事务式移动、`STATUS.yaml` 状态确认和路径前缀重写。
- `validation.py` 继续保持最终不变量：`archived` 包必须位于 archived 根目录，非 archived 包不能位于 archived 根目录。

关键状态模型不变：`STATUS.yaml.status == archived` 表示该包不再 active；目录位置是这个状态的派生一致性要求。

## Key Flows
主路径：
1. CLI 调用 `discover_task_packages`。
2. 发现 active 根目录下某个包的 `STATUS.yaml.status` 是 `archived`。
3. 发现层调用生命周期归档 helper，将该包搬到 archived 根目录并重写包内路径。
4. discovery 继续扫描 archived 根目录，返回已归档位置下的 package。
5. 后续 `validate_task_package` 按现有不变量校验。

失败信号来自归档 helper 的返回值。如果目标 archived 目录已存在、事务移动失败或移动后的包校验不通过，CLI 应抛出明确错误，而不是静默保留不一致状态。

## Stage Gates
- 已决定自动移动触发点是 task package discovery，而不是 `verify` 成功后。
- 已决定复用现有归档 helper，避免重新写一套目录移动逻辑。
- 已决定保留最终位置校验，不把 active 根目录里的 archived 状态视为长期合法。
- 已识别主要失败模式：目标目录冲突、事务移动失败、包内路径重写后校验失败。

## Trade-offs
方案收益是任何读取 task package 的 CLI 入口都会先看到规范化后的目录状态，维护者不需要记住额外的手动搬目录步骤。代价是 discovery 从纯读取变成带副作用的规范化入口，因此必须让失败信号明确，并且只在 `status: archived` 这种已经表达归档意图的窄条件下触发。

备选方案是新增 `openharness normalize-archives` 命令。没有选择它，因为用户要求的是“归档状态自动移动”，单独命令仍然要求维护者记住额外步骤，不能解决状态和目录不同步的核心痛点。

## Recommended Diagrams
本轮流程短，测试用例比图更能稳定表达契约；不新增 `PlantUML` 图。

## Overview Reflection
挑战一：是否应该让 `verify` 通过后直接归档。结论是拒绝，因为这会把“验证证据”与“工作收尾决策”耦合，且会绕过人工更新 `04-verification.md` / `05-evidence.md` 的机会。

挑战二：discovery 带副作用是否过重。结论是接受这个代价，但把触发条件限制为 active 根目录下已明确写成 `status: archived` 的包，并复用事务式 helper 降低风险。
