# 需求

## 背景

`openharness update` 会在安装来源目录中同步 GitHub 代码，然后执行 `uv tool upgrade --reinstall openharness` 刷新本机工具。用户刚遇到的失败是 `git pull` 因 GitHub TLS 握手中断而失败，CLI 只输出一行笼统错误，缺少失败详情，也没有自动重试。

## 问题陈述

OpenHarness 使用者在本机运行 `openharness update` 时，如果网络抖动、TLS 握手中断或远端短暂不可用，当前命令会立即失败。用户只能看到“git pull failed”，不知道失败发生在哪次尝试、具体 stdout/stderr 是什么，也无法判断是否值得重试。

这会让更新问题难以诊断，尤其是独立源码目录和当前项目目录分离时，用户不容易知道实际失败的命令和目录。

## 目标

完成后，`openharness update` 在同步源码失败时应当：

1. 自动重试同步命令，最多尝试 3 次。
2. 每次失败都显示命令、尝试次数、退出码、stdout 和 stderr 摘要。
3. 3 次全部失败后，明确拒绝继续执行工具升级。
4. `pull` 和 `force-sync` 两种同步模式都使用同一套失败报告和重试机制。

## 交付物

1. 更新 `openharness_cli/commands/update.py`，为源码同步命令增加最多 3 次重试和失败详情输出。
2. 更新测试，覆盖前两次失败第三次成功、三次失败后退出、`force-sync` 同步命令也使用重试。
3. 保持工具升级命令 `uv tool upgrade --reinstall openharness` 不做重复重试；本轮只修复“同步 GitHub 代码”的失败报告和重试。

## 非目标

本轮不在 `openharness update` 中自动启用代理，也不改变远端地址、安装来源解析或更新模式配置。例如，把 git 命令自动包装成 `proxy git pull` 不属于本任务。

本轮也不在当前项目目录运行 `openharness update` 来更新当前仓库。

## 约束

1. 重试次数固定为 3 次，不新增配置项。
2. 错误输出要足够诊断，但避免无限量打印超长 stdout/stderr；可以做摘要截断。
3. 保持现有 CLI 成功路径输出兼容。
4. 提交前需要按仓库要求递增 `pyproject.toml` 版本号。

## 自检

- [x] 不了解本轮对话的人能理解问题来自 `openharness update` 同步失败不可诊断。
- [x] 目标和交付物能通过测试判断完成。
- [x] 非目标排除了自动代理和当前项目目录自更新。
- [x] 约束写明重试次数、输出边界和版本要求。
