# 需求

## 目标

`openharness init --agent codex` 在当前项目下创建 `.codex/hooks.json` 和 `.codex/config.toml`，使 Codex 会话启动时自动注入 using-openharness 技能全文。

## 问题陈述

当前 `init --agent codex` 只创建了 symlink，Codex 虽然能发现技能，但采用渐进式加载——只在 description 匹配用户输入时才注入完整内容。需要 SessionStart hook 在会话开头直接输出 SKILL.md 全文。

## 必须交付的结果

1. `init --agent codex` 创建 `.codex/hooks.json`，包含 SessionStart hook
2. 如 `.codex/config.toml` 不存在，创建并写入 `[features]\ncodex_hooks = true`
3. 如 `.codex/config.toml` 已存在但无 `codex_hooks`，打印警告提示手动添加

## 非目标

- 不解析/修改已有 `.codex/config.toml` 的其他内容
- 不引入 TOML 解析依赖

## 约束

- hooks.json 的 `matcher` 使用 `"startup|resume"`，排除 `clear`
- config.toml 仅在不冲突时创建，已存在时只警告不覆盖
