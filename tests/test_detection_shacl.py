"""Adversarial SHACL tests for the Black Mesa v0.3 detection core.

Every high-consequence modelling rule gets a planted violation. The point is
not merely that valid Turtle parses; the suite proves that the constraints that
protect the evidence chain actually reject the failure modes they were written
for.
"""
from __future__ import annotations

import pytest

from conftest import FIXTURES, find_schema, schema_graph, validate

SCHEMA_DIR = find_schema("bmo-core.ttl")
pytestmark = pytest.mark.skipif(
    SCHEMA_DIR is None, reason="this schema is not present in this repository"
)

SHAPES = SCHEMA_DIR / "shapes.ttl" if SCHEMA_DIR else None
VIOLATIONS = FIXTURES / "bmo-violations.ttl"

EXPECTED_VIOLATIONS = {
    "UnanchoredThing": "UNANCHORED CLASS",
    "SensorClaimingPathogen": "cannot assert pathogen presence",
    "UntraceableDetection": "custody record",
    "DetectionNoDisposition": "diagnostic disposition",
    "IndicationWithBlindConfidence": "model applicability",
    "DetectionWithBlindConfidence": "assay applicability",
    "BrokenTransfer": "receiving custodian",
    "TiledImagery": "GRAPH BOUNDARY VIOLATION",
    "SilentCrosswalk": "state fidelity",
    "CrosswalkNoTarget": "crosswalkTo",
    "IncompletePilot": "canonical pathogen taxon",
    "UnsafeDraftRule": "draft rule must require human review",
    "DraftRuleNoReviewNote": "legal review note",
}


def test_detection_core_conforms():
    conforms, _, text = validate(schema_graph(SCHEMA_DIR), SHAPES)
    assert conforms, "detection core must pass its own constraints: " + text


def test_detection_fixture_is_rejected():
    g = schema_graph(SCHEMA_DIR)
    g.parse(VIOLATIONS, format="turtle")
    conforms, _, _ = validate(g, SHAPES)
    assert not conforms, "the deliberate violation fixture was accepted"


@pytest.mark.parametrize("node,fragment", sorted(EXPECTED_VIOLATIONS.items()))
def test_each_detection_violation_is_caught(node: str, fragment: str):
    g = schema_graph(SCHEMA_DIR)
    g.parse(VIOLATIONS, format="turtle")
    _, _, text = validate(g, SHAPES)
    assert node in text, f"{node} produced no violation"
    assert fragment.lower() in text.lower(), (
        f"{node} was caught but the message did not explain why "
        f"(expected to mention {fragment!r})"
    )
