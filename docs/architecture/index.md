---
title: Architecture boundary
subtitle: What belongs in the graph and what remains outside it
style: mesa
---

## Boundary

The graph is for entities, relations, workflow records, provenance, and
references. Raw spectral imagery and raw telemetry remain outside it. An
imagery reference carries URI and checksum rather than per-pixel, per-band, or
per-tile RDF statements; a shape rejects locally named tile, pixel, and band
predicates on that reference.

This is an architectural constraint expressed by the schema, not an implemented
storage, access-control, or data-pipeline architecture.
