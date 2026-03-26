# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
让 OpenHarness CLI 的帮助输出具备“可自解释性”，用户只看 `--help` 就能理解命令用途、关键行为和典型用法。

## Problem Statement
当前帮助输出存在两个问题：

- 顶层 `openharness --help` 还可以，但各个子命令的 `--help` 普遍只剩参数列表。
- 像 `update` 这种副作用较强的命令，没有在帮助页里解释它究竟更新什么、按什么顺序执行。

这会让用户误以为“帮助没坏，只是没内容”，但实际上帮助系统没有履行说明职责。

## Required Outcomes
1. 顶层帮助页保留并强化子命令总览。
2. `bootstrap`、`check-tasks`、`new-task`、`transition`、`verify`、`update` 的帮助页都要出现说明性文本。
3. `update --help` 必须明确它会更新 OpenHarness clone 并刷新已安装 CLI。
4. 自动化测试断言帮助文本的关键片段，防止之后再次退化成空壳。

## Non-Goals
- 不实现 shell 级自动补全。
- 不引入交互式帮助浏览器。
- 不在本轮重做整个 CLI 参数结构。

## Constraints
- 保持现有子命令和参数兼容。
- 优先通过 `argparse` 原生能力补文案，不引入新的 CLI 框架。
- 帮助文本要简洁，但必须有信息密度，不能只有 `-h, --help`。
