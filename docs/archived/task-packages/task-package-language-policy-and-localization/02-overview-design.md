# Overview Design

## System Boundary
本包负责定义并落地 task package 的第一阶段语言策略。它会更新会影响未来 task package 编写行为的协议表面与模板，但不会尝试整仓翻译，也不会在本轮修改校验器去接受中文章节标题。

## Proposed Structure
采用分层语言策略，而不是一句“全仓库都中文”或“全部继续英文”的笼统规则。

### Layer 1: Human narrative content becomes Chinese-first
下面这些表面应该默认改成中文正文，因为它们主要承载目标说明、设计解释、验证结论和证据解读，本质上是给维护者读的：

- `docs/task-packages/*/*.md`
- `docs/archived/task-packages/*/*.md`
- 与 task package 写法直接相关的仓库协议说明和模板引导文字

在这一层里，段落、说明性列表、需求描述、取舍分析、验证备注和 follow-up 推理都应优先使用中文。

### Layer 2: Protocol-stable structure remains English
下面这些元素继续保留英文，因为它们要么是协议标识，要么是机器校验锚点，要么直接就是命令与路径表面：

- status values such as `proposed`, `detailed_ready`, `archived`
- YAML keys and field names
- CLI commands
- file names
- path names
- 当前被校验器依赖的章节标题，至少在第一阶段保持英文

### Layer 3: Section-title localization is a second-phase decision
仓库不应在这一轮直接把 task package 的章节标题翻成中文，因为当前校验器把下面这些英文标题硬编码成了语义锚点：

- `## Goal`
- `## Problem Statement`
- `## Proposed Structure`
- `## Runtime Verification Plan`

因此，第一阶段应该是：

- keep section titles in English
- translate the content under those titles into Chinese
- keep commands and identifiers in English

如果第一阶段完成后仍然希望把标题也本地化，后续实现包再在下面几个选项里做选择：

1. `dual-title support`
   - validator accepts either English or Chinese canonical titles
2. `Chinese-title migration`
   - validator, templates, and tests move to Chinese titles
3. `English-title permanent`
   - titles stay English permanently while body content is Chinese-first

第一阶段的推荐决策是 `English-title permanent for phase one`。它能以最小协议震荡，立刻拿到大部分可读性收益。

## Key Flows
1. 维护者打开 task package，主要阅读目标、设计、验证和证据正文。
2. 仓库按统一语言策略书写这些正文，而不是每个包自行决定怎么混写。
3. 新建或后续更新的 task package 使用中文叙述正文。
4. 章节标题、命令、状态值、YAML 键名、文件名和路径继续保持英文。
5. 如果后续确实要做中文标题迁移，再单独开实现包，一次性改模板、校验器和测试。

## Trade-offs
- task package 正文改成中文后，维护者阅读成本会立刻下降，但仓库必须更明确地区分“正文”与“协议结构”。
- 第一阶段保留英文标题并不算最纯粹的本地化方案，但它能避免改动校验器，风险明显更低。
- 如果做全量本地化，文档表面会更一致，但必须连带修改模板、测试和 `check-tasks`。
- 如果什么都不改，协议最稳定，但仓库最常用的事实载体仍然会持续对维护者不友好。

## Overview Reflection
- 我先挑战了“全部直接改成中文”的路径。它表述最简单，但会立刻撞上校验器假设和协议标识稳定性的问题。
- 我也考虑过“task package 继续英文，只把助手回复改成中文”。这解决不了根因，因为维护者仍然要直接读仓库里的 task package。
- 我检查了第一阶段是否应该把整个 skill 体系也翻成中文。结论是不应该；真正高频、收益最高的目标是 task package 及其写作协议。
- 我也挑战了“英文标题 + 中文正文”会不会过于混杂。它确实不是最美观的方案，但它是明确、受控、低风险的折中，而不是无序漂移。
