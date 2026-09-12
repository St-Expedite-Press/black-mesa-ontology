"""Shared, project-neutral library for repository tooling.

Submodules are loaded lazily. Ontology validation only needs workbench.paths
and must not acquire document-rendering dependencies (YAML, browser tooling,
etc.) merely because Python imported the package.

The package remains neutral because the same workbench can be vendored into
separately published ontology projects.
"""
from __future__ import annotations

import importlib

__all__ = ["frontmatter", "mathtext", "paths", "rendering", "tokens"]


def __getattr__(name: str):
    if name in __all__:
        module = importlib.import_module(f"{__name__}.{name}")
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
