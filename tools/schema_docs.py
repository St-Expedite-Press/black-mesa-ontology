#!/usr/bin/env python3
"""Generate structural Markdown documentation from Black Mesa Turtle sources."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

MARKER = "<!-- GENERATED FILE — DO NOT EDIT BY HAND. Rebuild with: python tools/schema_docs.py --schema schema --out docs/reference -->"


@dataclass(frozen=True)
class Term:
    term: str
    kind: str
    label: str
    comment: str
    parent: str = "—"
    domain: str = "—"
    range: str = "—"


def parse_terms(text: str) -> list[Term]:
    lines = text.splitlines()
    out: list[Term] = []
    i = 0
    start = re.compile(r"^(bmo:\w+)\s+a\s+owl:(Class|ObjectProperty|DatatypeProperty)\s*;")
    while i < len(lines):
        match = start.match(lines[i])
        if not match:
            i += 1
            continue
        buf = [lines[i]]
        while not buf[-1].rstrip().endswith(".") and i + 1 < len(lines):
            i += 1
            buf.append(lines[i])
        block = "\n".join(buf)
        label_m = re.search(r'rdfs:label\s+"([^"]+)"', block)
        comment_m = re.search(r'rdfs:comment\s+"([^"]+)"', block)
        parent_m = re.search(r"rdfs:subClassOf\s+([^;]+)\s*;", block)
        domain_m = re.search(r"rdfs:domain\s+([^;\s]+)\s*;", block)
        range_m = re.search(r"rdfs:range\s+([^;\s.]+)(?:\s*[;.])", block)
        out.append(Term(
            term=match.group(1),
            kind=match.group(2),
            label=label_m.group(1) if label_m else match.group(1),
            comment=comment_m.group(1) if comment_m else "_No description supplied._",
            parent=parent_m.group(1).strip() if parent_m else "—",
            domain=domain_m.group(1) if domain_m else "—",
            range=range_m.group(1) if range_m else "—",
        ))
        i += 1
    return out


def anchor(text: str) -> str:
    return re.sub(r"[:_ ]", "-", text.lower())


def node(text: str) -> str:
    return "n_" + re.sub(r"\W", "_", text)


def esc(text: str) -> str:
    return text.replace("\n", " ").replace("|", "\\|")


def generate_reference(terms: list[Term]) -> str:
    classes = sorted((x for x in terms if x.kind == "Class"), key=lambda x: x.term)
    ops = sorted((x for x in terms if x.kind == "ObjectProperty"), key=lambda x: x.term)
    dps = sorted((x for x in terms if x.kind == "DatatypeProperty"), key=lambda x: x.term)
    out = [
        MARKER, "", "# Schema reference", "",
        "Structural reference generated directly from Turtle. For conceptual guidance, read [modeling principles](../model/modeling-principles.md) and [evidence chain](../model/evidence-chain.md).",
        "", f"**{len(classes)} local classes · {len(ops)} object properties · {len(dps)} datatype properties**",
        "", "## Classes", "", "| Class | Parent(s) | Meaning |", "|---|---|---|",
    ]
    out += [f"| [{x.term}](#{anchor(x.term)}) | {x.parent} | {esc(x.comment)} |" for x in classes]
    out += ["", "## Object properties", "", "| Property | Domain | Range | Meaning |", "|---|---|---|---|"]
    out += [f"| {x.term} | {x.domain} | {x.range} | {esc(x.comment)} |" for x in ops]
    out += ["", "## Datatype properties", "", "| Property | Domain | Range | Meaning |", "|---|---|---|---|"]
    out += [f"| {x.term} | {x.domain} | {x.range} | {esc(x.comment)} |" for x in dps]
    out += ["", "## Detailed class definitions", ""]
    for x in classes:
        out += [f"### {x.term}", "", f"**{x.label}**", "", x.comment, ""]
    return "\n".join(out).rstrip() + "\n"


def generate_diagram(terms: list[Term]) -> str:
    classes = sorted((x for x in terms if x.kind == "Class"), key=lambda x: x.term)
    ops = sorted((x for x in terms if x.kind == "ObjectProperty"), key=lambda x: x.term)
    out = [
        MARKER, "", "# Class diagrams", "",
        "These diagrams are generated from the current Turtle schema. For product workflow and rationale, read [system architecture](../overview/system-architecture.md) and [evidence chain](../model/evidence-chain.md).",
        "", "## Local subclass hierarchy", "", "~~~mermaid", "graph TD",
    ]
    for x in classes:
        out.append(f'  {node(x.term)}["{x.term}"]')
        for parent in (p.strip() for p in x.parent.split(",")):
            if parent.startswith("bmo:"):
                out.append(f'  {node(parent)}["{parent}"] --> {node(x.term)}')
    out += ["~~~", "", "## Core relation graph", "", "~~~mermaid", "graph LR"]
    for x in ops:
        if x.domain == "—" or x.range == "—":
            continue
        out += [
            f'  {node(x.domain)}["{x.domain}"]',
            f'  {node(x.range)}["{x.range}"]',
            f'  {node(x.domain)} -->|"{x.term}"| {node(x.range)}',
        ]
    out += ["~~~", ""]
    return "\n".join(out)


def generate_shacl_reference(text: str) -> str:
    block_re = re.compile(r"^(bmo:\w+Shape)\s+a\s+sh:NodeShape\s*;(.*?)(?=^bmo:\w+Shape\s+a\s+sh:NodeShape\s*;|\Z)", re.M | re.S)
    out = [MARKER, "", "# SHACL reference", "", "Generated from `schema/shapes.ttl`. This is a structural index of current validation messages; [validation and CI](../operations/validation-and-ci.md) explains what the constraints do and do not prove.", ""]
    for name, body in block_re.findall(text):
        target_m = re.search(r"sh:targetClass\s+([^\s;]+)", body)
        target = target_m.group(1) if target_m else "— nested/node shape"
        messages = re.findall(r'sh:message\s+"([^"]+)"', body)
        out += [f"## `{name}`", "", f"**Target:** `{target}`", ""]
        if messages:
            out += ["Validation messages:", ""]
            out += [f"- {msg}" for msg in messages]
        else:
            out += ["_No human-readable sh:message found._"]
        out += [""]
    return "\n".join(out).rstrip() + "\n"


def generate_namespace_reference(core: str) -> str:
    version_m = re.search(r'owl:versionInfo\s+"([^"]+)"', core)
    version_iri_m = re.search(r"owl:versionIRI\s+<([^>]+)>", core)
    version = version_m.group(1) if version_m else "unknown"
    version_iri = version_iri_m.group(1) if version_iri_m else "unknown"
    return f"""{MARKER}

# Namespace reference

Generated from current ontology identity declarations.

| Purpose | Identifier |
|---|---|
| core ontology | `https://w3id.org/black-mesa/bmo` |
| core term namespace | `https://w3id.org/black-mesa/bmo/` |
| current core version | `{version}` |
| current version IRI | `{version_iri}` |
| upper ontology | `https://w3id.org/black-mesa/upper` |
| upper term namespace | `https://w3id.org/black-mesa/upper/` |
| reference-data base | `https://w3id.org/black-mesa/reference/` |
| rule-record base | `https://w3id.org/black-mesa/rules/` |
| authority base | `https://w3id.org/black-mesa/authority/` |
| example base | `https://w3id.org/black-mesa/example/` |

Public HTTP resolution is a deployment concern distinct from these RDF declarations. See [persistent identifiers](../governance/persistent-identifiers.md).
"""


def generate_index() -> str:
    return f"""{MARKER}

# Generated reference

These files are derived from current schema and SHACL. Do not edit them by hand.

- [Schema reference](schema-reference.md) — local classes and properties.
- [Class diagrams](class-diagram.md) — subclass and relation graphs.
- [SHACL reference](shacl-reference.md) — validation targets/messages.
- [Namespace reference](namespace-reference.md) — current ontology identity.

For conceptual explanation, start with [modeling principles](../model/modeling-principles.md) and [evidence chain](../model/evidence-chain.md).
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=Path("schema"))
    parser.add_argument("--out", type=Path, default=Path("docs/reference"))
    args = parser.parse_args()
    source_files = [p for p in sorted(args.schema.glob("*.ttl")) if p.name != "shapes.ttl"]
    source = "\n".join(p.read_text(encoding="utf-8") for p in source_files)
    core = (args.schema / "bmo-core.ttl").read_text(encoding="utf-8")
    shapes = (args.schema / "shapes.ttl").read_text(encoding="utf-8")
    terms = parse_terms(source)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "README.md").write_text(generate_index(), encoding="utf-8")
    (args.out / "schema-reference.md").write_text(generate_reference(terms), encoding="utf-8")
    (args.out / "class-diagram.md").write_text(generate_diagram(terms), encoding="utf-8")
    (args.out / "shacl-reference.md").write_text(generate_shacl_reference(shapes), encoding="utf-8")
    (args.out / "namespace-reference.md").write_text(generate_namespace_reference(core), encoding="utf-8")
    print(f"Generated documentation for {len(terms)} declared local schema terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
