---
title: Ontology change and release
subtitle: Keep source, generated references, tests, and public assembly aligned
style: mesa
---

## Change sequence

1. Change `schema/` or `schema/shapes.ttl` with evidence for the scope.
2. Add a positive or deliberate negative fixture when a shape changes.
3. Regenerate `docs/reference/` with `tools/schema_docs.py`.
4. Run ontology, documentation, and focused tests in the canonical layout.
5. Assemble a disposable flattened repository and repeat its checks.

Do not hand-edit generated references or change a public assembly as the
durable source. See the [release checklist](../maintainers/release-checklist.md).
