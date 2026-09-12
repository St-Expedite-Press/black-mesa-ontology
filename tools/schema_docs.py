#!/usr/bin/env python3
"""Generate structural Markdown documentation from the Black Mesa Turtle schema.

Usage:
    python tools/schema_docs.py --schema schema --out docs

The generator deliberately documents structure, not narrative architecture.
Hand-written design rationale lives in docs/architecture.md and
docs/team-guide.md.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS, OWL

BMO = rdflib.Namespace("https://w3id.org/black-mesa/bmo/")
UP = rdflib.Namespace("https://w3id.org/black-mesa/upper/")


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
    classes = sorted(
        {s for s in g.subjects(RDF.type, OWL.Class) if local(s)}, key=str
    )
    object_props = sorted(
        {s for s in g.subjects(RDF.type, OWL.ObjectProperty) if local(s)}, key=str
    )
    datatype_props = sorted(
        {s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if local(s)}, key=str
    )

    out: list[str] = [
        "<!-- GENERATED FILE — rebuild with: python tools/schema_docs.py --schema schema --out docs -->",
        "",
        "# Schema reference",
        "",
        "Structural reference generated directly from the Turtle schema. For product meaning and rationale, read architecture.md and team-guide.md.",
        "",
        f"**{len(classes)} local classes · {len(object_props)} object properties · {len(datatype_props)} datatype properties**",
        "",
        "## Classes",
        "",
        "| Class | Parent(s) | Meaning |",
        "|---|---|---|",
    ]

    for cls in classes:
        parents = sorted(g.objects(cls, RDFS.subClassOf), key=str)
        parent_text = ", ".join(qname(g, p) for p in parents) or "—"
        meaning = comment(g, cls).replace("\n", " ").replace("|", "\\|")
        out.append(f"| [{qname(g,cls)}](#{anchor(qname(g,cls))}) | {parent_text} | {meaning} |")

    out += ["", "## Object properties", "", "| Property | Domain | Range | Meaning |", "|---|---|---|---|"]
    for prop in object_props:
        dom = first(g, prop, RDFS.domain)
        ran = first(g, prop, RDFS.range)
        meaning = comment(g, prop).replace("\n", " ").replace("|", "\\|")
        out.append(
            f"| {qname(g,prop)} | {qname(g,dom)} | {qname(g,ran)} | {meaning} |"
        )

    out += ["", "## Datatype properties", "", "| Property | Domain | Range | Meaning |", "|---|---|---|---|"]
    for prop in datatype_props:
        dom = first(g, prop, RDFS.domain)
        ran = first(g, prop, RDFS.range)
        meaning = comment(g, prop).replace("\n", " ").replace("|", "\\|")
        out.append(
            f"| {qname(g,prop)} | {qname(g,dom)} | {qname(g,ran)} | {meaning} |"
        )

    out += ["", "## Detailed class definitions", ""]
    for cls in classes:
        out += [
            f"### {qname(g,cls)}",
            "",
            f"**{label(g, cls)}**",
            "",
            comment(g, cls),
            "",
        ]

    return "\n".join(out).rstrip() + "\n"


def generate_diagram(g: rdflib.Graph) -> str:
    classes = sorted(
        {s for s in g.subjects(RDF.type, OWL.Class) if local(s)}, key=str
    )
    object_props = sorted(
        {s for s in g.subjects(RDF.type, OWL.ObjectProperty) if local(s)}, key=str
    )

    out: list[str] = [
        "<!-- GENERATED FILE — rebuild with: python tools/schema_docs.py --schema schema --out docs -->",
        "",
        "# Class diagrams",
        "",
        "These diagrams are generated from the current Turtle schema. The hand-written system diagrams in architecture.md explain the product workflow; these show the declared ontology structure.",
        "",
        "## Local subclass hierarchy",
        "",
        "~~~mermaid",
        "graph TD",
    ]

    for cls in classes:
        cid = node_id(cls)
        out.append(f'  {cid}["{qname(g, cls)}"]')
        for parent in sorted(g.objects(cls, RDFS.subClassOf), key=str):
            if local(parent):
                pid = node_id(parent)
                out.append(f'  {pid}["{qname(g, parent)}"] --> {cid}')

    out += ["~~~", "", "## Core relation graph", "", "~~~mermaid", "graph LR"]

    for prop in object_props:
        dom = first(g, prop, RDFS.domain)
        ran = first(g, prop, RDFS.range)
        if dom is None or ran is None:
            continue
        did = node_id(dom)
        rid = node_id(ran)
        out.append(f'  {did}["{qname(g, dom)}"]')
        out.append(f'  {rid}["{qname(g, ran)}"]')
        out.append(f'  {did} -->|"{qname(g, prop)}"| {rid}')

    out += ["~~~", ""]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=Path("schema"))
    parser.add_argument("--out", type=Path, default=Path("docs"))
    args = parser.parse_args()

    g = load_schema(args.schema)
    args.out.mkdir(parents=True, exist_ok=True)

    (args.out / "schema-reference.md").write_text(
        generate_reference(g), encoding="utf-8"
    )
    (args.out / "class-diagram.md").write_text(
        generate_diagram(g), encoding="utf-8"
    )

    print(f"Generated docs from {len(g)} schema triples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
