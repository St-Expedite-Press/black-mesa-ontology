---
title: Module map
subtitle: Local schema, shapes, upper module, and external references
style: mesa
---

## Modules

| Artifact | Role |
|---|---|
| `schema/bmo-core.ttl` | Local detection-core terms and confidence tiers |
| `schema/shapes.ttl` | Closed-world validation constraints |
| `upper/upper-core.ttl` | Shared BFO-anchored upper concepts |
| `vendor/bfo.owl` | Vendored BFO import for offline validation |

External terms from SOSA/SSN, QUDT, GeoSPARQL, NCBITaxon, OBI, and PATO are
referenced where present in the Turtle; they are not fully vendored or imported.
