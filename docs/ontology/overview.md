---
title: Ontology overview
subtitle: A BFO-anchored conceptual schema with limited formalization
style: mesa
---

## Normative artifacts

`schema/bmo-core.ttl` contains the 20 local classes, 22 local properties, and
confidence-tier individuals. `schema/shapes.ttl` contains SHACL constraints.
`upper/upper-core.ttl` and `vendor/bfo.owl` are required local imports for
validation. The Turtle and SHACL, not this prose, are normative.

The schema is intentionally a documented conceptual schema rather than a fully
axiomatized ontology. It uses OWL syntax and BFO anchors for type distinctions,
but does not claim complete domain axiomatization.
