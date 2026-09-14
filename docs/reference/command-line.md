---
title: Command-line reference
subtitle: Commands in the canonical project and flattened assembly
style: mesa
---

## Commands

| Purpose | Canonical | Flattened |
|---|---|---|
| Ontology validation | `python tools/validate_ontology.py projects/black-mesa-ontology/schema/bmo-core.ttl projects/black-mesa-ontology/schema/shapes.ttl --shapes projects/black-mesa-ontology/schema/shapes.ttl` | `python tools/validate_ontology.py schema/bmo-core.ttl schema/shapes.ttl --shapes schema/shapes.ttl` |
| Reference generation | `python tools/schema_docs.py --schema projects/black-mesa-ontology/schema --out projects/black-mesa-ontology/docs/reference` | `python tools/schema_docs.py --schema schema --out docs/reference` |
| Documentation checks | `python tools/check_docs.py --project black-mesa-ontology` | `python tools/check_docs.py --project black-mesa-ontology` |

Use the active virtual environment's Python in the canonical checkout.
