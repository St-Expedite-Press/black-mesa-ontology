#!/usr/bin/env python3
"""Generate structural Markdown documentation from the Black Mesa schema."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS

BMO = rdflib.Namespace("https://w3id.org/black-mesa/bmo/")
UP = rdflib.Namespace("https://w3id.org/black-mesa/upper/")
MARKER = "<!-- GENERATED FILE — DO NOT EDIT BY HAND. Rebuild with: python tools/schema_docs.py --schema schema --out docs/reference -->"


def load_schema(schema_dir: Path) -> rdflib.Graph:
    g = rdflib.Graph()
    g.bind("bmo", BMO)
    g.bind("up", UP)
    for path in sorted(schema_dir.glob("*.ttl")):
        if path.name == "shapes.ttl":
            continue
        g.parse(path, format="turtle")
    return g


def qname(g: rdflib.Graph, term) -> str:
    if term is None:
        return "—"
    try:
        return g.namespace_manager.qname(term)
    except Exception:
        return str(term)


def local(term) -> bool:
    return str(term).startswith(str(BMO))


def label(g: rdflib.Graph, term) -> str:
    value = next(iter(g.objects(term, RDFS.label)), None)
    return str(value) if value is not None else qname(g, term)


def comment(g: rdflib.Graph, term) -> str:
    value = next(iter(g.objects(term, RDFS.comment)), None)
    return str(value) if value is not None else "_No description supplied._"


def first(g: rdflib.Graph, subject, predicate):
    return next(iter(g.objects(subject, predicate)), None)


def anchor(text: str) -> str:
    return text.lower().replace(":", "-").replace("_", "-").replace(" ", "-")


def node_id(uri) -> str:
    return "n" + hashlib.sha1(str(uri).encode("utf-8")).hexdigest()[:10]


def generate_reference(g: rdflib.Graph) -> str:
    classes = sorted({s for s in g.subjects(RDF.type, OWL.Class) if local(s)}, key=str)
    object_props = sorted({s for s in g.subjects(RDF.type, OWL.ObjectProperty) if local(s)}, key=str)
    datatype_props = sorted({s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if local(s)}, key=str)
    out = [
        MARKER, "", "# Schema reference", "",
        "Structural reference generated directly from Turtle. For conceptual guidance, read [modeling principles](../model/modeling-principles.md) and [evidence chain](../model/evidence-chain.md).",
        "", f"**{len(classes)} local classes · {len(object_props)} object properties · {len(datatype_props)} datatype properties**",
        "", "## Classes", "", "| Class | Parent(s) | Meaning |", "|---|---|---|",
    ]
    for cls in classes:
        parents = sorted(g.objects(cls, RDFS.subClassOf), key=str)
        parent_text = ", ".join(qname(g, p) for p in parents) or "—"
        meaning = comment(g, cls).replace("\n", " ").replace("|", "\\|")
        out.append(f"| [{qname(g,cls)}](#{anchor(qname(g,cls))}) | {parent_text} | {meaning} |")
    out += ["", "## Object properties", "", "| Property | Domain | Range | Meaning |", "|---|---|---|---|"]
    for prop in object_props:
        meaning = comment(g, prop).replace("\n", " ").replace("|", "\\|")
        out.append(f"| {qname(g,prop)} | {qname(g,first(g,prop,RDFS.domain))} | {qname(g,first(g,prop,RDFS.range))} | {meaning} |")
    out += ["", "## Datatype properties", "", "| Property | Domain | Range | Meaning |", "|---|---|---|---|"]
    for prop in datatype_props:
        meaning = comment(g, prop).replace("\n", " ").replace("|", "\\|")
        out.append(f"| {qname(g,prop)} | {qname(g,first(g,prop,RDFS.domain))} | {qname(g,first(g,prop,RDFS.range))} | {meaning} |")
    out += ["", "## Detailed class definitions", ""]
    for cls in classes:
        out += [f"### {qname(g,cls)}", "", f"**{label(g, cls)}**", "", comment(g, cls), ""]
    return "\n".join(out).rstrip() + "\n"


def generate_diagram(g: rdflib.Graph) -> str:
    classes = sorted({s for s in g.subjects(RDF.type, OWL.Class) if local(s)}, key=str)
    object_props = sorted({s for s in g.subjects(RDF.type, OWL.ObjectProperty) if local(s)}, key=str)
    out = [
        MARKER, "", "# Class diagrams", "",
        "These diagrams are generated from the current Turtle schema. For product workflow and rationale, read [system architecture](../overview/system-architecture.md) and [evidence chain](../model/evidence-chain.md).",
        "", "## Local subclass hierarchy", "", "~~~mermaid", "graph TD",
    ]
    for cls in classes:
        cid = node_id(cls)
        out.append(f'  {cid}["{qname(g, cls)}"]')
        for parent in sorted(g.objects(cls, RDFS.subClassOf), key=str):
            if local(parent):
                out.append(f'  {node_id(parent)}["{qname(g, parent)}"] --> {cid}')
    out += ["~~~", "", "## Core relation graph", "", "~~~mermaid", "graph LR"]
    for prop in object_props:
        dom, ran = first(g, prop, RDFS.domain), first(g, prop, RDFS.range)
        if dom is None or ran is None:
            continue
        out += [f'  {node_id(dom)}["{qname(g, dom)}"]', f'  {node_id(ran)}["{qname(g, ran)}"]', f'  {node_id(dom)} -->|"{qname(g, prop)}"| {node_id(ran)}']
    out += ["~~~", ""]
    return "\n".join(out)


def generate_shacl_reference(text: str) -> str:
    block_re = re.compile(r"^(bmo:\\w+Shape)\\s+a\\s+sh:NodeShape\\s*;(.*?)(?=^bmo:\\w+Shape\\s+a\\s+sh:NodeShape\\s*;|\\Z)", re.M | re.S)
    out = [MARKER, "", "# SHACL reference", "", "Generated from `schema/shapes.ttl`. This is a structural index of current validation messages; [validation and CI](../operations/validation-and-ci.md) explains what the constraints do and do not prove.", ""]
    for name, body in block_re.findall(text):
        target_match = re.search(r"sh:targetClass\s+([^\s;]+)", body)
        target = target_match.group(1) if target_match else "— nested/node shape"
        messages = re.findall(r'sh:message\s+"([^"]+)"', body)
        out += [f"## `{name}`", "", f"**Target:** `{target}`", ""]
        if messages:
            out += ["Validation messages:", ""]
            out += [f"- {msg}" for msg in messages]
        else:
            out += ["_No human-readable sh:message found._"]
        out += [""]
    return "\n".join(out).rstrip() + "\n"


def generate_namespace_reference(g: rdflib.Graph) -> str:
    ont = rdflib.URIRef("https://w3id.org/black-mesa/bmo")
    version = next(iter(g.objects(ont, OWL.versionInfo)), "unknown")
    version_iri = next(iter(g.objects(ont, OWL.versionIRI)), "unknown")
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
    g = load_schema(args.schema)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "README.md").write_text(generate_index(), encoding="utf-8")
    (args.out / "schema-reference.md").write_text(generate_reference(g), encoding="utf-8")
    (args.out / "class-diagram.md").write_text(generate_diagram(g), encoding="utf-8")
    shapes_text = (args.schema / "shapes.ttl").read_text(encoding="utf-8")
    (args.out / "shacl-reference.md").write_text(generate_shacl_reference(shapes_text), encoding="utf-8")
    (args.out / "namespace-reference.md").write_text(generate_namespace_reference(g), encoding="utf-8")
    print(f"Generated documentation from {len(g)} schema triples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
