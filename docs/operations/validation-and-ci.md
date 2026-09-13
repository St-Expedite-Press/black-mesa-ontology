# Validation and CI

Valid Turtle syntax is not equivalent to a valid Black Mesa record.

## Validation layers

### 1. Import resolution

`tools/validate_ontology.py` follows known `owl:imports` through a local import map. This makes the vendored BFO hierarchy load-bearing and keeps routine validation offline/reproducible.

### 2. Structural lint

The validator checks local classes/properties for metadata and structural problems, including undeclared local terms and BFO anchor targets that are not real classes in the loaded standard.

### 3. OWL-RL reasoning

The graph is expanded under OWL-RL and checked for the `owl:Nothing` inconsistency signal. This is a logical consistency check, not a proof of biological truth.

### 4. SHACL

`schema/shapes.ttl` enforces operational contracts such as:

- sensor indications cannot assert pathogen presence;
- diagnostic detections require disposition, custody, confidence, result, version, and time;
- transfers require releasing/receiving custodians;
- imagery references require URI + checksum;
- pathosystem profiles require host/pathogen/role;
- draft rules require human review and a review note.

### 5. Adversarial tests

`tests/fixtures/bmo-violations.ttl` contains deliberate failures. Tests prove that safety constraints reject the target failure modes and return useful messages.

## Commands

```bash
python tools/validate_ontology.py schema/bmo-core.ttl schema/reporting-crosswalks.ttl --shapes schema/shapes.ttl
python -m pytest tests/ -q
python tools/schema_docs.py --schema schema --out docs/reference
python tools/validate_docs.py
```

Generated-reference freshness and local documentation links are part of the documentation integrity contract.

Validation does not substitute for plant-pathology validity, legal review, representative sampling design, secure operational custody, or production-system assurance.
