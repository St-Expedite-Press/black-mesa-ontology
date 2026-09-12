"""Repository layout, resolved once.

Five tools previously each computed the repository root from their own file
location. That works until a tool moves, at which point it silently resolves to
the wrong directory. One definition here, imported everywhere.
"""
from __future__ import annotations

from pathlib import Path

# src/workbench/paths.py -> src/workbench -> src -> repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PROJECTS_DIR = REPO_ROOT / "projects"
TEMPLATES_DIR = REPO_ROOT / "templates"
TOOLS_DIR = REPO_ROOT / "tools"
TESTS_DIR = REPO_ROOT / "tests"

# Directories inside a project that hold inputs or build output rather than
# authored documents. build_docs and doc_lint both need this distinction.
INPUT_DIRS = {"sources", "standards"}
OUTPUT_DIRS = {"reports", "visualizations"}
NON_DOCUMENT_DIRS = INPUT_DIRS | OUTPUT_DIRS | {"__pycache__", ".venv"}


#: A published repository names the one project it contains in this file.
#: It is how the flat layout is identified without this module hardcoding any
#: project name - which matters because the module is vendored into a
#: repository that must name no programme. Written by tools/publish_repo.py.
PROJECT_MARKER = ".project"


def project_id() -> str | None:
    """The project this repository contains, if it contains exactly one.

    None in the monorepo, where projects/ holds several and the question has no
    single answer.
    """
    marker = REPO_ROOT / PROJECT_MARKER
    if marker.is_file():
        name = marker.read_text(encoding="utf-8").strip()
        return name or None
    return None


def schema_dir(project: str) -> Path | None:
    """A project's schema directory, in either repository layout.

    This monorepo nests projects as `projects/<name>/schema`. Each project is
    also published as a standalone repository, where that single project is
    flattened to `schema/` at the root - a standalone repo with a `projects/`
    directory holding exactly one project is indirection for no one's benefit.

    Tools and tests that must run in both resolve through here. Returns None
    when the project is not present at all, which is the normal case for the
    sibling project inside a published repository: it is absent by design, and
    a caller should skip rather than fail.
    """
    nested = PROJECTS_DIR / project / "schema"
    if nested.is_dir():
        return nested
    flat = REPO_ROOT / "schema"
    if flat.is_dir() and project_id() == project:
        return flat
    return None


def projects() -> list[Path]:
    """Every project directory, sorted."""
    if not PROJECTS_DIR.is_dir():
        return []
    return sorted(p for p in PROJECTS_DIR.iterdir() if p.is_dir())


def project_of(path: Path) -> Path | None:
    """The project directory containing `path`, or None if it is outside one."""
    path = path.resolve()
    for parent in path.parents:
        if parent.parent == PROJECTS_DIR:
            return parent
    return None


def stylesheets() -> list[str]:
    """Available stylesheet names, without the .css extension."""
    return sorted(p.stem for p in TEMPLATES_DIR.glob("*.css"))


def relative(path: Path) -> str:
    """Repo-relative path for display, falling back to the absolute path."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)
