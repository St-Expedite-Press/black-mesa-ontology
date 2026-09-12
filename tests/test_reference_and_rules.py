"""Validate pilot reference data and jurisdictional rule records against the schema."""
from __future__ import annotations

from pathlib import Path

import rdflib

from conftest import ROOT, find_schema, schema_graph, validate

BMO = rdflib.Namespace("https://w3id.org/black-mesa/bmo/")

SCHEMA_DIR = find_schema("bmo-core.ttl")
SHAPES = SCHEMA_DIR / "shapes.ttl" if SCHEMA_DIR else None


def project_data_graph() -> rdflib.Graph:
    g = schema_graph(SCHEMA_DIR)
    for path in sorted((ROOT / "reference").glob("*.ttl")):
        g.parse(path, format="turtle")
    for path in sorted((ROOT / "rules").glob("**/*.ttl")):
        g.parse(path, format="turtle")
    return g


def test_reference_and_rule_data_conform():
    conforms, _, text = validate(project_data_graph(), SHAPES)
    assert conforms, text


def test_exactly_four_initial_pilot_profiles():
    g = project_data_graph()
    profiles = set(g.subjects(rdflib.RDF.type, BMO.PilotPathosystem))
    assert len(profiles) == 4


def test_five_state_rule_intakes_are_draft_and_human_reviewed():
    g = project_data_graph()
    rules = set(g.subjects(rdflib.RDF.type, BMO.ReportingRule))
    # reporting-crosswalks are Crosswalks, not ReportingRule instances; the
    # five state intake files should therefore be the only rule records here.
    assert len(rules) == 5
    for rule in rules:
        assert (rule, BMO.ruleReviewStatus, BMO.DraftRequiresLegalRegulatoryReview) in g
        assert (rule, BMO.requiresHumanReview, rdflib.Literal(True)) in g
