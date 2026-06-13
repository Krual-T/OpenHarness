from .common import Path, REPO_ROOT, TaskPackageDocument, create_task_package, setup_harness, openharness
from openharness_cli.core.yaml import load_yaml

TASK_TYPE_PLACEHOLDER = "<mechanical|standard|structural|>"
DESIGN_REVIEW_MODE_PLACEHOLDER = "<stepwise|auto|>"
VERIFICATION_METHOD_PLACEHOLDER = "<unit_test|qualitative|>"
RWP_ENABLED_PLACEHOLDER = "<true|false|>"
RWP_REASON_PLACEHOLDER = "<rwp reason>"


def test_create_task_package_quotes_yaml_sensitive_status_fields(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    (repo_root / "skills" / "using-openharness" / "references" / "templates").mkdir(parents=True)
    (repo_root / "docs" / "task-packages").mkdir(parents=True)
    template_root = repo_root / "skills" / "using-openharness" / "references" / "templates"
    (template_root / "task-package.task-info.yaml").write_text(
        "id: <TASK_ID>\n"
        "title: <TITLE>\n"
        "status: <STATUS>\n"
        "summary: <SUMMARY>\n"
        "owner: <GIT OWNER>\n"
        "created_at: <DATE>\n"
        "updated_at: <DATE>\n"
        "collaboration:\n"
        f"  task_type: {TASK_TYPE_PLACEHOLDER}\n"
        f"  design_review_mode: {DESIGN_REVIEW_MODE_PLACEHOLDER}\n"
        "verification:\n"
        f"  method: {VERIFICATION_METHOD_PLACEHOLDER}\n"
        "  rwp:\n"
        f"    enabled: {RWP_ENABLED_PLACEHOLDER}\n"
        f"    reason: {RWP_REASON_PLACEHOLDER}\n",
        encoding="utf-8",
    )
    for name in (
        "task-package.requirements.md",
        "task-package.overview-design.md",
        "task-package.detailed-design.md",
        "task-package.plan.md",
        "task-package.evidence.md",
    ):
        (template_root / name).write_text("x\n", encoding="utf-8")

    setup_harness(repo_root)
    task_root, task_id = create_task_package(
        task_name="Quote Probe",
        title="`overview-design.md` guidance: quote YAML",
        summary="`overview-design.md` guidance: explain quoting.",
    )

    status_text = TaskPackageDocument.TASK_INFO.path_from(task_root).read_text(encoding="utf-8")
    status = load_yaml(TaskPackageDocument.TASK_INFO.path_from(task_root))

    assert 'title: "`overview-design.md` guidance: quote YAML"' in status_text
    assert 'summary: "`overview-design.md` guidance: explain quoting."' in status_text
    assert status["id"] == task_id
    assert status["title"] == "`overview-design.md` guidance: quote YAML"
    assert status["summary"] == "`overview-design.md` guidance: explain quoting."
    assert status["collaboration"]["task_type"] == TASK_TYPE_PLACEHOLDER
    assert status["collaboration"]["design_review_mode"] == DESIGN_REVIEW_MODE_PLACEHOLDER
    assert status["verification"]["method"] == VERIFICATION_METHOD_PLACEHOLDER
    assert status["verification"]["rwp"]["enabled"] == RWP_ENABLED_PLACEHOLDER
    assert status["verification"]["rwp"]["reason"] == RWP_REASON_PLACEHOLDER
