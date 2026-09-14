"""Repository-wide checks for rebuilt project documentation in either layout."""
from __future__ import annotations

import sys
import json
import subprocess
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from check_docs import validate  # noqa: E402


def project_root() -> Path:
    """Find the one published project, or the EIOS project in the monorepo.

    This test is vendored into both public assemblies. The source monorepo has
    both projects and retains the established EIOS coverage; a flattened
    assembly has only its own README, docs, and schema at ROOT.
    """
    canonical = ROOT / "projects" / "guis-ecosystem-typology"
    return canonical if canonical.is_dir() else ROOT


def active_projects() -> list[Path]:
    """Discover project documentation without naming every monorepo project.

    The test file is vendored into a publication that must keep its shared
    toolchain project-neutral. A flat assembly has its own schema at ROOT.
    """
    candidates = ROOT / "projects"
    if candidates.is_dir():
        return [path for path in sorted(candidates.iterdir())
                if (path / "README.md").is_file() and (path / "docs").is_dir()
                and (path / "schema").is_dir()]
    return [ROOT]


def test_active_documentation_is_internally_consistent():
    for project in active_projects():
        errors = validate(project, project / "schema")
        assert not errors, "\n".join(errors)


def test_all_committed_visual_examples_validate():
    project = project_root()
    if not (project / "contracts" / "visual-evidence-v1.schema.json").is_file():
        return
    schema = json.loads((project / "contracts" / "visual-evidence-v1.schema.json").read_text(encoding="utf-8"))
    for path in sorted((project / "examples").glob("photo-evidence-*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(record)


def test_invalid_visual_example_fails_for_media_identity():
    project = project_root()
    fixture = ROOT / "tests" / "fixtures" / "visual-evidence-invalid.json"
    if not (project / "contracts" / "visual-evidence-v1.schema.json").is_file():
        return
    schema = json.loads((project / "contracts" / "visual-evidence-v1.schema.json").read_text(encoding="utf-8"))
    record = json.loads(fixture.read_text(encoding="utf-8"))
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(record))
    paths = {tuple(error.absolute_path) for error in errors}
    assert ("media_asset", "sha256") in paths
    assert ("media_asset", "mime_type") in paths


def test_generated_reference_documentation_is_fresh(tmp_path):
    for index, project in enumerate(active_projects()):
        out = tmp_path / str(index)
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "schema_docs.py"),
             "--schema", str(project / "schema"), "--out", str(out)],
            check=True,
        )
        generated = tuple(path.name for path in sorted(out.glob("*.md")))
        assert generated, "reference generator emitted no documentation"
        for name in generated:
            expected = project / "docs" / "reference" / name
            assert (out / name).read_bytes() == expected.read_bytes(), f"regenerate {expected}"
