# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮只覆盖两个仓库表面：

- `README.md` 中的 Codex 安装引导。
- `INSTALL.codex.md` 中给 Agent 执行的安装步骤。

不覆盖自动安装脚本、技能发现实现或仓库结构调整。

## Proposed Structure
推荐方案是直接改文档主路径，不新增脚本：

1. `README.md` 继续把 `INSTALL.codex.md` 作为安装入口。
2. `INSTALL.codex.md` 在最前面明确要求 Agent 先询问用户目标目录。
3. 所有安装、校验、更新、卸载命令都改成 `<target dir>` 占位符形式。
4. `README.md` 的手动安装示例同步改成基于 `<target dir>` 的命令。

## Key Flows
主流程如下：

1. 用户让 Codex 抓取并遵循 `INSTALL.codex.md`。
2. Agent 先询问用户想把 OpenHarness 安装到哪个目标目录。
3. Agent 将仓库克隆到 `<target dir>/openharness`。
4. Agent 将技能链接建立到 `<target dir>/.agents/skills/openharness`。
5. 用户重启 Codex 后从该目标目录发现技能。

## Stage Gates
- 关键约束：不新增安装脚本。
- 边界决定：只修改 `README.md`、`INSTALL.codex.md` 与任务包。
- 关键失败模式：README 与 INSTALL 表述不一致，或者仍残留默认 `~` 路径。
- 降级方向：如果无法脚本化强制执行，至少要让 INSTALL 文档把“先询问目录”写成主路径约束。

## Trade-offs
这个方案的收益是范围小、变更集中、不会新增维护负担。代价是安装行为仍依赖 Agent 遵循文档，而不是由脚本硬性约束。

另一个可行方向是增加安装脚本并由脚本接收目录参数。这个方向更强，但明显超出本轮文档修订的范围，因此不选。

## Overview Reflection
我反思过是否应该顺手引入安装脚本来彻底避免执行偏差。结论是不应该在本轮扩大范围，因为用户首先要改的是 INSTALL 描述与 Agent 主路径行为。验证影响也很明确：只要 README 与 INSTALL 都不再把 `~` 写成默认路径，并都强调先询问目标目录，就能覆盖这次改动的主要风险。
