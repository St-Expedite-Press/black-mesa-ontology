# Black Mesa ontology

Semantic and evidentiary core for the Black Mesa agricultural biosecurity platform.

Black Mesa is designed to move from **sensor observation → anomaly → hypothesis → targeted sampling → legally defensible specimen custody → diagnostic result → scientific determination → reporting or alerting** without collapsing those stages into one opaque "detection" flag.

The ontology is **sensor-agnostic**. Drone flight and spectral imagery are expected early implementations, but neither is part of the core semantic contract. Thermal systems, fixed stations, ground robots, aircraft, satellite products, or other observation systems should enter through the same evidence model.

## What this repository is

This is the documented operational ontology and validation suite for the Phase 1 detection/evidence chain.

v0.3 design commitments:

- Observation, anomaly, hypothesis, diagnostic determination, regulatory determination, and alert are different objects.
- A **sensor indication is not a diagnosis** and cannot assert pathogen presence.
- Diagnostic disposition (`Confirmed`, `Suspected`, `Not Detected`, `Undetermined`) is separate from evidence stage and confidence.
- Confidence is multi-axis: evidence strength, evidence completeness, applicability, provenance quality, and optional calibrated probability.
- Sampling creates a persistent specimen identity; aliquots receive their own identities while retaining genealogy.
- Legally defensible chain of custody is represented as explicit collection, transfer, receipt, storage, and aliquot events.
- Scientific detection is kept separate from regulatory/reporting decisions.
- Raw imagery and dense sensor arrays stay outside the RDF graph and are referenced by URI + checksum.
- Crops, pathogens, sensors, methods, and other reference vocabularies should use external canonical identifiers rather than being reinvented locally.
- Initial operational jurisdictions are Arkansas, Louisiana, Missouri, Oklahoma, and Texas, represented as data rather than ontology subclasses.

## Read this first

If you are not an ontology engineer:

1. [Team guide](docs/team-guide.md) — what RDF, OWL, SHACL, BFO, SOSA, provenance, custody, confidence, and crosswalks mean in plain language.
2. [Architecture](docs/architecture.md) — how the Black Mesa product is represented end to end, with workflow diagrams.
3. [Canonical workflow](examples/canonical-workflow.ttl) — a worked survey-to-confirmed-detection record.
4. [Negative survey](examples/negative-survey.ttl) — why "surveyed with no anomaly" is not the same thing as "pathogen not detected."

For ontology work:

- [Domain schema](schema/bmo-core.ttl)
- [Reporting crosswalks](schema/reporting-crosswalks.ttl)
- [SHACL constraints](schema/shapes.ttl)
- [Schema reference](docs/schema-reference.md)
- [Class diagram](docs/class-diagram.md)
- [v0.3 design note](docs/detection-ontology-v0.3.md)

## The workflow in one picture

~~~mermaid
flowchart LR
    A[Survey activity] --> B[Sensor observation]
    B --> C[Observed anomaly]
    C --> D[Sensor indication]
    D --> E[Diagnostic hypotheses]
    E --> F[Next-best observation or sampling]
    F --> G[Specimen + custody record]
    G --> H[Diagnostic procedure]
    H --> I[Diagnostic result]
    I --> J[Scientific detection assertion]
    J --> K[Reporting / regulatory evaluation]
    K --> L[Alert or notification]

    C -. does not equal .-> J
    J -. does not equal .-> K
    K -. does not equal .-> L
~~~

## Why the distinctions matter

A sensor may identify an abnormal crop signature without knowing its cause. That should trigger investigation, not silently become a pathogen record.

A laboratory result may be negative without proving that a pathogen is absent from an entire field.

A scientifically confirmed detection may not by itself determine whether an agency must be notified, because reporting rules are jurisdictional and versioned.

A specimen without a continuous identity and custody history may be scientifically interesting but inadequate for a regulatory action.

The ontology exists to keep these distinctions machine-readable.

## External standards and vocabularies

| Standard | Role |
|---|---|
| BFO 2.0 | upper-level categories: information, process, material, site, quality, role |
| IAO / RO | information artifacts and core relations |
| SOSA/SSN | sensors, platforms, observation semantics |
| PROV-O | provenance, derivation, agents, assertion time |
| GeoSPARQL | geometry and spatial relationships |
| QUDT | quantitative values and units when measurement modules are added |
| OBI | selected assay/specimen concepts |
| NCBITaxon and other authorities | external organism identifiers |
| NPDN NDR | diagnostic reporting dispositions and downstream interoperability |
| OASIS CAP 1.2 | alert-message semantics; not treated as diagnostic confidence |

The NPDN diagnostic vocabulary uses Confirmed, Suspected, Not Detected, and Undetermined. Black Mesa maps its **diagnostic dispositions** to those values while explicitly refusing to map a sensor-only indication into them.

CAP certainty is intentionally not treated as equivalent to diagnostic disposition. CAP describes the subject event of an alert; translation belongs in an explicit reporting rule.

## Repository layout

~~~text
schema/
    bmo-core.ttl
    reporting-crosswalks.ttl
    shapes.ttl

upper/
    upper-core.ttl

vendor/
    bfo.owl

examples/
    canonical-workflow.ttl
    negative-survey.ttl

tests/
    fixtures/bmo-violations.ttl
    test_detection_shacl.py
    test_anchoring.py

tools/
    validate_ontology.py
    visualize_ontology.py
    schema_docs.py

docs/
    team-guide.md
    architecture.md
    detection-ontology-v0.3.md
    schema-reference.md
    class-diagram.md
~~~

## Validate it

~~~bash
pip install -r requirements.txt

python tools/validate_ontology.py \
  schema/bmo-core.ttl \
  schema/reporting-crosswalks.ttl \
  --shapes schema/shapes.ttl

python -m pytest tests/ -q
~~~

Regenerate structural documentation after schema changes:

~~~bash
python tools/schema_docs.py --schema schema --out docs
~~~

## Current scope

Phase 1 is the **evidence chain**, not an exhaustive crop/pathogen taxonomy and not a regulatory rules engine.

The first deployment region is the Arkansas–Louisiana–Missouri–Oklahoma–Texas cluster. The core schema must remain portable beyond it.

Near-term work after v0.3:

- bind real crop and pathogen identifiers for pilot use cases;
- define actual sensor/model records once hardware and models are selected;
- add validated diagnostic method profiles;
- encode jurisdiction-specific reporting rules separately from scientific detections;
- add environmental context and spread inference without contaminating the core evidence model.

## Publishing note

This public repository has historically been assembled from a source monorepo. A generated publish can overwrite direct edits here. Any accepted changes therefore need to be carried back into the source-of-truth publishing workspace before the next automated publish.
