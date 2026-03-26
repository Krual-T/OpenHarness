# Requirements

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## Goal
让 OpenHarness 的当前协议入口稳定收敛到 `openharness <cmd>`，并在 skills 中明确运行约束：默认在项目根目录运行，如果不在根目录，就显式传 `--repo <项目根目录>`。

## Problem Statement
- 现在虽然已经支持全局命令 `openharness`，但仓库内仍存在一部分活跃协议文档和示例混用旧脚本路径命令，用户很容易继续照抄 `uv run python .../openharness.py ...`。
- 当前 CLI 的 `--repo` 默认值就是当前目录。这个行为本身可以接受，但如果协议文档不说明“默认在项目根目录执行”，用户会误以为工具会自动帮他找根目录。
- 这轮目标不是改 CLI 行为，而是把 skills 和协议说明写清楚，避免入口混乱。

## Required Outcomes
1. 活跃协议文档应统一使用 `openharness <cmd>` 作为标准调用方式，不再在这些说明里出现 `skills/using-openharness/...` 脚本路径命令。
2. skills 需要明确说明：`openharness` 默认应在项目根目录执行；如果当前不在根目录，改用 `--repo <项目根目录>`，而不是改走脚本路径。
3. 帮助文案与协议文档要避免暗示 CLI 已经支持自动向上发现根目录，因为当前实现并没有这么做。
4. 成功标准（single success metric）：维护者只需要记住一套入口，即 `openharness <cmd>`，而不是同时记忆命令名和脚本路径。

## Non-Goals
- 不批量重写历史归档任务包中的旧命令证据；归档材料保留其历史真实性。
- 不把 OpenHarness 改造成原生编译型二进制程序。
- 不移除 `skills/using-openharness/scripts/openharness.py` 兼容入口，但也不再把它作为协议文档里的推荐入口。
- 不要求用户修改任意业务仓库的 `pyproject.toml`。
- 不实现自动向上发现项目根目录，也不实现“必须在根目录”这一类新的硬性校验逻辑。

## Constraints
- 仓库协议要求先更新 task package，再实施文档改动，并在完成后补齐验证与证据。
- 现有 CLI 已经暴露 `--repo` 参数，因此 skills 里的约束要基于现有行为表达，不能虚构新的自动发现语义。
- 需要兼容两类仓库布局：直接包含 `skills/using-openharness/...` 的仓库，以及通过 `.agents/skills/openharness/...` 接入 skill hub 的仓库。
- 反例（counterexample）：如果用户在业务仓库子目录直接执行 `openharness bootstrap`，当前实现不会自动回溯到项目根目录；文档必须避免让用户误解这一点。
