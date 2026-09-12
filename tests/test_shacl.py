"""The SHACL constraints must accept the real schema and reject the fixture.

Both halves matter. A constraint that only ever sees valid data is untested,
and a constraint so strict it rejects the real schema is worse than none.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import rdflib

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from blackmesa.paths import REPO_ROOT, TESTS_DIR, schema_dir  # noqa: E402
from validate_ontology import check_anchors, resolve_imports  # noqa: E402

UPPER = REPO_ROOT / "upper" / "upper-core.ttl"

# Resolved through schema_dir so the suite runs both here and inside a
# published standalone repository. A project that is absent there is absent
# by design - the repositories are deliberately separate - so the tests for
# it skip rather than fail.
SCHEMA_DIR = schema_dir("guis-ecosystem-typology")
SHAPES = SCHEMA_DIR / "shapes.ttl" if SCHEMA_DIR else None
VIOLATIONS = TESTS_DIR / "fixtures" / "shacl-violations.ttl"

BM_SCHEMA_DIR = schema_dir("black-mesa-ontology")
BM_SHAPES = BM_SCHEMA_DIR / "shapes.ttl" if BM_SCHEMA_DIR else None
BM_VIOLATIONS = TESTS_DIR / "fixtures" / "bmo-violations.ttl"

#: Skip, do not fail, when a project is not in this repository. Inside a
#: published standalone repository the sibling project is absent on purpose.
needs_guis = pytest.mark.skipif(
    SCHEMA_DIR is None, reason="ecosystem-typology schema not present in this repository")
needs_bm = pytest.mark.skipif(
    BM_SCHEMA_DIR is None, reason="detection schema not present in this repository")

BM_EXPECTED = {
    "UnanchoredThing": "UNANCHORED CLASS",
    "UntraceableDetection": "custody chain",
    "OverbroadDetection": "exactly one zone",
    "TiledImagery": "GRAPH BOUNDARY VIOLATION",
    "BlindConfidence": "assay applicability",
    "SilentTier": "presupposes visible symptoms",
    "SilentCrosswalk": "fidelity",
}

# Each fixture node and the substring its violation message must contain.
EXPECTED_VIOLATIONS = {
    "WronglyNestedL5": "must not be nested under a Level 4",
    "UnattachedL5": "must be assigned to a Level 3",
    "SomeOccurrence": "assessed of a TYPE",
    "OverclaimingType": "epistemic status",
    "EcotypeUsingL5Property": "must not be used on a Level 4",
    "PurposelessRequirement": "purpose",
    # The two axes: anthropogenic origin belongs to the type, collapsed state
    # to an occurrence, and merging them is the mistake worth constraining.
    "OriginlessType": "must declare exactly one eios:anthropogenicOrigin",
    "OccurrenceWithOrigin": "Origin belongs to the TYPE",
    "OccurrenceWithOriginAsState": "not a state",
    "UnthresholdedCollapse": "threshold claim",
    "TypelessCollapseDescription": "type-relative",
    "DanglingTransformation": "antecedent occurrence",
    "ConflatedOccurrence": "ORIGIN/STATE CONFLATION",
}


def schema_graph(directory: Path = SCHEMA_DIR) -> rdflib.Graph:
    """The project's schema plus its resolved import closure.

    The closure is resolved with the same function validate_ontology.py uses,
    so the tests and the command line validate the same graph. They did not
    before: the tests loaded upper-core.ttl but nothing loaded BFO, and the
    anchoring rule could only ever check IRI prefixes.
    """
    g = rdflib.Graph()
    loaded = set()
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


def validate(graph: rdflib.Graph, shapes_path: Path = SHAPES):
    from pyshacl import validate as shacl_validate

    shapes = rdflib.Graph().parse(shapes_path, format="turtle")
    return shacl_validate(graph, shacl_graph=shapes, inference="rdfs")


@needs_guis
def test_real_schema_conforms():
    conforms, _, text = validate(schema_graph())
    assert conforms, f"the committed schema must pass its own constraints:\n{text}"


@needs_guis
def test_fixture_is_rejected():
    g = schema_graph()
    g.parse(VIOLATIONS, format="turtle")
    conforms, _, text = validate(g)
    assert not conforms, "the violation fixture was accepted - constraints are not firing"


@pytest.mark.parametrize("node,fragment", sorted(EXPECTED_VIOLATIONS.items()))
@needs_guis
def test_each_violation_is_caught(node: str, fragment: str):
    g = schema_graph()
    g.parse(VIOLATIONS, format="turtle")
    _, _, text = validate(g)
    assert node in text, f"{node} produced no violation"
    assert fragment.lower() in text.lower(), (
        f"{node} was caught but the message did not explain why "
        f"(expected to mention {fragment!r})")


@needs_guis
def test_messages_cite_their_authority():
    """The architectural constraint must name its source in the message.

    Someone hitting this rule years from now will not have read the papers.
    """
    shapes_text = SHAPES.read_text(encoding="utf-8")
    assert "Keith et al. 2020" in shapes_text, (
        "the Level 4/5 constraint must cite the standard it enforces")


# --- the detection core -----------------------------------------------------


@needs_bm
def test_detection_core_conforms():
    conforms, _, text = validate(schema_graph(BM_SCHEMA_DIR), BM_SHAPES)
    assert conforms, "detection core must pass its own constraints: " + text


@needs_bm
def test_detection_fixture_is_rejected():
    g = schema_graph(BM_SCHEMA_DIR)
    g.parse(BM_VIOLATIONS, format="turtle")
    conforms, _, _ = validate(g, BM_SHAPES)
    assert not conforms, "the detection violation fixture was accepted"


@pytest.mark.parametrize("node,fragment", sorted(BM_EXPECTED.items()))
@needs_bm
def test_each_detection_violation_is_caught(node: str, fragment: str):
    g = schema_graph(BM_SCHEMA_DIR)
    g.parse(BM_VIOLATIONS, format="turtle")
    _, _, text = validate(g, BM_SHAPES)
    assert node in text, f"{node} produced no violation"
    assert fragment.lower() in text.lower(), (
        f"{node} was caught but the message did not explain why "
        f"(expected to mention {fragment!r})")


# --- upper-ontology anchoring ----------------------------------------------


@pytest.mark.parametrize("project,shapes", [
    ("guis-ecosystem-typology", SHAPES),
    ("black-mesa-ontology", BM_SHAPES),
])
def test_every_domain_class_reaches_bfo(project: str, shapes: Path):
    """No class may be invented without saying what kind of thing it is."""
    directory = schema_dir(project)
    if directory is None:
        pytest.skip("project not present in this repository")
    g = schema_graph(directory)
    conforms, _, text = validate(g, shapes)
    assert "UNANCHORED CLASS" not in text, (
        f"{project} has classes with no upper-ontology anchor: " + text)


@needs_bm
def test_import_closure_carries_bfo():
    """BFO must be in the graph, not merely committed to vendor/.

    vendor/bfo.owl was loaded by no code path at all: the owl:imports in
    upper-core.ttl was decorative, because rdflib does not follow imports.
    """
    g = schema_graph(BM_SCHEMA_DIR)
    bfo = {s for s in g.subjects()
           if str(s).startswith("http://purl.obolibrary.org/obo/BFO_")}
    assert len(bfo) > 30, (
        f"only {len(bfo)} BFO terms in the import closure — vendor/bfo.owl was "
        f"not loaded, so the anchoring rule has no hierarchy to check")


@pytest.mark.parametrize("directory", [SCHEMA_DIR, BM_SCHEMA_DIR])
def test_every_bfo_anchor_target_exists_in_bfo(directory: Path):
    """The anchors must name real BFO classes, checked against the standard.

    Reaching a BFO IRI proves nothing by itself — subClassOf will point at
    obo:BFO_0000301, which does not exist, and every prefix-matching rule here
    keeps passing. This is what the vendored copy is for.
    """
    if directory is None:
        pytest.skip("project not present in this repository")
    assert not check_anchors(schema_graph(directory))


@pytest.mark.parametrize("directory", [SCHEMA_DIR, BM_SCHEMA_DIR])
def test_a_bogus_bfo_anchor_is_caught(directory: Path):
    """The adversarial half: plant an anchor that looks right and is not."""
    if directory is None:
        pytest.skip("project not present in this repository")
    g = schema_graph(directory)
    g.add((rdflib.URIRef("https://example.org/upper/Invented"),
           rdflib.RDFS.subClassOf,
           rdflib.URIRef("http://purl.obolibrary.org/obo/BFO_0000301")))
    issues = check_anchors(g)
    assert issues, "a subClassOf pointing at a non-existent BFO class was accepted"
    assert "BFO_0000301" in issues[0] and "up:Invented" in issues[0], (
        f"caught, but the message does not say what or where: {issues}")


def test_upper_module_names_neither_project():
    """A shared upper module must stay project-neutral."""
    text = UPPER.read_text(encoding="utf-8").lower()
    for forbidden in ("black mesa", "darpa", "guis", "gulf islands", "ouachita",
                      "pathogen", "ecosystem typology"):
        assert forbidden not in text, (
            f"upper module mentions {forbidden!r}; it must read as natural in "
            f"either domain or the term belongs in a project file")
