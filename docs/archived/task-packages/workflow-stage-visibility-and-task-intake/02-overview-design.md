# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
覆盖四个仓库表面：

- `skills/using-openharness/scripts/openharness.py` 的任务入口 CLI。
- `skills/using-openharness/SKILL.md` 的入口协议说明。
- `skills/brainstorming/SKILL.md` 的 requirements 收敛与 handoff 规则。
- `skills/using-openharness/tests/test_openharness.py` 以及必要的 README 文字说明。

不纳入范围：

- 不修改 task package 根目录结构。
- 不新增新的 stage。
- 不把 review gate 做成必须人工确认的强制暂停。

## Proposed Structure
采用“脚本可见性 + 技能时机约束”双层方案。

- CLI 层负责把阶段讲清楚：
  - 为每个 status 提供简短阶段说明和推荐下一步。
  - `bootstrap` 文本输出直接展示 `current stage`、`next stage`、`next step`。
  - `bootstrap --json` 提供同样的结构化字段，便于后续 agent 或其他工具直接读取。
- task intake 层负责把建包时机和编号问题收敛掉：
  - `new-task` 新增自动分配 `task_id` 的能力。
  - 自动编号基于现有 task package 的稳定前缀和最大编号递增，避免手工维护。
- skill 层负责把“什么时候建包”和“什么时候告知用户”写成显式协议：
  - `brainstorming` 明确要求：没有 package 时，不在最开始模糊讨论就建包，而是在 brainstorming 完成、准备进入 exploration 前创建。
  - `using-openharness` 明确要求：进入新 stage 时，需要向用户说明当前 stage、刚完成什么、下一步准备做什么。

## Key Flows
主流程一：已有 task package 的阶段可见性

1. agent 进入仓库，运行 `bootstrap`。
2. CLI 除了列出 task package，还输出当前阶段说明、下一合法阶段和建议动作。
3. agent 据此向用户同步“当前在什么阶段，下一步要做什么”，而不是只说“我继续看一下”。

主流程二：没有 task package 的任务 intake

1. agent 先完成 brainstorming，把需求收敛到可以写进 `01-requirements.md` 的程度。
2. 当它准备调用 `exploring-solution-space` 时，如果当前还没有 package，就先调用 `new-task` 建包。
3. `new-task` 可以自动生成下一个 `task_id`，只需要稳定的任务名和标题即可落包。
4. agent 将 requirements 写入新包，再进入 exploration。

## Stage Gates
- 明确阶段可见性的落点在 CLI，而不是只靠聊天习惯。
- 明确自动建包的触发点是“brainstorming 结束、进入下一阶段前”，而不是会话一开始。
- 明确自动编号必须向后兼容老命令写法。
- 明确技能协议至少要覆盖“阶段播报”和“建包时机”这两件事。
- 明确测试会同时覆盖脚本输出与技能文案，避免实现与协议再次漂移。

## Trade-offs
收益：

- 用户可以直接从入口输出理解流程位置，不必手动翻 `STATUS.yaml`。
- 自动建包时机更晚、更稳，能减少一开始就创建空壳 package 的噪音。
- 自动编号消除了最容易阻塞 agent 自主落包的一步。

代价：

- `bootstrap` 输出会比之前更长。
- 技能文案会更具体，意味着后续若要再改流程，需要同时维护测试。

不选的方案：

- 不选“用户一提出任务就立刻建包”，因为很多讨论只是临时方向探索，过早落包会制造大量空包。
- 不选“只改 skill，不改 CLI”，因为用户仍然难以从仓库输出理解阶段。
- 不选“新增一个专门的 stage-status 命令”，因为 `bootstrap` 本来就是入口，把信息放回入口更直接。

## Overview Reflection
我先挑战了最激进的方案：在一开始就自动建包。这个方案虽然最自动，但会把模糊讨论也固化成 task package，噪音太大，因此放弃。

我再挑战了最保守的方案：只补 CLI 说明，不改 skill。这样仍然无法把“脑暴结束后自动建包”变成稳定协议，只能改善一半问题，因此不够。

我也检查了是否需要新增状态来表达“待确认阶段”。这会引入新的协议迁移和更多历史兼容成本，而当前问题的根因更多是可见性和 handoff 时机，不是状态数量不够，所以不新增 stage。

这轮 overview 的结论是：把可见性做在 `bootstrap`，把建包时机做在 `brainstorming` / `using-openharness` 的 handoff 规则，并用自动编号把脚本阻塞点清掉，是最小且成体系的收敛路径。
