# 需求

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **使用前先确认你能回答这些问题**：
> - 为什么现在要做这件事，而不是以后再做？
> - 当前痛点、缺口、冲突或风险具体是什么？
> - 本轮必须交付哪些结果？这些结果的验收标准是什么？
> - 本轮明确不做什么？哪个 counterexample 看起来相似，但仍然不属于这个任务包？
> - 目标用户是谁？核心场景是什么？单一成功指标是什么？
> - 本轮允许付出的 cost cap 是什么？
> - 有哪些不能违反的约束？
>
> **写法建议**：先写问题陈述（当前到底哪里痛），再写必须交付的结果（准备交付什么），不要倒过来。模板里的每个标题都是必答题。如果你写完后仍然无法解释"为什么不是另一个问题包"，说明需求还没收敛。

## 目标
修复 `openharness update` 在错误目录执行 `git pull` 的问题，让它定位到 OpenHarness 工具安装来源 clone，而不是安装包内的 `openharness_cli/` 目录，也不是当前被 harness 管理的业务项目目录。

单一成功指标：通过 `openharness --repo <project> update` 触发更新时，`git pull` 和 `uv tool upgrade --reinstall openharness` 都以 OpenHarness 安装来源 clone 作为工作目录；`--repo <project>` 不改变 update 的源码更新目标。

## 问题陈述
当前 `update` 命令用 `Path(__file__).resolve().parents[1]` 推导仓库根目录。全局安装后，`__file__` 指向安装环境里的 `openharness_cli/commands/update.py`，推导结果可能是包目录而不是 OpenHarness clone 根目录，导致 `git pull` 报 `fatal: not a git repository`。

目标用户是维护 OpenHarness 安装并使用全局 `openharness` 的开发者。核心场景是在任意业务项目中运行 `openharness update`，仍然更新 OpenHarness 自身源码 clone 和重新安装 CLI。现在先修复是因为全局 CLI 无法自更新会阻断后续使用。

## 必须交付的结果
1. `update` 命令优先使用已安装包元数据 `direct_url.json` 中记录的 OpenHarness 安装来源路径。
   - 验收标准：editable 安装来源存在时，`git pull`、`git fetch`、`git reset --hard @{u}`、`uv tool upgrade --reinstall openharness` 的 `cwd` 都来自该来源路径。
2. 本地源码运行时保留可靠回退路径。
   - 验收标准：没有安装元数据时，从 `openharness_cli/commands/update.py` 向上找到包含 `.git` 和 `pyproject.toml` 的 OpenHarness 仓库根。
3. 增加回归测试覆盖 `--repo` 指定业务项目时的 update 行为。
   - 验收标准：测试不执行真实 `git` 或 `uv`，但能断言所有 subprocess 调用使用 OpenHarness source root，而不是 `--repo` 指定的 project root。

## 非目标
- 不重写 `update` 的更新策略、远端分支选择或冲突处理。
- 不改变 `--force-sync`、`--mode`、`--set-default-mode` 的命令语义。
- 不在本轮处理全局已安装旧版本的部署刷新；代码修复完成后可手动运行 `uv tool upgrade --reinstall openharness`。

Counterexample：让 `update` 使用 `HarnessConfig.repo_root` 看起来能修复在 OpenHarness 仓库里运行的场景，但会把任意业务项目误当成更新目标，不属于正确修复。

## 约束
- 保持 `openharness update` 的现有参数和输出语义。
- `HarnessContext` / `HarnessConfig` 表示当前被 harness 管理的项目，不作为 `update` 的 OpenHarness 安装来源。
- 测试必须避免真实执行 `git pull`、`git reset` 或 `uv tool upgrade`。
- cost cap：只修复 repo root 定位和直接测试，不扩展更新命令功能。
