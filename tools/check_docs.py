#!/usr/bin/env python
"""Validate active project Markdown links, fences, examples, and ontology terms.

This complements the house document linter with repository-wide checks. It is
deliberately dependency-light and does not claim to render Mermaid; it checks
that Mermaid blocks use a supported diagram declaration and balanced brackets.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import rdflib

import _bootstrap  # noqa: F401
from workbench.paths import REPO_ROOT

LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
FENCE = re.compile(r"^```([\w+-]*)\s*$")
TERM = re.compile(r"`((?:bmo|eios|rle|get|up):[A-Za-z][A-Za-z0-9_-]*)`")
PREFIX = {
    "bmo": "https://example.org/bmo/",
    "eios": "https://example.org/eios/",
    "rle": "https://example.org/rle/",
    "get": "https://example.org/get/",
    "up": "https://example.org/upper/",
}
MERMAID_START = ("flowchart ", "graph ", "classDiagram", "sequenceDiagram", "stateDiagram", "erDiagram", "gantt", "timeline")


def blocks(text: str):
    language = None
    body: list[str] = []
    start = 0
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if match:
            if language is None:
                language = match.group(1).lower()
                body = []
                start = number
            else:
                yield language, "\n".join(body), start
                language = None
            continue
        if language is not None:
            body.append(line)
    if language is not None:
        raise ValueError(f"unclosed code fence opened at line {start}")


def ontology_terms(schema: Path, root: Path) -> set[str]:
    graph = rdflib.Graph()
    for path in sorted(schema.glob("*.ttl")):
        graph.parse(path, format="turtle")
    for upper in (REPO_ROOT / "upper" / "upper-core.ttl", root / "upper" / "upper-core.ttl"):
        if upper.is_file():
            graph.parse(upper, format="turtle")
    return {str(node) for node in graph.all_nodes() if isinstance(node, rdflib.URIRef)}


def validate(root: Path, schema: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "README.md").is_file() or not (root / "docs").is_dir():
        return [f"{root}: expected README.md and docs/; refusing a vacuous pass"]
    if not schema.is_dir():
        return [f"{schema}: schema directory does not exist"]
    terms = ontology_terms(schema, root)
    paths = [root / "README.md"] + sorted((root / "docs").rglob("*.md"))
    paths = [p for p in paths if p.is_file() and "archive" not in p.parts]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        for target in LINK.findall(text):
            clean = target.strip().split("#", 1)[0]
            if not clean or clean.startswith(("http://", "https://", "mailto:")):
                continue
            if not (path.parent / clean).resolve().exists():
                errors.append(f"{rel}: broken relative link {target}")
        try:
            fenced = list(blocks(text))
        except ValueError as exc:
            errors.append(f"{rel}: {exc}")
            fenced = []
        for language, body, line in fenced:
            if language == "json":
                try:
                    json.loads(body)
                except json.JSONDecodeError as exc:
                    errors.append(f"{rel}:{line}: invalid JSON example: {exc.msg}")
            elif language in {"turtle", "ttl"}:
                try:
                    rdflib.Graph().parse(data=body, format="turtle")
                except Exception as exc:  # rdflib uses several parser exceptions
                    errors.append(f"{rel}:{line}: invalid Turtle example: {exc}")
            elif language == "sparql":
                try:
                    from rdflib.plugins.sparql.parser import parseQuery
                    parseQuery(body)
                except Exception as exc:
                    errors.append(f"{rel}:{line}: invalid SPARQL example: {exc}")
            elif language == "mermaid":
                first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
                if not first.startswith(MERMAID_START):
                    errors.append(f"{rel}:{line}: unsupported Mermaid declaration {first!r}")
                for left, right in (("[", "]"), ("{", "}"), ("(", ")")):
                    if body.count(left) != body.count(right):
                        errors.append(f"{rel}:{line}: unbalanced Mermaid {left}{right}")
        for qname in TERM.findall(text):
            prefix, local = qname.split(":", 1)
            if PREFIX[prefix] + local not in terms:
                errors.append(f"{rel}: documented ontology term does not exist: {qname}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--schema", type=Path, default=None)
    parser.add_argument("--project", default=None,
                        help="canonical project directory name; autodetected in a flat assembly")
    args = parser.parse_args()
    canonical = (REPO_ROOT / "projects" / args.project
                 if args.project else REPO_ROOT / "projects" / "guis-ecosystem-typology")
    root = args.root or (canonical if canonical.is_dir() else REPO_ROOT)
    schema = args.schema or root / "schema"
    errors = validate(root.resolve(), schema.resolve())
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"FAIL: {len(errors)} documentation error(s)")
        return 1
    print("PASS: active documentation links, fences, examples, and ontology terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
