# 安装和项目配置地图

## 目录作用

- `install.sh`：Linux 和 macOS 安装脚本；修改类 Unix 安装、升级或链接行为时进入。
- `install.ps1`：Windows PowerShell 安装脚本；修改 Windows 安装、升级或链接行为时进入。
- `pyproject.toml`：Python 项目配置、依赖声明、命令入口和版本号；修改依赖、打包入口、测试配置或提交前版本号时进入。
- `uv.lock`：uv 依赖锁定文件；修改依赖或同步项目版本号后检查这里。
