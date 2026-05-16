# 项目运行时表面地图

> 表格标题保留英文；正文默认使用中文；命令、状态值、YAML 键名、文件名与路径保持英文。

## 使用说明

- 每行对应一个已支持的运行时表面。
- 如果运行时循环已有支撑，将 `Helper Or Bootstrap` 链接到对应的可复用辅助技能。
- 如果表面已记录但尚无辅助工具，先加一个窄辅助，再将临时引导链接替换为辅助路径。
- 如果仓库尚未定义该表面，将 `Helper Or Bootstrap` 链接到一个引导包。
- 将选定的运行时表面抄入 `03-detailed-design.md`，在 `04-verification.md` 中记录执行路径，在 `05-evidence.md` 中列出产物和残余风险。

| Surface | Purpose | Prerequisites | Driver | Evidence | Helper Or Bootstrap |
| --- | --- | --- | --- | --- | --- |
| API | 验证请求/响应行为（需运行中服务） | 本地环境、种子数据、鉴权夹具 | `uv run ...` 或项目 API 驱动 | 响应、trace、日志 | `skills/<项目-api-运行时>/SKILL.md` |
| Browser | 验证真实浏览器中的端到端流程 | 运行中的应用、测试账号 | 浏览器辅助命令或脚本 | 截图、控制台日志、网络 trace | `docs/task-packages/<引导-浏览器-运行时>/README.md` |
| Worker | 验证队列或后台任务行为 | Worker 环境、fixture 输入 | worker 启动器或触发脚本 | 日志、输出记录、指标 | `skills/<项目-worker-运行时>/SKILL.md` |

## 注意事项

- 每个辅助技能只对应一个主要运行时表面。
- 如果某个表面的前提条件、证据或驱动步骤写不清楚，先开一个引导包再考虑复用。
