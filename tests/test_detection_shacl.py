"""The detection-core SHACL constraints must accept the schema and reject the
fixture.

Separated from the ecosystem-typology suite so that neither travels into the
other's published repository. The two projects are kept apart by rule, and
their tests are part of what gets published alongside them.
"""
from __future__ import annotations

import pytest

from conftest import FIXTURES, find_schema, schema_graph, validate

SCHEMA_DIR = find_schema("bmo-core.ttl")
pytestmark = pytest.mark.skipif(
    SCHEMA_DIR is None, reason="this schema is not present in this repository")

SHAPES = SCHEMA_DIR / "shapes.ttl" if SCHEMA_DIR else None
VIOLATIONS = FIXTURES / "bmo-violations.ttl"

EXPECTED_VIOLATIONS = {
    "UnanchoredThing": "UNANCHORED CLASS",
    "UntraceableDetection": "custody chain",
    "OverbroadDetection": "exactly one zone",
    "TiledImagery": "GRAPH BOUNDARY VIOLATION",
    "BlindConfidence": "assay applicability",
    "SilentTier": "presupposes visible symptoms",
    "SilentCrosswalk": "fidelity",
}


def test_detection_core_conforms():
    conforms, _, text = validate(schema_graph(SCHEMA_DIR), SHAPES)
    assert conforms, "detection core must pass its own constraints: " + text


def test_detection_fixture_is_rejected():
    g = schema_graph(SCHEMA_DIR)
    g.parse(VIOLATIONS, format="turtle")
    conforms, _, _ = validate(g, SHAPES)
    assert not conforms, "the detection violation fixture was accepted"


@pytest.mark.parametrize("node,fragment", sorted(EXPECTED_VIOLATIONS.items()))
def test_each_detection_violation_is_caught(node: str, fragment: str):
    g = schema_graph(SCHEMA_DIR)
    g.parse(VIOLATIONS, format="turtle")
    _, _, text = validate(g, SHAPES)
    assert node in text, f"{node} produced no violation"
    assert fragment.lower() in text.lower(), (
        f"{node} was caught but the message did not explain why "
        f"(expected to mention {fragment!r})")
