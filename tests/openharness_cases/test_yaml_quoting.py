from __future__ import annotations

import pytest

from .common import Path, REPO_ROOT, CreateTaskInput, create_task_package, openharness
from openharness_cli.repository.yaml import _load_yaml


def test_create_task_package_quotes_yaml_sensitive_status_fields(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "task-packages").mkdir(parents=True)
    (repo_root / "skills" / "using-openharness" / "references" / "manifest.yaml").write_text(
        "version: 1\n"
        "task_packages_root: docs/task-packages\n"
        "archived_task_packages_root: docs/archived/task-packages\n"
        "required_design_files:\n"
        "  - README.md\n"
        "  - task-info.yaml\n"
        "  - 01-requirements.md\n"
        "  - 02-overview-design.md\n"
        "  - 03-detailed-design.md\n"
        "  - verification_design.md\n"
        "  - evidence.md\n",
        encoding="utf-8",
    )
    template_root = repo_root / "skills" / "using-openharness" / "references" / "templates"
    (template_root / "task-package.README.md").write_text("# <DESIGN_ID> <TITLE>\n", encoding="utf-8")
    (template_root / "task-package.task-info.yaml").write_text(
        "id: <DESIGN_ID>\n"
        "title: <TITLE>\n"
        "status: <STATUS>\n"
        "summary: <SUMMARY>\n"
        "owner: <OWNER>\n"
        "created_at: <DATE>\n"
        "updated_at: <DATE>\n",
        encoding="utf-8",
    )
    for name in (
        "task-package.01-requirements.md",
        "task-package.02-overview-design.md",
        "task-package.03-detailed-design.md",
        "task-package.verification_design.md",
        "task-package.evidence.md",
    ):
        (template_root / name).write_text("x\n", encoding="utf-8")

    task_root = create_task_package(
        CreateTaskInput(
            repo_root=repo_root,
            task_name="Quote Probe",
            task_id="OH-017",
            title="`02-overview-design.md` guidance: quote YAML",
            owner="codex",
            summary="`02-overview-design.md` guidance: explain quoting.",
        )
    )

    status_text = (task_root / "task-info.yaml").read_text(encoding="utf-8")
    status = _load_yaml(task_root / "task-info.yaml")

    assert 'title: "`02-overview-design.md` guidance: quote YAML"' in status_text
    assert 'summary: "`02-overview-design.md` guidance: explain quoting."' in status_text
    assert status["title"] == "`02-overview-design.md` guidance: quote YAML"
    assert status["summary"] == "`02-overview-design.md` guidance: explain quoting."


@pytest.mark.skip(reason="template simplified")
def test_author_entry_documents_yaml_quote_rule_with_examples() -> None:
    text = (
        REPO_ROOT / "skills" / "using-openharness" / "references" / "author-entry.md"
    ).read_text(encoding="utf-8")

    assert "task-info.yaml" in text
    assert "double quotes" in text
    assert "`02-overview-design.md` guidance: explain the boundary." in text
