# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮只覆盖 OpenHarness 的 live capability surface：

- `README.md` 中的产品定位、工作流叙述与能力总览。
- `skills/brainstorming/SKILL.md` 中对视觉辅助、需求脑暴和方法论检查项的定义。
- `skills/exploring-solution-space/SKILL.md` 中对总体设计、详细设计、反思与多智能体讨论的检查项定义。
- `skills/using-openharness/references/skill-hub.md` 中对核心能力和可选辅助的分层表述。
- `skills/using-openharness/tests/test_openharness.py` 中对上述文案与协议的固定测试。

不纳入本轮的部分：

- 新增浏览器 helper、runtime helper 或安装脚本。
- 新增 product/CEO 专用技能。
- 改写 `AGENTS.md` 中已经成立的仓库协议。

## Proposed Structure
推荐方案是“核心能力前置，视觉辅助降级”为一个明确的四层结构：

1. 核心认知工作流
   - 由 README 和 skill hub 统一表述为 OpenHarness 的核心卖点。
   - 包括需求脑暴、探索、总体设计、详细设计、测试与评审、验证闭环。
2. 方法论检查项
   - 在 `brainstorming` 中加入产品价值、用户问题、业务影响等思考维度。
   - 在 `exploring-solution-space` 中把这些维度延伸到架构选择、边界划分、测试策略和反思环节。
3. 多智能体协作能力
   - 继续以 bounded subagent discussion、review loops、subagent-driven execution 等形式出现。
   - 强调它们服务于脑暴、设计和测试，而不是作为孤立的“并行能力”被宣传。
4. 可选视觉辅助
   - 浏览器 companion 继续存在，但明确属于按需工具。
   - 其职责是“帮助看图”，不是“定义产品核心”。

这样处理后，后端项目首先看到的是通用方法论能力；前端或视觉问题较多的项目，则仍然能在需要时使用 companion。

## Key Flows
主信息流如下：

1. 用户或维护者从 README 认识产品时，先接触核心能力模型，再看到视觉辅助只是可选补充。
2. 代理进入仓库后，仍然从 `using-openharness` 路由到 `brainstorming`、`exploring-solution-space`、实现和验证，不改变主协议。
3. 在 `brainstorming` 中，代理默认通过文本完成需求收敛；只有问题本身是视觉性的，才会单独 offer visual companion。
4. 在 `exploring-solution-space` 中，代理不仅比较技术方案，还要显式检查用户价值、业务影响、过度设计风险、测试与验证边界。
5. 在测试与实现环节，review loops 和 bounded subagent discussion 共同承担“挑战假设、发现遗漏、从不同角度校验方案”的职责。

状态流保持不变：task package 仍然按 requirements -> overview -> detailed -> implementation -> verification -> archive 推进。

## Trade-offs
收益：

- 产品信息更贴近真实价值，不会让非前端项目误判 OpenHarness 的适用性。
- 现有 reflection 与 multi-agent 能力得到统一命名和前置表达，而不是散落在不同技能里等待读者自己拼出来。
- 不需要发明新的技能层，就能把“产品视角/CEO 视角”转化成稳定的方法论检查项。

代价：

- README、skill hub 和技能文档会变长一点，测试也要相应增强。
- “浏览器 companion 很酷”这类显眼点会被刻意压低，产品展示会更克制。

为什么不选其他方向：

- 不选“完全移除浏览器能力”，因为视觉场景仍然真实存在，而且 companion 已经被设计成按需工具。
- 不选“新增 product/CEO 独立技能”，因为这会把方法论变成角色扮演，增加协议复杂度，却不一定提升落地质量。
- 不选“只改 README 不改技能”，因为那样 live surface 会再次失配，测试也无法保护真正的能力边界。

## Overview Reflection
我主要挑战了三个备选方向。

第一个方向是简单降噪，只在 `brainstorming` 里补一句“浏览器是可选的”。这个做法太弱，因为用户真正指出的是产品重心，而不是一句提示语。

第二个方向是新增一组 product/CEO/reviewer 技能，把不同视角分别建模。这个做法太重，会把原本应该内化到设计检查项里的思考方式，变成更多技能入口和更多维护负担。

最终保留的方向是把这些视角写进现有核心技能的检查项和 README 的产品叙事里。这样既能明确“方法论优先”，又不破坏当前简洁的协议结构。

验证影响也比较清楚：这轮不是靠运行时证据成立，而是靠文档、技能文案和测试断言同时收敛。如果只有文档改了而测试没跟上，这个能力模型很快还会漂回去。
