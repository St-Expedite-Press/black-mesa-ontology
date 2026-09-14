"""Shared test helpers, and the project discovery every suite depends on.

WHY DISCOVERY RATHER THAN A LIST OF PROJECT NAMES

Each project is published as its own repository, one of which is independent
research that must name no programme, platform, funder or company. Tests are
vendored into those repositories alongside the schema they guard, so a test
module that hardcodes both project names cannot travel into either of them.

So the suites ask which projects are actually present and parametrise over the
answer. A project that is absent is absent by design, and its tests simply do
not exist rather than failing or being skipped by name.
"""
from __future__ import annotations

import sys
from pathlib import Path

import rdflib

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

# Project-local packages, discovered the same way and for the same reason as
# present_projects() below: this file travels into a repository that may not
# name a project. In a published repository projects/ is absent and the single
# project's package is already under the src/ added above.
for _p in sorted((ROOT / "projects").iterdir()) if (ROOT / "projects").is_dir() else []:
    if (_p / "src").is_dir():
        sys.path.insert(0, str(_p / "src"))

from workbench.paths import PROJECTS_DIR, REPO_ROOT, project_id  # noqa: E402
from validate_ontology import resolve_imports  # noqa: E402

UPPER = REPO_ROOT / "upper" / "upper-core.ttl"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def present_projects() -> list[tuple[str, Path]]:
    """Every project in this repository, in either layout, as (id, schema dir).

    The monorepo yields several from projects/*/schema. A published repository
    yields exactly one, from its flat schema/ named by the .project marker.
    """
    found: list[tuple[str, Path]] = []
    if PROJECTS_DIR.is_dir():
        for d in sorted(PROJECTS_DIR.iterdir()):
            if (d / "schema").is_dir() and any((d / "schema").glob("*.ttl")):
                found.append((d.name, d / "schema"))
    if found:
        return found
    flat = REPO_ROOT / "schema"
    if flat.is_dir() and any(flat.glob("*.ttl")):
        return [(project_id() or "this-project", flat)]
    return []


def schema_graph(directory: Path) -> rdflib.Graph:
    """A schema directory plus its resolved import closure.

    The closure is resolved with the same function validate_ontology.py uses,
    so the tests and the command line validate the same graph. They did not
    before: the tests loaded upper-core.ttl but nothing loaded BFO, and the
    anchoring rule could only ever check IRI prefixes.
    """
    g = rdflib.Graph()
    loaded: set[Path] = set()
    for ttl in sorted(directory.glob("*.ttl")):
        if ttl.name != "shapes.ttl":
            g.parse(ttl, format="turtle")
            loaded.add(ttl.resolve())
    unresolved = resolve_imports(g, loaded)
    assert not unresolved, f"unresolved owl:imports: {unresolved}"
    assert UPPER.resolve() in loaded, (
        "the schema did not import the shared upper module; the anchoring rule "
        "cannot be checked without it")
    return g


def validate(graph: rdflib.Graph, shapes_path: Path):
    from pyshacl import validate as shacl_validate

    shapes = rdflib.Graph().parse(shapes_path, format="turtle")
    return shacl_validate(graph, shacl_graph=shapes, inference="rdfs")


def has_schema(directory: Path, marker: str) -> bool:
    """Whether this schema directory is the one carrying `marker`."""
    return (directory / marker).is_file()


def find_schema(marker: str) -> Path | None:
    """The schema directory containing `marker`, or None.

    Keyed on a file the schema itself contains rather than on a project name,
    so a test module can locate the schema it guards without naming a project.
    """
    for _, directory in present_projects():
        if has_schema(directory, marker):
            return directory
    return None
