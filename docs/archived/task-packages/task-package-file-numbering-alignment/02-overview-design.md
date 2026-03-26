# Overview Design

> 章节标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## System Boundary
- 覆盖范围包括协议源、模板、校验器、测试，以及所有 active 与 archived task package 的真实文件和路径引用。
- 不纳入范围的是 task package 章节内容本身的语义重写，以及其他与编号无关的协议演化。

## Proposed Structure
- 新的 canonical 文件集合改为：`README.md`、`STATUS.yaml`、`01-requirements.md`、`02-overview-design.md`、`03-detailed-design.md`、`04-verification.md`、`05-evidence.md`。
- `manifest.yaml` 与模板先切到新编号，再批量重命名仓库里的实际文件。
- `openharness_cli/constants.py`、校验逻辑和测试断言同步切到新编号，确保仓库只存在一套现行协议。

## Key Flows
1. 先让测试和协议源对新编号形成明确断言。
2. 再批量把 task package 中的 `04-verification.md` 重命名为 `04-verification.md`，把 `05-evidence.md` 重命名为 `05-evidence.md`。
3. 批量替换 task package 正文、`STATUS.yaml`、模板、文档和测试中的旧路径引用。
4. 最后用 `openharness check-tasks` 验证整仓没有遗留的现行旧编号。

## Stage Gates
- 必须明确这是一次整仓切换，不保留双编号。
- 必须明确 active 和 archived package 都要跟着改。
- 必须明确测试如何判断新旧编号边界，而不是只看模板。

## Trade-offs
- 收益是协议变得直观，维护者不再看到缺失的 `04-*`。
- 代价是这是一轮大面积路径重命名，需要触达大量历史包和测试。
- 不选“继续保持现状”，因为你已经明确要求切到连续编号。
- 不选“只改模板，旧包不动”，因为这会制造长期双协议。

## Overview Reflection
- 我挑战过“给 `05/06` 起一个正式解释并保留现状”，但这只是在给历史遗留找理由，不是真正收敛。
- 我也挑战过“保留双编号兼容”，但那会让协议长期存在两套现行命名，复杂度反而更高。
- 因此这轮直接选整仓一次性切换，虽然重，但边界最清楚。
