# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
这个 package 覆盖 OpenHarness 的例行维护协议，而不是单个功能流。它关心的是哪些仓库表面需要定期审计、如何串联已有工具、以及发现问题后该写回哪个事实源。

本轮覆盖的表面有三类：

- `docs/task-packages/` 与 `docs/archived/task-packages/` 中的 task package 健康度与父子包一致性。
- `.project-memory/` 中事实、决策、别名和新鲜度元数据。
- `skills/using-openharness/references/skill-hub.md`、`README.md` 与 live skill docs 的文本漂移。

本轮不覆盖新的运行时 helper 设计，也不直接实现一个统一维护命令；那些工作只有在手工维护路径被证明重复且高频时才需要单独拆包。

## Proposed Structure
推荐方案不是在本轮立刻引入一个大而全的维护入口，而是先把维护流固定成三段式审计结构，并让每段都复用现有能力：

1. `task package health audit`
   - 复用 `uv run python skills/using-openharness/scripts/openharness.py check-tasks` 与 `bootstrap`。
   - 负责发现 package 结构损坏、状态与文档锚点不一致、父级路线图与活跃子包脱节等问题。
2. `project memory freshness audit`
   - 复用 `uv run python skills/project-memory/scripts/check_stale.py` 与 `audit_memory.py`。
   - 负责发现 stale object、缺失元数据、alias 噪声，以及哪些 memory object 需要重新验证或归档。
3. `skill surface drift audit`
   - 复用 live docs 与现有 `pytest` 文本测试。
   - 负责发现 skill hub、README 与 per-skill 文本表述再次分叉的情况。
4. `focused remediation policy`
   - 如果发现是低噪声、边界清晰、不会扩展协议的新问题，就在 `OH-017` 内直接修复。
   - 如果发现需要新增共享命令、模板或协议层规则，就从 `OH-017` 再拆一个 focused child package。

推荐先执行 `project memory freshness audit` 作为首个实施波次，因为当前仓库已经有真实、边界清晰且可验证的 stale findings，这比抽象地先发明一个维护命令更务实。

## Key Flows
主流程如下：

1. 用户请求继续 `OH-004` 或处理维护问题。
2. 代理先进入 `OH-004` 确认维护仍是唯一剩余流，再进入 `OH-017`。
3. 依次运行 package health、memory freshness、skill surface 三段审计，得到一组可分类的 findings。
4. 把 findings 分成两类：
   - 可以在 `OH-017` 里直接落地的 bounded cleanup。
   - 会引入新协议、新模板或新命令的扩展性工作。
5. 对第一类 findings，直接在 `OH-017` 中实现并把证据写回 `04-verification.md`、`05-evidence.md`，必要时更新 `.project-memory/` 或 live docs/tests。
6. 对第二类 findings，先回写 `OH-017` 的结论，再脚手架新的 child package。
7. 只有当维护流的剩余边界发生变化时，才回写 `OH-004`。

## Trade-offs
我考虑了三种方案：

- 方案一：继续把维护流留在 `OH-004` 父包里，只在路线图层面记录后续清理事项。
  - 代价是实现细节会再次回流到父包，破坏 `OH-004` 作为 umbrella roadmap 的边界。
- 方案二：现在就直接做一个 `maintenance` 总命令，把 task package、memory、skill drift 都收进去。
  - 这会过早锁定接口，尤其是在仓库还没有验证哪条维护路径最常出现、最值得产品化之前。
- 方案三：先拆 `OH-017`，复用现有审计能力，等第一波维护真实跑过几轮后再决定是否需要总命令。
  - 这是推荐方案。它的代价是短期仍有多条命令，但好处是可以先根据真实 findings 收敛维护面，而不是先发明抽象。

## Overview Reflection
- 我先挑战了“是否根本不需要新包，只要继续维护 `OH-004`”。结论是否定的，因为 `OH-004` 的职责是父级路线图，而不是承载新的维护实施细节。
- 我再挑战了“是否应该立刻产品化维护命令”。当前证据不足以支持这一点，因为现有 `check_stale.py` 与 `audit_memory.py` 已经给出了清晰的第一波问题，先跑真实清理比先造抽象更稳妥。
- 我检查了这个设计是否重复了 `project-memory` skill 或 taxonomy package 的职责。没有；`OH-017` 只定义维护轮次如何消费这些既有能力，不重写它们的基线协议。
- 我还检查了验证面是否过弱。当前设计已经把 `check-tasks`、`bootstrap`、memory audit 和 `pytest` 串成一个明确验证路径，因此不再只是“未来再说”的维护意图。
- 本轮没有使用有边界的子智能体讨论，因为主要不确定性来自仓库内部优先级与拆包边界，现有本地证据已经足够。
