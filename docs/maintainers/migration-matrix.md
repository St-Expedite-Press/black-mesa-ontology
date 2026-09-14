---
title: Documentation migration matrix
subtitle: Disposition of pre-rebuild Black Mesa documentation
style: mesa
---

## Documentation migration matrix

This matrix was created before replacing, moving, or deleting active Black Mesa
documentation. The canonical source is the monorepo project directory; the
flattened public repository is assembled by `tools/publish_repo.py`.

| Existing file | Disposition | Replacement / rationale |
|---|---|---|
| `README.md` | REWRITE | `README.md` remains the entry point, rewritten to state the actual Phase 1 boundary and both layouts. |
| `docs/detection-ontology-v0.2.md` | ARCHIVE | Retained under `docs/archive/` as a historically useful design paper; active material is split across concepts, ontology, methodology, workflows, and governance. |
| `docs/schema-reference.md` | MERGE_AND_DELETE | Re-generated as `docs/reference/schema-reference.md`; generated files must live under `docs/reference/`. |
| `docs/class-diagram.md` | MERGE_AND_DELETE | Re-generated as `docs/reference/class-diagram.md`; generated files must live under `docs/reference/`. |

No other Markdown documentation existed at audit time. Internal `sources/` files
are not documentation to publish and are not moved or copied into the public
documentation tree.
