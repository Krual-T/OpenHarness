# 验证策略

> 章节标题使用中文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。
>
> **本文件在 `verification_designing` 阶段编写（TDD 红阶段，先于实现）**。
> 定义验证策略——计划怎么验证、用什么命令、期望什么结果。
> 实际验证执行和证据在 `verifying` 阶段写入 `evidence.md`。
>
> **使用前先确认你能回答这些问题**：
> - 每项 Required Outcome 是否有对应的验证方法？
> - 验证命令是否具体到可以直接复制粘贴执行？
> - 是否有边界或错误场景的验证？
> - 哪些风险本轮不覆盖，接受理由是什么？
> - 计划路径和回退路径分别是什么？

## 验证路径
- **计划路径**：新增单元测试，用 `CliRunner` 调用 `openharness --repo <project> update`，monkeypatch `subprocess.run` 和安装元数据解析，断言 `git pull` 和 `uv tool upgrade --reinstall openharness` 的 `cwd` 都等于 OpenHarness source root，而不是 `<project>`。
- **回退路径**：如果测试无法稳定拦截 subprocess，改为抽出一个内部函数解析 repo root 并直接单测；不执行真实 `git` 或 `uv`。
- **路径说明**：这个 bug 是可编程的 cwd 选择错误，unit_test 足够覆盖；不需要实际访问网络或远端 git。

## 必需命令
| 命令 | 期望退出码 | 期望输出 |
|------|------------|----------|
| `uv run pytest tests/openharness_cases/test_cli_workflows.py -k 'update_uses_installed_openharness_source_root or openharness_source_root_falls_back_to_module_repo'` | 0 | 新增 update source root 回归测试通过 |
| `uv run pytest tests/openharness_cases/test_cli_workflows.py` | 0 | CLI workflow 测试通过 |
| `uv run pytest` | 0 | 全量测试通过 |

## 预期结果
- `update` 不再使用 `Path(__file__).resolve().parents[1]` 作为 repo root。
- `update` 优先使用 `direct_url.json` 中记录的 OpenHarness 安装来源路径。
- 没有安装元数据时，`update` 从模块路径向上找到 OpenHarness 本地源码仓库根。
- 测试证明 `--repo` 指定的业务项目目录不会传入 update 子进程的 `cwd`。

## 可追溯性
| 需求结果 | 验证方法 | 证据位置 |
|----------|----------|----------|
| 使用 OpenHarness 安装来源路径 | 代码审查和新增测试 | `openharness_cli/commands/update.py`、测试输出 |
| 本地源码运行可回退到模块所在仓库根 | 直接测试 `_openharness_source_root()` | `tests/openharness_cases/test_cli_workflows.py` |
| `git` 和 `uv` 子进程 cwd 不来自业务项目 `--repo` | monkeypatch `subprocess.run` 记录调用 | `tests/openharness_cases/test_cli_workflows.py` |

## 风险接受
- 不执行真实 `git pull` 或 `uv tool upgrade`。接受理由：真实命令有网络和环境副作用；本轮只验证 cwd 选择。
- 不改变 update 模式语义。接受理由：当前 bug 是 repo root 定位，不是更新策略问题。

## 验证执行计划
实现完成后立即执行必需命令。若新增测试失败，先判断是 cwd 断言失败还是 mock 设置问题；cwd 断言失败回 `implementing` 修复，mock 设置问题留在验证设计内修正测试策略。
