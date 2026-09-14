---
title: Installation and layouts
subtitle: Dependencies and canonical versus flattened paths
style: mesa
---

## Layouts

The canonical checkout keeps this project below `projects/black-mesa-ontology`.
The public assembly flattens the project so that `schema/`, `docs/`, and
`README.md` are at its root. Python dependencies are listed in the repository
root `requirements.txt` in both layouts.

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Do not copy internal `sources/` into a public assembly; publication tooling
intentionally excludes them.
