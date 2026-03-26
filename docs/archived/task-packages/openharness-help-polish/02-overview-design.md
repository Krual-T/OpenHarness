# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖 CLI parser 文案与相关帮助测试，不涉及命令执行语义变化。

## Proposed Structure
继续使用 `argparse`，但为顶层 parser 和各子命令补充：

- `description`
- `epilog`
- 更明确的 `help`
- 适合保留换行的 formatter

这样可以在不改变命令结构的前提下提升帮助可读性。

## Key Flows
用户执行 `openharness <subcommand> --help` 时，帮助页应依次呈现：

1. 命令用途
2. 关键行为或注意事项
3. 参数
4. 最小示例

## Stage Gates
- 明确哪些子命令必须有示例。
- 明确帮助页至少要覆盖命令用途和一个示例。

## Trade-offs
收益是成本低、兼容好、立刻生效。代价是帮助文本仍然是静态文案，不会像专门 CLI 框架那样自动生成更丰富展示。

## Overview Reflection
反思后结论是：当前问题不是 CLI 框架能力不够，而是我们没有把帮助文本当成正式接口维护，因此应先补测试和文案，而不是贸然换框架。
