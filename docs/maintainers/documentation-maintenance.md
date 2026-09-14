---
title: Documentation maintenance
subtitle: Keep active prose, generated output, and assembly checks aligned
style: mesa
---

## Maintenance

Before a documentation reorganization, update the migration matrix. Keep active
links and examples checked by `tools/check_docs.py`; archive historical material
rather than letting it be read as current. Regenerate schema references after
Turtle changes and run the byte-for-byte freshness test.

When publishing, validate a freshly assembled flattened repository. Never copy
internal `sources/` into public documentation.
