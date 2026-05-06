# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
新增 `openharness init` 命令的第一步行为，让用户在仓库里运行命令后得到 `.harness/.gitignore`，且文件内容为 `*`。单一成功指标是：测试仓库中执行命令后，`.harness/.gitignore` 存在并精确忽略 `.harness` 下全部内容。

## Problem Statement
目标用户是维护或接入 OpenHarness 的开发者。核心场景是在一个仓库开始使用 harness 本地运行期目录前，需要一个稳定入口准备 `.harness`，并避免后续生成的运行期文件、trace、artifact 或临时状态被误提交。现在先做 `.gitignore` 是因为这是 `init` 命令最小且低风险的基础能力。

## Required Outcomes
1. CLI 暴露 `openharness init` 子命令，并支持 `--repo` 指向目标仓库。
2. 命令会创建 `.harness` 目录和 `.harness/.gitignore` 文件。
3. `.harness/.gitignore` 内容为 `*\n`；`acceptance criteria` 是测试直接读取文件内容并断言等于该值。
4. 命令成功时返回 `0`，并输出初始化位置，便于用户知道改动落在哪里。

## Non-Goals
- 本轮不初始化 RWP、workspace、artifact、trace 等子目录。
- 本轮不修改仓库根目录 `.gitignore`。
- 本轮不设计完整 `init` 配置交互或模板系统。
- `counterexample`：自动生成 `.harness/rwp/workflows/` 看起来也像初始化，但不属于这一步。

## Constraints
- 仓库内 Python 命令使用 `uv run ...`。
- 实现应沿用现有 argparse CLI 结构，不引入新 CLI 框架。
- `cost cap` 是一个聚焦提交，只改 CLI、测试和本任务包文档。
- `.harness/.gitignore` 的策略必须保持简单明确：忽略全部，即 `*`。
