---
title: Repository map
subtitle: Authored, generated, and internal-only project material
style: mesa
---

## Map

| Location | Role | Publication status |
|---|---|---|
| `schema/` | Authored conceptual schema and SHACL shapes | Published |
| `docs/` | Authored documentation and generated references | Published |
| `sources/` | Converted internal project records | Not published |
| `visualizations/` | Generated visualization output | Not required for validation |
| `tools/` | Validation, documentation, and publication tooling | Selected tools published |
| `upper/` and `vendor/` | Shared upper module and vendored BFO | Published with an assembly |

The monorepo is canonical. `tools/publish_repo.py` builds a disposable
flattened repository from it.
