"""YAML frontmatter parsing, defined once.

Three tools previously carried their own copy of this regex and their own
interpretation of what counts as valid frontmatter. When the linter and the
renderer disagree about that, a document passes lint and then renders wrongly.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)

REQUIRED_KEYS = ("title", "style")
KNOWN_KEYS = {
    "title", "subtitle", "kicker", "doc_id", "style", "meta", "footer",
    "authors", "date", "version",
}


@dataclass
class Document:
    """A Markdown document split into its frontmatter and body."""

    path: Path
    meta: dict = field(default_factory=dict)
    body: str = ""
    raw: str = ""

    @property
    def has_frontmatter(self) -> bool:
        return bool(self.meta) or self.raw.startswith("---")

    @property
    def style(self) -> str:
        return str(self.meta.get("style", "report"))

    @property
    def title(self) -> str:
        return str(self.meta.get("title") or self.path.stem)

    def missing_required(self) -> list[str]:
        return [k for k in REQUIRED_KEYS if not self.meta.get(k)]

    def unknown_keys(self) -> list[str]:
        return sorted(k for k in self.meta if k not in KNOWN_KEYS)


class FrontmatterError(ValueError):
    """Frontmatter present but not parseable."""


def split(text: str) -> tuple[dict, str]:
    """Split raw text into (metadata, body). No frontmatter yields ({}, text)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise FrontmatterError(str(exc)) from exc
    if not isinstance(meta, dict):
        raise FrontmatterError("frontmatter must be a mapping")
    return meta, text[match.end():]


def load(path: Path) -> Document:
    """Read a Markdown file and split it."""
    raw = path.read_text(encoding="utf-8")
    meta, body = split(raw)
    return Document(path=path, meta=meta, body=body, raw=raw)


def is_document(path: Path) -> bool:
    """True if the file carries frontmatter declaring a style.

    This is what separates an authored document from a converted source, a
    README, or a note: documents declare how they are to be rendered.
    """
    try:
        meta, _ = split(path.read_text(encoding="utf-8"))
    except (FrontmatterError, OSError, UnicodeDecodeError):
        return False
    return bool(meta.get("style"))
