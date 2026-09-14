---
title: Contributing and testing
subtitle: Change source, exercise constraints, then rebuild references
style: mesa
---

## Contribution loop

Provide labels and comments for local terms, and anchor each local class through
the upper module. Run ontology validation, documentation checks, and focused
tests after changes. When a constraint changes, include a deliberate violation
and ensure it is caught for the intended reason.

Run the complete suite with `python -m pytest tests/ -q`.
