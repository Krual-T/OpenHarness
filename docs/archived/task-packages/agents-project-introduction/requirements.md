# 需求

## 背景

`AGENTS.md` 已经改为仓库协作入口，但开头缺少对 OpenHarness 项目本身的简短说明。新进入仓库的协作者需要先知道：这个项目是什么、主要由哪些部分组成、当前仓库源码和环境中直接注入的 `using-openharness` 技能有什么区别。

用户明确指出：环境中直接注入的是系统安装的 OpenHarness，通常版本落后于当前项目；如果要更新系统安装版本，不能在本仓库目录使用 `openharness update`，必须在其他目录执行。

## 问题陈述

协作者打开 `AGENTS.md` 后，如果只看到协作入口规则，仍可能混淆“当前仓库正在开发的 OpenHarness 源码”和“环境里已经注入、正在驱动本次协作的 `using-openharness`”。这种混淆会导致错误更新路径，例如在 OpenHarness 源码仓库内运行 `openharness update`，让系统安装版本和当前开发目录关系变得不清楚。

## 目标

完成后应成立以下事实：

- `AGENTS.md` 开头说明 OpenHarness 是面向智能体协作的仓库脚手架和工作流工具。
- `AGENTS.md` 说明项目主要组成：核心库、CLI、技能、文档和测试。
- `AGENTS.md` 明确区分当前仓库源码和环境注入的 `using-openharness`。
- `AGENTS.md` 明确系统安装版本通常落后于当前项目，更新系统安装版本时不能在本仓库目录运行 `openharness update`，必须切到其他目录。

## 交付物

- 在 `AGENTS.md` 开头新增项目介绍。
- 更新 `pyproject.toml` 和 `uv.lock` 的项目版本号。
- 记录本轮任务包证据并提交。

## 非目标

- 不修改 OpenHarness CLI 行为。
- 不修改安装脚本或 README。
- 不改变 `using-openharness` 技能内容。

## 约束

- 文案保持简短，放在入口文件开头，不把 `AGENTS.md` 重新变成完整仓库百科。
- 继续使用通俗中文；命令、路径和技能名保持英文。
