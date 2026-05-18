
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class RuntimeWorkflowPackage:
    root: Path
    workflow_path: Path
    name: str
    description: str
