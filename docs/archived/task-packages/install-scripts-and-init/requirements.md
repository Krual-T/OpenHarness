# 需求

## 目标

为 OpenHarness 提供一键安装体验：用户执行安装脚本完成全局安装，再通过 `openharness init --agent` 完成项目级配置后，对应的 AI 编码助手（Codex 或 Claude Code）能在会话启动时自动加载 OpenHarness 技能。

单一成功指标：用户在新项目中从零到"会话启动自动加载 using-openharness"不超过两条命令。

## 问题陈述

当前矛盾：只有一份 `INSTALL.codex.md` 供人工阅读执行，没有可执行脚本。用户需要手动创建 symlink、手动配置 hook，步骤分散且容易出错。Claude Code 平台完全缺少安装方案。

目标用户：使用 Codex 或 Claude Code 的开发者，他们需要在项目中接入 OpenHarness 的任务包协作协议。

核心场景：开发者在项目根目录运行安装脚本 → 全局依赖就绪 → 项目级配置自动完成 → 下次会话启动时技能自动加载。

## 必须交付的结果

1. **install-codex.sh**：可执行脚本，完成 clone/pull + CLI 安装 + `openharness init --agent codex`
2. **install-claude.sh**：可执行脚本，完成 clone/pull + CLI 安装 + `openharness init --agent claude`
3. **openharness init --agent 命令**：接受 `claude`/`codex`/`all` 参数
   - 创建对应平台的 skill symlink
   - Claude Code 平台配置 SessionStart hook
   - 按规则桥接 AGENTS.md ↔ CLAUDE.md
4. **幂等性**：安装脚本和 init 命令可安全重复执行

## 非目标

- 不创建 Windows 专用的 PowerShell 安装脚本
- 不包含 RWP 的配置
- 不修改现有工作流引擎（transition、gate 逻辑不变）
- 不自动生成 AGENTS.md 内容——只做已有文件间的桥接

## 约束

- 全局 clone 固定在 `~/.agents/skill-hub/openharness`，不提供自定义路径
- SessionStart hook 使用 `"using-openharness"` 字符串格式
- 已存在的 AGENTS.md 或 CLAUDE.md 不会被覆盖——只在不冲突时创建 symlink
- 安装脚本依赖 git 和 uv 已预先安装
