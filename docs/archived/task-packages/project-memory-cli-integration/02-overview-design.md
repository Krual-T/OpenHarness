# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
覆盖范围：

- `openharness_cli` 的公共命令面，新增 `project-memory` 子命令树。
- `skills/project-memory/SKILL.md` 的活跃命令示例与使用说明。
- 覆盖 CLI 暴露面和活跃协议文档约束的测试。

不纳入范围：

- `project-memory` 底层对象模型、索引结构和匹配算法。
- 其他 skills 的脚本入口收口。
- 历史归档 task package 中保留的旧命令证据。

## Proposed Structure
推荐方案是在 `openharness_cli` 内新增一层轻量的 project-memory 命令编排，而不是把 `skills/project-memory/scripts/*.py` 的逻辑全部内联复制进 CLI。

边界划分如下：

- `openharness_cli/cli.py`
  负责声明 `project-memory` 一级命令和各个二级子命令的参数面。
- `openharness_cli/commands.py`
  负责把解析后的参数转成稳定的脚本调用，统一处理 `--repo`、子命令选择和参数转发。
- `skills/project-memory/scripts/*.py`
  继续承载实际业务逻辑，作为当前稳定实现面。
- `skills/project-memory/SKILL.md`
  负责把对外推荐入口切到正式 CLI。

关键约束是不要在 CLI 层复制 project-memory 的领域逻辑，否则会形成双份实现和双份维护成本。

## Key Flows
主路径：

1. 维护者执行 `openharness project-memory <subcommand> ...`。
2. CLI 解析一级 `project-memory` 和二级动作，例如 `query`、`save-fact`。
3. `commands.py` 组装对应的 `uv run python skills/project-memory/scripts/<script>.py ... --repo-root <repo>` 调用。
4. 现有脚本继续在目标 repo 根目录下执行，输出文本或 JSON 结果。

关键失败信号：

- parser 不认子命令，说明 CLI 暴露面未接好。
- 参数未正确转发，脚本会报 argparse 错误或行为偏差。
- `--repo` 未传透时，脚本可能在错误目录查找 `.project-memory/` 或 manifest。

兼容性约束会改变主路径的一点是：为了兼容从非项目根目录调用 CLI，包装层必须显式把 repo 路径传给脚本，而不是依赖当前工作目录碰巧正确。

## Stage Gates
- 必须先确定本轮只做 CLI 收口，不重写 project-memory 领域逻辑。
- 必须确定二级子命令覆盖面，避免实现到一半再扩张范围。
- 必须明确失败模式主要在“CLI 暴露和参数转发”，而不是 memory schema。
- 必须明确回退方向：如果包装层实现受阻，宁可保留脚本为底层实现，也不把逻辑硬复制进 CLI。

## Trade-offs
推荐方案的收益是复用现有脚本、改动集中、验证路径清晰，而且能立刻把官方入口统一到 `openharness`。代价是 CLI 仍然依赖 skill 目录里的脚本文件，短期内不是完全独立的产品层。

备选方案一：直接把所有 project-memory 逻辑搬进 `openharness_cli`。
不选原因：改动面太大，会把“统一入口”膨胀成“重写 memory 运行时”，而且容易制造双份实现漂移。

备选方案二：只改 skill 文档，不改 CLI。
不选原因：这只能统一文案，不能统一真实入口，问题会继续存在。

## Overview Reflection
反思后确认的 challenge closure：

- 接受：CLI 层先做轻量包装，短期继续依赖 `skills/project-memory/scripts` 作为稳定实现面。
- 拒绝：把本轮扩大成 project-memory 逻辑重构，因为这会显著增加回归面且偏离用户当前诉求。
- 延期：如果未来需要把更多 helper skills 收口进 CLI，再单独评估是否抽象出通用“脚本桥接层”。
