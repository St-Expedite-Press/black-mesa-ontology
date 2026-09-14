---
title: Quickstart
subtitle: Parse the schema, regenerate references, and check docs
style: mesa
---

## Canonical checkout

```powershell
.venv\Scripts\python.exe tools\validate_ontology.py projects\black-mesa-ontology\schema\bmo-core.ttl projects\black-mesa-ontology\schema\shapes.ttl --shapes projects\black-mesa-ontology\schema\shapes.ttl
.venv\Scripts\python.exe tools\schema_docs.py --schema projects\black-mesa-ontology\schema --out projects\black-mesa-ontology\docs\reference
.venv\Scripts\python.exe tools\check_docs.py --project black-mesa-ontology
```

Validation checks parseability, local imports, structural lint, an OWL-RL smoke
closure, and SHACL conformance. It does not validate real-world detections or
assay performance.
