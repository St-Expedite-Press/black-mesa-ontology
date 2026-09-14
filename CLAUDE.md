# Working rules

This repository contains a Phase 1 conceptual schema for recording a possible
pre-symptomatic agricultural pathogen detection. It is not a deployed sensing,
assay, alerting, or reporting system.

## Public boundary

The public repository intentionally excludes internal project records,
credentials, operational identifiers, and deployment material. Do not add such
material to examples, documentation, fixtures, or generated references.

## Modeling rules

- A spectral anomaly is evidence from imagery, not a diagnosis.
- A detection is an assertion with supporting result, zone, custody chain, and
  rule-set version; an alert is a separate decision.
- Pre-symptomatic indication is a hypothesis that can warrant sampling, not a
  claim that a pathogen is present.
- Raw imagery is referenced by URI and checksum and is not represented as
  pixel, tile, or band triples.
- SHACL conformance checks supplied graph structure only. It does not establish
  biological truth, source authenticity, assay performance, or security.

## Commands

```bash
python tools/validate_ontology.py schema/*.ttl --shapes schema/shapes.ttl
python tools/check_docs.py --project black-mesa-ontology
python -m pytest tests/ -q
```

Generated references under `docs/reference/` must be regenerated from the
Turtle; do not hand-edit them. This repository has no committed reuse license.

---

Assembled from a source monorepo by `tools/publish_repo.py`. Edits made
directly here are overwritten on the next publish.
