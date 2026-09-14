# Black Mesa Ontology

Black Mesa Ontology is a Phase 1 conceptual schema for recording a possible
pre-symptomatic crop-pathogen detection from a flight through sampling, assay,
and a possible alert. It makes the evidence chain, confidence, and storage
boundary explicit; it is not a detector, assay implementation, alert service,
surveillance deployment, or evidence that any pathogen is present.

The implemented schema contains 20 local classes and 22 local properties in
`schema/bmo-core.ttl`, with SHACL constraints in `schema/shapes.ttl`. It models
farms, fields, zones, flights, anomalies, collections, specimens, assays,
results, detections, confidence, custody, imagery references, and alerts.
A detection is an assertion about a zone, not a fact stamped on a farm.

## Status and boundaries

Implemented now: the conceptual Turtle schema, BFO anchoring, SHACL shapes,
deliberate invalid fixtures, ontology validation, and generated references.
The project references external vocabularies rather than distributing or fully
importing them. `ReportingCrosswalk` is modeled, but no NPDN or CAP mapping
entry has been authored. This repository does not demonstrate integration,
deployment, assay performance, or scientific validation.

Raw imagery and telemetry are outside the graph. The schema permits a URI and
checksum reference to imagery; it does not model pixels, tiles, image storage,
or a data pipeline.

## Start here

- [Documentation index](docs/index.md)
- [Getting started](docs/getting-started/overview.md)
- [Ontology overview](docs/ontology/overview.md)
- [Known limitations](docs/methodology/validation-and-limitations.md)
- [Generated schema reference](docs/reference/schema-reference.md)

## Validate

In the canonical monorepo:

```powershell
.venv\Scripts\python.exe tools\validate_ontology.py projects\black-mesa-ontology\schema\bmo-core.ttl projects\black-mesa-ontology\schema\shapes.ttl --shapes projects\black-mesa-ontology\schema\shapes.ttl
.venv\Scripts\python.exe tools\check_docs.py --project black-mesa-ontology
.venv\Scripts\python.exe -m pytest tests\test_detection_shacl.py tests\test_docs_rebuild.py -q
```

In the flattened public layout:

```powershell
python tools\validate_ontology.py schema\bmo-core.ttl schema\shapes.ttl --shapes schema\shapes.ttl
python tools\check_docs.py --project black-mesa-ontology
python -m pytest tests\ -q
```

The canonical monorepo is authoritative. A public repository is an assembly
created with `tools/publish_repo.py`; do not edit it as a durable source.

## License and maturity

No reuse license is currently committed for this project. Reuse rights and
third-party notices are therefore not established by this repository. This is
an early conceptual artifact, not a validated scientific or production system.
