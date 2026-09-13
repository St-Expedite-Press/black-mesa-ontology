#!/usr/bin/env python3
"""Validate Black Mesa's GitHub-native documentation corpus."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
    ROOT / "README.md",
    ROOT / "CLAUDE.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "CHANGELOG.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "reference" / "README.md",
    ROOT / "docs" / "reference" / "schema-reference.md",
    ROOT / "docs" / "reference" / "class-diagram.md",
    ROOT / "docs" / "reference" / "shacl-reference.md",
    ROOT / "docs" / "reference" / "namespace-reference.md",
)

DELETED_DOCS = (
    "docs/architecture.md",
    "docs/team-guide.md",
    "docs/persistence.md",
    "docs/detection-ontology-v0.2.md",
    "docs/detection-ontology-v0.3.md",
    "docs/detection-ontology-v0.4.md",
    "docs/schema-reference.md",
    "docs/class-diagram.md",
)

FORBIDDEN_NS = (
    "https://" + "example.org/bmo/",
    "https://" + "example.org/upper/",
)

GENERATED_MARKER = "GENERATED FILE — DO NOT EDIT BY HAND"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    files = [ROOT / name for name in ("README.md", "CLAUDE.md", "CONTRIBUTING.md", "CHANGELOG.md")]
    for dirname in ("docs", "reference", "rules"):
        files.extend(sorted((ROOT / dirname).glob("**/*.md")))
    return [p for p in files if p.is_file()]


def main() -> int:
    issues: list[str] = []

    for path in REQUIRED:
        if not path.is_file():
            issues.append(f"missing required documentation: {path.relative_to(ROOT)}")

    docs = markdown_files()
    for path in docs:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for old in DELETED_DOCS:
            if old in text:
                issues.append(f"{rel}: references retired document {old}")
        for old_ns in FORBIDDEN_NS:
            if old_ns in text:
                issues.append(f"{rel}: contains deprecated namespace {old_ns}")

        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                issues.append(f"{rel}: local link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                issues.append(f"{rel}: broken local link -> {raw_target}")


    core = (ROOT / "schema" / "bmo-core.ttl").read_text(encoding="utf-8")
    version_m = re.search(r'owl:versionInfo\\s+"([^"]+)"', core)
    version_iri_m = re.search(r"owl:versionIRI\\s+<([^>]+)>", core)
    if not version_m or not version_iri_m:
        issues.append("schema/bmo-core.ttl: cannot resolve owl:versionInfo/versionIRI for documentation checks")
    else:
        version = version_m.group(1)
        version_iri = version_iri_m.group(1)
        for relpath in (
            "README.md",
            "docs/governance/persistent-identifiers.md",
            "docs/governance/releases-and-versioning.md",
        ):
            path = ROOT / relpath
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if version not in text:
                issues.append(f"{relpath}: does not advertise current ontology version {version}")
            if version_iri not in text:
                issues.append(f"{relpath}: does not advertise current version IRI {version_iri}")

    for path in (ROOT / "docs" / "reference").glob("*.md"):
        if GENERATED_MARKER not in path.read_text(encoding="utf-8"):
            issues.append(f"{path.relative_to(ROOT)}: missing generated-file marker")

    if issues:
        print("Documentation validation failed:")
        for issue in issues:
            print(" -", issue)
        return 1
    print(f"Documentation validation PASS ({len(docs)} Markdown files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
