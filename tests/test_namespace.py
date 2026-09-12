"""Persistent namespace and licensing invariants."""
from __future__ import annotations

from pathlib import Path

import rdflib
from rdflib import DCTERMS, OWL, RDF

from conftest import ROOT

BMO_ONTOLOGY = rdflib.URIRef("https://w3id.org/black-mesa/bmo")
UPPER_ONTOLOGY = rdflib.URIRef("https://w3id.org/black-mesa/upper")
CC_BY_4 = rdflib.URIRef("https://creativecommons.org/licenses/by/4.0/")

SCAN_DIRS = ("schema", "upper", "examples", "reference", "rules", "tests", "tools")
FORBIDDEN = (
    "https://" + "example.org/bmo/",
    "https://" + "example.org/upper/",
)


def test_no_deprecated_local_namespace_remains():
    findings = []
    for dirname in SCAN_DIRS:
        for path in (ROOT / dirname).glob("**/*"):
            if not path.is_file() or path.suffix not in {".ttl", ".py", ".md", ".yml", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8")
            for old in FORBIDDEN:
                if old in text:
                    findings.append(f"{path.relative_to(ROOT)} contains {old}")
    assert not findings, "\n".join(findings)


def test_core_ontology_has_persistent_identity_version_and_license():
    g = rdflib.Graph().parse(ROOT / "schema" / "bmo-core.ttl", format="turtle")
    assert (BMO_ONTOLOGY, RDF.type, OWL.Ontology) in g
    assert (BMO_ONTOLOGY, DCTERMS.license, CC_BY_4) in g
    assert (
        BMO_ONTOLOGY,
        OWL.versionIRI,
        rdflib.URIRef("https://w3id.org/black-mesa/bmo/releases/0.4.0"),
    ) in g


def test_upper_ontology_has_persistent_identity_and_license():
    g = rdflib.Graph().parse(ROOT / "upper" / "upper-core.ttl", format="turtle")
    assert (UPPER_ONTOLOGY, RDF.type, OWL.Ontology) in g
    assert (UPPER_ONTOLOGY, DCTERMS.license, CC_BY_4) in g
