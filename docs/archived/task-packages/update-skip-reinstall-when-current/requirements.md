# 需求

## 背景

`openharness update` 现在默认执行强制同步：先 `git fetch --prune`，再 `git reset --hard @{u}`，最后执行 `uv tool upgrade --reinstall openharness`。上一轮已经把默认模式从 `pull` 改为强制同步，并新增了 `dev-source` 开发者模式。

当前仍有一个体验问题：即使远端没有新提交，默认更新也会继续 reinstall。对于普通用户来说，这会多跑一次没有必要的安装；对于调试更新问题的人来说，也会把“源码是否变化”和“工具是否重装”混在一起。

## 问题陈述

普通 OpenHarness 使用者运行 `openharness update` 时，如果安装源码目录在强制同步前后已经指向同一个 commit，CLI 仍然执行 reinstall。这个行为浪费时间，也让用户无法区分“已经是最新源码”和“确实更新并重装了工具”。

判断是否需要 reinstall 应放在强制同步完成之后，而不是只看 `fetch` 输出。`fetch` 更新的是远端引用，真正决定本地源码是否变化的是 `reset --hard @{u}` 前后的 `HEAD`。

## 目标

完成后，以下事实成立：

1. 默认 `force-sync` 更新会在同步前后比较本地 `HEAD`。
2. 如果同步后 `HEAD` 没有变化，CLI 不执行 `uv tool upgrade --reinstall openharness`，并提示 OpenHarness 已经是最新代码。
3. 如果同步后 `HEAD` 发生变化，CLI 继续执行 reinstall，并输出更新成功信息。
4. `dev-source` 模式不做 git 同步，也不做 HEAD 变化判断，仍然总是 reinstall。
5. 依赖缺失时的轻量兜底入口也遵守同样的跳过 reinstall 规则。

## 交付物

1. 更新 `openharness_cli/commands/update.py`：强制同步前后读取 `git rev-parse HEAD`；只有 `HEAD` 变化时才 reinstall；无变化时提示已经是最新代码。
2. 更新 `openharness_cli/main.py`：兜底入口保持 stdlib 实现，同样通过 `HEAD` 比较决定是否 reinstall。
3. 更新测试：覆盖强制同步无变化跳过 reinstall、强制同步有变化执行 reinstall、`dev-source` 仍执行 reinstall、兜底入口无变化跳过 reinstall。
4. 按仓库规则提升 patch 版本。

## 非目标

本轮不判断 package metadata、已安装 console script 或 `uv tool` 缓存是否和源码一致。即使源码 commit 没变但用户手动破坏了本机安装，本轮默认更新也不会自动 reinstall；这种场景应使用 `openharness update --mode dev-source` 主动重装。

本轮不添加 `--force-reinstall` 参数，也不改变 `dev-source` 的语义。

## 约束

1. 同步命令失败时仍保留最多 3 次重试和 stdout/stderr 报错。
2. HEAD 读取失败应视为更新失败，不能继续 reinstall。
3. 不在当前项目目录执行真实 `openharness update`。
4. `uv tool upgrade --reinstall openharness` 本轮仍不自动重试。

## 自检

提交前确认：

- [x] 不了解本轮对话的人能理解：默认更新如果同步后没有新 commit，就不该 reinstall。
- [x] 目标和交付物能通过 subprocess 调用序列和输出断言判断完成。
- [x] 非目标排除了安装损坏自动修复、`--force-reinstall` 和 `dev-source` 语义变更。
- [x] 约束写清了失败处理、真实自更新限制和 reinstall 不重试。
