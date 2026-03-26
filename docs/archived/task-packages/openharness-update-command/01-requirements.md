# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
提供 `openharness update` 命令，让用户不用再记忆 `cd ~/.agents/skill-hub/openharness && git pull` 与 `uv tool upgrade openharness` 这两步手工流程。

## Problem Statement
虽然 OpenHarness 已经提供 `openharness <cmd>`，但更新仍然依赖用户手工切到克隆目录再执行两条命令。这有几个问题：

- 用户需要记住安装源路径，增加心智负担。
- 文档与真实使用路径分裂，日常维护体验仍然不够“即插即用”。
- 如果用户在错误目录执行 `git pull`，容易把更新行为误应用到业务仓库。

## Required Outcomes
1. CLI 增加 `update` 子命令，作为面向用户的统一更新入口。
2. 该命令默认定位到 OpenHarness 自身仓库根，而不是依赖调用时当前目录。
3. 命令成功路径必须先执行 `git pull`，再执行 `uv tool upgrade openharness`。
4. 若 `git pull` 失败，命令必须立刻返回失败，且不得继续执行工具升级。
5. 安装文档与技能文档需要更新为优先推荐 `openharness update`。

## Non-Goals
- 不做通用插件系统或任意仓库的升级器。
- 不在本轮自动处理未提交改动、分支冲突或鉴权失败。
- 不替代首次安装流程；`update` 只覆盖已安装后的更新场景。

## Constraints
- 必须保持现有 CLI 风格和子命令结构一致。
- 命令实现应复用现有运行命令机制，避免单独再造一套 subprocess 包装。
- 测试不能真的执行用户环境中的 `git pull` 或 `uv tool upgrade`，需要通过可控替身验证顺序与参数。
- 信息输出继续遵守仓库中文说明要求，但命令本身保持英文。
