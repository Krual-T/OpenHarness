# 安装 OpenHarness

OpenHarness 支持 Linux、macOS 和 Windows。安装分为两步：

1. 安装全局 `openharness` CLI 工具
2. 在目标项目中运行 `openharness init` 完成项目初始化

## 前置条件

- Git
- [uv](https://docs.astral.sh/uv/)

## Linux / macOS

### 自动安装

```bash
curl -fsSL https://raw.githubusercontent.com/Krual-T/OpenHarness/refs/heads/main/install.sh | bash
```

或者克隆仓库后手动执行：

```bash
git clone https://github.com/Krual-T/OpenHarness.git
cd OpenHarness
bash install.sh
```

`install.sh` 支持 `--branch` 参数指定分支：

```bash
bash install.sh --branch main
```

### 手动安装

如果不使用脚本，也可以逐步手动安装：

```bash
# 克隆仓库
git clone https://github.com/Krual-T/OpenHarness.git ~/.agents/skill-hub/openharness

# 安装全局 CLI
uv tool install --editable ~/.agents/skill-hub/openharness
```

## Windows

### 自动安装（PowerShell）

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Krual-T/OpenHarness/refs/heads/main/install.ps1" | Invoke-Expression
```

或者克隆仓库后手动执行：

```powershell
git clone https://github.com/Krual-T/OpenHarness.git
cd OpenHarness
.\install.ps1
```

`install.ps1` 支持 `-Branch` 参数：

```powershell
.\install.ps1 -Branch main
```

### 手动安装（PowerShell）

```powershell
# 克隆仓库
git clone https://github.com/Krual-T/OpenHarness.git $env:USERPROFILE\.agents\skill-hub\openharness

# 安装全局 CLI
uv tool install --editable $env:USERPROFILE\.agents\skill-hub\openharness
```

## 验证 CLI 安装

```bash
openharness task-package list
```

如果提示命令未找到，重新执行：

```bash
uv tool install --editable ~/.agents/skill-hub/openharness
```

## 项目初始化

告知用户在目标项目根目录下执行：

```bash
openharness init --agent <claude|codex|all>
```

- `--agent claude`：仅初始化 Claude Code 项目
- `--agent codex`：仅初始化 Codex 项目
- `--agent all`（默认）：同时初始化 Claude Code 和 Codex

`openharness init` 会完成以下操作：

1. 创建 `.harness/` 目录
2. 为 Claude Code 创建技能符号链接（`.claude/skills/using-openharness`）和会话启动钩子
3. 为 Codex 创建技能符号链接（`.agents/skills/openharness`）和会话启动钩子
4. 在 `AGENTS.md` 和 `CLAUDE.md` 之间建立桥接（如果只存在其一）

## 更新

```bash
openharness update
```

此命令会强制同步 OpenHarness 安装源码目录并刷新 CLI 工具。技能通过符号链接自动保持最新。

默认同步会执行 `git fetch --prune` 和 `git reset --hard @{u}`，会丢弃安装源码目录中的本地修改。这个目录应视为 OpenHarness 管理的安装缓存，不应作为开发工作区使用。

如果你正在开发 OpenHarness 本仓库，只想把当前源码重新安装到全局工具中，使用开发源码模式：

```bash
openharness update --mode dev-source
```

也可以把开发源码模式设为默认：

```bash
openharness update --set-default-mode dev-source
```

恢复默认强制同步模式：

```bash
openharness update --set-default-mode force-sync
```

## 已有安装补充 CLI

如果之前只安装了技能符号链接而未安装全局 CLI，只需补充一条命令：

```bash
uv tool install --editable ~/.agents/skill-hub/openharness
```

## 卸载

删除项目中的技能符号链接：

```bash
rm <target-dir>/.claude/skills/using-openharness        # Claude Code
rm <target-dir>/.agents/skills/openharness              # Codex
```

移除全局 CLI：

```bash
uv tool uninstall openharness
```

如需删除克隆仓库：`rm -rf ~/.agents/skill-hub/openharness`。

## 归属声明

OpenHarness 复用并改编了 [`obra/superpowers`](https://github.com/obra/superpowers) 的源码。如果你分发本仓库的实质性部分，请保留上游版权和许可声明。
