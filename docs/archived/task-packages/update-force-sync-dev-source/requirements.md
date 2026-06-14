# 需求

## 背景

`openharness update` 用来更新已安装的 OpenHarness 源码目录，并重新安装全局 CLI。刚完成的上一轮修复已经让源码同步失败能显示 stdout/stderr，并自动重试 3 次。

现在还剩一个更根本的问题：默认更新路径仍然是 `git pull`。`git pull` 适合人工在开发工作区里合并代码，但不适合作为工具自更新的默认策略，因为它可能被本地改动、merge 冲突、upstream 配置和分支状态影响。OpenHarness 的安装源码目录更像工具托管缓存，默认应当稳定同步到远端分支。

## 问题陈述

普通 OpenHarness 使用者运行 `openharness update` 时，期望得到一个可重复、可诊断的更新过程，而不是进入 Git 合并语义。当前默认 `git pull` 会把工具更新和开发工作区协作混在一起：一旦安装源码目录里有本地改动或 merge 风险，更新流程就不稳定。

另一方面，OpenHarness 仓库开发者确实需要一种本地开发安装路径：他们可能正在修改源码，希望跳过任何 git 同步，只把当前来源目录重新安装到全局工具里。这个场景不应该继续借用默认 `pull` 模式表达。

## 目标

完成后，以下事实成立：

1. 无参数 `openharness update` 默认执行强制同步：`git fetch --prune` 后 `git reset --hard @{u}`，再执行 `uv tool upgrade --reinstall openharness`。
2. 新增 `dev-source` 更新模式，用于开发者本地源码安装：跳过 git 同步，直接 reinstall 当前已安装来源目录。
3. `--force-sync` 仍可作为显式强制同步入口；`--mode dev-source` 和保存默认模式都能使用 `dev-source`。
4. 依赖缺失时的轻量兜底入口也遵守新的默认强制同步，并支持 `dev-source`。

## 交付物

1. 更新 `openharness_cli/commands/update.py`：默认模式改为强制同步，新增 `dev-source` 模式，模式解析、默认配置和错误提示都能识别 `dev-source`。
2. 更新 `openharness_cli/main.py`：依赖缺失兜底入口默认执行强制同步，并能识别 `--dev-source` 或 `--mode dev-source`。
3. 更新安装文档和 CLI 参考说明，让用户知道默认更新会丢弃安装源码目录里的本地改动，开发者应使用 `dev-source`。
4. 更新测试，覆盖默认强制同步、`dev-source` 跳过 git 同步、保存默认 `dev-source`、兜底入口默认强制同步和兜底 `dev-source`。
5. 按仓库规则提升版本号。由于默认更新行为从非破坏性的 `pull` 改为会丢弃安装源码目录本地改动的强制同步，本轮按不兼容变更处理。

## 非目标

本轮不引入 release/tag 更新机制，也不自动选择最新 GitHub Release。看起来也能提高稳定性，但那是另一套发布渠道设计。

本轮不添加代理自动探测，不改变源码目录定位规则，也不设计“从任意路径安装”的新参数。`dev-source` 只表示“使用当前已安装来源目录，跳过 git 同步”。

## 约束

1. 同步命令仍沿用现有最多 3 次重试和失败详情输出。
2. 强制同步使用 upstream 引用 `@{u}`，不在本轮新增分支选择配置。
3. `uv tool upgrade --reinstall openharness` 仍不自动重试。
4. 不在当前项目目录执行真实 `openharness update`。

## 自检

提交前确认：

- [x] 不了解本轮对话的人，读完「背景」和「问题陈述」，能知道当前要把默认更新从 `pull` 改成强制同步，并给开发者增加 `dev-source`。
- [x] 「目标」和「交付物」能通过 CLI 行为和测试判断完成。
- [x] 「非目标」排除了 release/tag 更新、代理探测和任意路径安装。
- [x] 「约束」写清了重试机制、upstream 引用、reinstall 不重试和不运行真实自更新。
