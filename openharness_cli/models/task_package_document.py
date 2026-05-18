
from enum import StrEnum
from pathlib import Path


class TaskPackageDocument(StrEnum):
    TASK_INFO = ("task-info.yaml", True, ())
    REQUIREMENTS = ("requirements.md", False, (
        "## 目标", "## 问题陈述", "## 必须交付的结果", "## 约束",
    ))
    OVERVIEW_DESIGN = ("overview-design.md", False, (
        "## 系统边界", "## 推荐结构", "## 关键流程",
        "## 阶段门禁", "## 取舍", "## 总体设计反思",
    ))
    DETAILED_DESIGN = ("detailed-design.md", False, (
        "## 可观察性与验证准备", "## 新增或修改文件",
        "## 接口", "## 模块内部设计", "## 数据语义",
        "## 决策闭合", "## 错误处理", "## 迁移说明",
        "## 详细设计反思",
    ))
    VERIFICATION_DESIGN = ("verification-design.md", False, (
        "## 验证路径", "## 必需命令", "## 预期结果",
        "## 可追溯性", "## 风险接受",
    ))
    EVIDENCE = ("evidence.md", False, (
        "## 验证结果", "## 文件", "## 残余风险",
    ))

    def __new__(cls, filename: str, is_base: bool, sections: tuple[str, ...]):
        obj = str.__new__(cls, filename)
        obj._value_ = filename
        obj.is_base = is_base
        obj.sections = sections
        return obj

    def path_from(self, root: Path) -> Path:
        return root / self.value

    @classmethod
    def base_files(cls) -> tuple[TaskPackageDocument, ...]:
        return tuple(d for d in cls if d.is_base)

    @classmethod
    def section_specs(cls) -> dict[TaskPackageDocument, tuple[tuple[TaskPackageDocument, str], ...]]:
        return {
            d: tuple((d, h) for h in d.sections)
            for d in cls
            if d.sections
        }
