"""Upper-ontology anchoring, checked for every project present.

Project-agnostic on purpose: this module is vendored into each published
repository, including one that must name no programme, so it discovers the
projects in the repository rather than listing them.

The rule these tests guard: no class may be invented without saying what kind
of thing it is. It was weaker than it looked for a while - the shapes accepted
any ancestor under the up: namespace, and nothing ever loaded BFO, so the check
was on an IRI prefix and the vendored standard was decorative.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import rdflib

from conftest import find_schema, present_projects, schema_graph, validate
from validate_ontology import check_anchors

PROJECTS = present_projects()
IDS = [p[0] for p in PROJECTS]
BFO_PREFIX = "http://purl.obolibrary.org/obo/BFO_"


@pytest.mark.parametrize("project,directory", PROJECTS, ids=IDS)
def test_every_domain_class_reaches_bfo(project: str, directory: Path):
    """No class may be invented without saying what kind of thing it is."""
    shapes = directory / "shapes.ttl"
    if not shapes.is_file():
        pytest.skip(f"{project} has no shapes.ttl")
    _, _, text = validate(schema_graph(directory), shapes)
    assert "UNANCHORED CLASS" not in text, (
        f"{project} has classes with no upper-ontology anchor: " + text)


@pytest.mark.parametrize("project,directory", PROJECTS, ids=IDS)
def test_import_closure_carries_bfo(project: str, directory: Path):
    """BFO must be in the graph, not merely committed to vendor/.

    vendor/bfo.owl was loaded by no code path at all: the owl:imports in
    upper-core.ttl was decorative, because rdflib does not follow imports.
    """
    g = schema_graph(directory)
    bfo = {s for s in g.subjects() if str(s).startswith(BFO_PREFIX)}
    assert len(bfo) > 30, (
        f"{project}: only {len(bfo)} BFO terms in the import closure - "
        f"vendor/bfo.owl was not loaded, so the anchoring rule has no "
        f"hierarchy to check")


@pytest.mark.parametrize("project,directory", PROJECTS, ids=IDS)
def test_every_bfo_anchor_target_exists_in_bfo(project: str, directory: Path):
    """The anchors must name real BFO classes, checked against the standard.

    Reaching a BFO IRI proves nothing by itself - subClassOf will point at
    obo:BFO_0000301, which does not exist, and every prefix-matching rule here
    keeps passing. This is what the vendored copy is for.
    """
    assert not check_anchors(schema_graph(directory)), project


@pytest.mark.parametrize("project,directory", PROJECTS, ids=IDS)
def test_a_bogus_bfo_anchor_is_caught(project: str, directory: Path):
    """The adversarial half: plant an anchor that looks right and is not."""
    g = schema_graph(directory)
    g.add((rdflib.URIRef("https://w3id.org/black-mesa/upper/Invented"),
           rdflib.RDFS.subClassOf,
           rdflib.URIRef(BFO_PREFIX + "0000301")))
    issues = check_anchors(g)
    assert issues, "a subClassOf pointing at a non-existent BFO class was accepted"
    assert "BFO_0000301" in issues[0] and "up:Invented" in issues[0], (
        f"caught, but the message does not say what or where: {issues}")


@pytest.mark.parametrize("project,directory", PROJECTS, ids=IDS)
def test_no_undeclared_terms(project: str, directory: Path):
    """Every term used in our own namespace must be declared.

    The gap that let eios:anthropogenicOrigin live in two example files without
    existing: the linter audited declared terms for missing metadata, so a term
    never declared at all had nothing to be audited against. Sixteen terms were
    in that state when the check was first run.
    """
    from validate_ontology import check_undeclared
    assert not check_undeclared(schema_graph(directory)), project
