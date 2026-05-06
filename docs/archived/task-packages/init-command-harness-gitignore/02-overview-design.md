# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
本轮覆盖 `openharness_cli` 的子命令注册、命令实现、主模块包装和 CLI 测试。它不覆盖未来 `init` 的完整初始化清单，也不改变已有 task package、RWP 或 project-memory 命令的行为。

## Proposed Structure
推荐方案是在现有 argparse 架构中增加一个 `init` 子命令。`cli.py` 负责注册参数和 handler，`commands.py` 负责副作用：解析 `--repo`、创建 `.harness`、写入 `.harness/.gitignore`。`main.py` 继续承担测试可 monkeypatch 的薄包装层。

## Key Flows
主流程是 `openharness init --repo <repo>` 解析参数，handler 将 repo 解析为绝对路径，创建 `.harness` 目录，写入 `.gitignore` 为 `*\n`，然后打印路径并返回 `0`。失败信号主要来自文件系统异常，按现有简单命令风格让异常直接暴露给调用方和测试。

## Stage Gates
进入详细设计前必须明确：命令名称为 `init`，支持 `--repo`，生成文件为 `.harness/.gitignore`，内容为 `*\n`，本轮不生成其他初始化文件。

## Trade-offs
直接写 `.harness/.gitignore` 的收益是最小、可测、符合当前第一步要求。备选方案是先做完整 init 配置系统，但会把未来初始化项、幂等策略和交互设计提前绑定，超出本轮成本上限。

## Recommended Diagrams
不需要图；这轮只有一个 CLI 到文件系统的线性流程。

## Overview Reflection
已挑战“是否一次性做完整初始化”这一备选方案，结论是拒绝，因为用户明确说“第一步先让 `.harness/` 加上一个 `.gitignore`”。已接受覆盖写入 `*\n` 的简单策略，后续如需保留用户自定义内容再单独设计。
