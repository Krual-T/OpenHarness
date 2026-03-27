# Author Entry

本页是 OpenHarness 面向中文作者的最短入口。

如果你看不懂英文 `SKILL.md`，或者你只想先知道 task package 应该怎么开始写，就先看这里。

## First Step

- 如果你刚进入仓库，先看 `AGENTS.md` 了解仓库地图。
- 然后运行 `openharness bootstrap` 查看当前 active task packages。
- 如果你要新建或补写 task package，不要先硬读所有 skill；先根据你所在阶段找到对应 guidance。

## Which Guidance To Read

- 你还在收敛任务目标、用户、场景、范围：
  - 先看 `requirements-writing-guidance.md`
  - 对应阶段是 `brainstorming`
  - 对应文档是 `01-requirements.md`
- 你已经知道要做什么，正在决定整体结构、边界和主流程：
  - 先看 `overview-design-writing-guidance.md`
  - 对应阶段是 `exploring-solution-space`
  - 对应文档是 `02-overview-design.md`
- 你已经确定总体方向，正在决定验证路径、文件落点、接口、迁移顺序：
  - 先看 `detailed-design-writing-guidance.md`
  - 对应阶段是 `exploring-solution-space`
  - 对应文档是 `03-detailed-design.md`
- 你已经做完实现，准备证明结果是否成立：
  - 先看 `verification-writing-guidance.md`
  - 对应阶段是 `verification-before-completion`
  - 对应文档是 `04-verification.md`
- 你要整理这轮真正改了什么、跑了什么命令、证据放在哪里：
  - 先看 `evidence-writing-guidance.md`
  - 对应阶段是 `verification-before-completion`
  - 对应文档是 `05-evidence.md`

## Fast Path

- 只想快速开始写需求：
  - 打开 `01-requirements.md` 模板
  - 同时对照 `requirements-writing-guidance.md`
- 只想判断“系统边界”“主路径”“Trade-offs”到底该写什么：
  - 打开 `02-overview-design.md` 模板
  - 同时对照 `overview-design-writing-guidance.md`
- 只想判断“验证路径”“文件落点”“接口”“迁移顺序”该写什么：
  - 打开 `03-detailed-design.md` 模板
  - 同时对照 `detailed-design-writing-guidance.md`

## What This Page Does Not Do

- 本页不替代五份 guidance 正文。
- 本页不定义新的 task package 文件。
- 本页不替代 stage skill 的动作指导。

它只负责一件事：把你导向当前最该看的正式说明。
