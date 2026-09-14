#!/usr/bin/env python
"""Generate Markdown reference documentation from a schema directory.

WHY GENERATED RATHER THAN WRITTEN

The schema already carries its own documentation: every class and property has
an rdfs:comment saying what it is for and, where a modelling choice was
contested, what the alternative was. Those comments are the argument. Writing a
second prose copy of them by hand produces two sources of truth, and the one
that drifts is always the prose - it is the copy nobody validates.

So this reads the Turtle and emits Markdown. A term added without a comment
shows up here as a gap, which is a useful pressure. Regenerate rather than
edit; validate_ontology.py fails on an undeclared term and the linter fails on
a term with no label.

WHAT IT EMITS

  schema-reference.md   every class and property, with its BFO anchor, its
                        domain and range, and its comment in full; the
                        controlled vocabularies with their members; the SHACL
                        constraints with the message each one fails with, which
                        is where most of the reasoning lives
  class-diagram.md      Mermaid class and hierarchy diagrams, rendered natively
                        by GitHub - no image files, no build step, and the
                        source diffs as text
  ontology-classes.md   compact generated class index
  ontology-properties.md compact generated property index
  shapes.md             compact generated SHACL shape index

Usage:
    python tools/schema_docs.py --schema projects/<p>/schema --out projects/<p>/docs
    python tools/schema_docs.py --schema schema --out docs          # published layout
"""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS, SKOS, Namespace

import _bootstrap  # noqa: F401
from workbench.paths import relative
from validate_ontology import resolve_imports

UP = Namespace("https://example.org/upper/")
SH = Namespace("http://www.w3.org/ns/shacl#")
DCT = Namespace("http://purl.org/dc/terms/")
LOCAL = "https://example.org/"
BFO = "http://purl.obolibrary.org/obo/BFO_"

#: The answers the anchoring question has, in the repository's own words:
#: "is it information, a process, matter, a place, a quality, or a role?"
#:
#: Keyed on both the upper module's category and the BFO or IAO class beneath
#: it, so a class anchored either way resolves to the same readable answer.
#: Raw BFO numerics are accurate and unreadable, and a reference nobody can
#: skim is a reference nobody reads.
KIND_OF_THING = {
    # information
    "https://example.org/upper/InformationArtifact": "information",
    "http://purl.obolibrary.org/obo/IAO_0000030": "information",
    "http://purl.obolibrary.org/obo/IAO_0000027": "information",
    "http://purl.obolibrary.org/obo/IAO_0000033": "information",
    "http://purl.obolibrary.org/obo/IAO_0000109": "information",
    "http://purl.obolibrary.org/obo/IAO_0000007": "information",
    "http://purl.obolibrary.org/obo/IAO_0000005": "information",
    "http://purl.obolibrary.org/obo/BFO_0000031": "information",
    # process
    "https://example.org/upper/RecordedProcess": "process",
    "http://purl.obolibrary.org/obo/BFO_0000015": "process",
    "http://purl.obolibrary.org/obo/BFO_0000003": "process",
    # matter
    "https://example.org/upper/OccurrentAggregate": "matter (object aggregate)",
    "http://purl.obolibrary.org/obo/BFO_0000027": "matter (object aggregate)",
    "http://purl.obolibrary.org/obo/BFO_0000030": "matter (object)",
    "http://purl.obolibrary.org/obo/BFO_0000040": "matter",
    # place
    "https://example.org/upper/SurveyedSite": "place (site)",
    "http://purl.obolibrary.org/obo/BFO_0000029": "place (site)",
    # quality, role, disposition
    "https://example.org/upper/Condition": "quality",
    "http://purl.obolibrary.org/obo/BFO_0000019": "quality",
    "https://example.org/upper/EvidentialRole": "role",
    "http://purl.obolibrary.org/obo/BFO_0000023": "role",
    "https://example.org/upper/Capability": "disposition",
    "http://purl.obolibrary.org/obo/BFO_0000016": "disposition",
    "http://purl.obolibrary.org/obo/BFO_0000017": "disposition",
}


#: Files that declare instance DATA rather than schema. A worked example and a
#: generated taxonomy both populate the schema; neither defines it, and mixing
#: the two turns the reference into a data dump. `up:ConceptualUnit` otherwise
#: appears as a 145-member "controlled vocabulary" - which is the GET taxonomy,
#: real and useful and not a vocabulary this schema defines.
DATA_FILES = ("examples-", "get-core")


def is_data_file(path: Path) -> bool:
    return any(path.name.startswith(p) or p in path.name for p in DATA_FILES)


def load(schema: Path) -> tuple[rdflib.Graph, set]:
    """The schema graph plus the set of subjects declared in schema files.

    Provenance is tracked per file because the distinction between a term the
    schema defines and an individual some example happens to create is not
    visible in the merged graph, and the reference needs it.
    """
    g = rdflib.Graph()
    schema_subjects: set = set()
    loaded: set[Path] = set()
    for ttl in sorted(schema.glob("*.ttl")):
        before = set(g.subjects())
        g.parse(ttl, format="turtle")
        loaded.add(ttl.resolve())
        if not is_data_file(ttl):
            schema_subjects |= set(g.subjects()) - before
    resolve_imports(g, loaded)
    # The upper module is schema too, and it arrives through the import closure
    # rather than the directory listing.
    for path in loaded:
        if path.name == "upper-core.ttl":
            schema_subjects |= set(rdflib.Graph().parse(
                path, format="turtle").subjects())
    return g, schema_subjects


def qn(g: rdflib.Graph, t) -> str:
    try:
        return g.namespace_manager.qname(t)
    except Exception:
        return str(t)


def one(g: rdflib.Graph, s, p) -> str | None:
    for o in g.objects(s, p):
        # RDF literals can retain source-file line endings. Normalize them
        # before Markdown generation so Windows and Linux produce identical
        # committed references.
        return str(o).replace("\r\n", "\n").replace("\r", "\n")
    return None


def is_local(t) -> bool:
    return str(t).startswith(LOCAL)


def anchor_of(g: rdflib.Graph, cls) -> str:
    """What kind of thing this class is, from the nearest recognised ancestor.

    Breadth-first, so the closest answer wins: every information artifact also
    reaches BFO's generically dependent continuant, and reporting the nearest
    category is what makes the summary table skimmable.
    """
    seen, frontier = {cls}, [cls]
    while frontier:
        nxt = []
        for node in frontier:
            for parent in g.objects(node, RDFS.subClassOf):
                if isinstance(parent, rdflib.BNode) or parent in seen:
                    continue
                if (kind := KIND_OF_THING.get(str(parent))):
                    return kind
                seen.add(parent)
                nxt.append(parent)
        frontier = nxt
    return "unanchored"


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n\n", "<br><br>").replace("\n", " ")


def anchor_id(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def classes_of(g: rdflib.Graph) -> list:
    return sorted((c for c in set(g.subjects(RDF.type, OWL.Class))
                   if is_local(c) and not isinstance(c, rdflib.BNode)), key=str)


def properties_of(g: rdflib.Graph) -> list:
    props = set()
    for t in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty,
              RDF.Property):
        props |= set(g.subjects(RDF.type, t))
    return sorted((p for p in props if is_local(p)
                   and not isinstance(p, rdflib.BNode)), key=str)


def domain_range(g: rdflib.Graph, p) -> tuple[str, str]:
    def render(pred):
        parts = []
        for o in g.objects(p, pred):
            if isinstance(o, rdflib.BNode):
                # A union domain: the members are what the reader wants.
                members = []
                for lst in g.objects(o, OWL.unionOf):
                    members = [qn(g, m) for m in rdflib.collection.Collection(g, lst)]
                parts.append(" or ".join(members) if members else "(anonymous)")
            else:
                parts.append(qn(g, o))
        return ", ".join(parts) or "-"
    return render(RDFS.domain), render(RDFS.range)


def vocabularies(g: rdflib.Graph, schema_subjects: set) -> dict:
    """Classes whose instances form a controlled vocabulary, with members.

    The house pattern for an enumeration is a class plus individuals declared
    beside it - rle:RiskCategory with CR/EN/VU, eios:OriginKind with Natural
    and Constructed. Only individuals the SCHEMA declares count: an individual
    created by a worked example is data, and counting it turns this section
    into a dump of every proposed unit and assessment outcome in the
    repository.
    """
    out: dict = defaultdict(list)
    for cls in classes_of(g):
        for inst in sorted(g.subjects(RDF.type, cls), key=str):
            if (is_local(inst) and inst in schema_subjects
                    and (inst, RDF.type, OWL.Class) not in g):
                out[cls].append(inst)
    return {k: v for k, v in out.items() if v}


def shapes_of(g: rdflib.Graph, schema: Path) -> list:
    """SHACL shapes with the message each constraint fails with.

    Read from shapes.ttl directly: the shapes are not part of the schema graph
    the rest of this reads, and their messages carry more of the reasoning than
    any other single place in the repository.
    """
    path = schema / "shapes.ttl"
    if not path.is_file():
        return []
    sg = rdflib.Graph().parse(path, format="turtle")
    rows = []
    for shape in sorted(set(sg.subjects(RDF.type, SH.NodeShape)), key=str):
        target = one(sg, shape, SH.targetClass)
        messages = []
        for _, _, constraint in sg.triples((shape, SH.property, None)):
            msg = one(sg, constraint, SH.message)
            path_o = one(sg, constraint, SH.path)
            if msg:
                messages.append((qn(sg, rdflib.URIRef(path_o)) if path_o else "-", msg))
        for _, _, constraint in sg.triples((shape, SH.sparql, None)):
            msg = one(sg, constraint, SH.message)
            if msg:
                messages.append(("(SPARQL)", msg))
        rows.append((qn(sg, shape), qn(sg, rdflib.URIRef(target)) if target else "-",
                     messages))
    return rows


HEADER = ("<!-- GENERATED FILE - do not hand-edit. -->\n"
          "<!-- Rebuild with tools/schema_docs.py; "
          "see docs/maintainers/generated-artifacts.md. -->\n\n")


def write_indexes(g: rdflib.Graph, schema: Path, out: Path) -> list[Path]:
    """Write compact, task-specific indexes beside the full reference.

    The full reference remains useful for browsing descriptions in context;
    these three pages give stable destinations for readers who need only one
    artifact kind and keep enumeration generated from source.
    """
    out.mkdir(parents=True, exist_ok=True)
    cls = classes_of(g)
    props = properties_of(g)
    shapes = shapes_of(g, schema)

    class_lines = [
        "# Ontology class index",
        "",
        "Generated from the current ontology import closure. The kind column is the nearest recognized upper/BFO anchor; it describes formal category, not scientific validation.",
        "",
        "| Class | Kind | Description |",
        "|---|---|---|",
    ]
    for term in cls:
        class_lines.append(
            f"| `{qn(g, term)}` | {anchor_of(g, term)} | "
            f"{md_escape(one(g, term, RDFS.comment) or 'No source comment.')} |"
        )

    property_lines = [
        "# Ontology property index",
        "",
        "Generated from the current ontology import closure. Domain and range are declarations, not closed-world validation guarantees.",
        "",
        "| Property | Domain | Range | Description |",
        "|---|---|---|---|",
    ]
    for term in props:
        domain, range_ = domain_range(g, term)
        property_lines.append(
            f"| `{qn(g, term)}` | `{domain}` | `{range_}` | "
            f"{md_escape(one(g, term, RDFS.comment) or 'No source comment.')} |"
        )

    shape_lines = [
        "# SHACL shape index",
        "",
        "Generated from `shapes.ttl`. These are implemented graph-validity checks; they are not a claim of ecological truth or scientific sufficiency.",
        "",
        "| Shape | Target | Constraint messages |",
        "|---|---|---|",
    ]
    for shape, target, messages in shapes:
        rendered = "<br>".join(md_escape(message) for _, message in messages) or "No explicit message."
        shape_lines.append(f"| `{shape}` | `{target}` | {rendered} |")

    outputs = []
    for name, lines in (
        ("ontology-classes.md", class_lines),
        ("ontology-properties.md", property_lines),
        ("shapes.md", shape_lines),
    ):
        path = out / name
        path.write_text(HEADER + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        outputs.append(path)
    return outputs


def write_reference(g: rdflib.Graph, schema: Path, out: Path,
                    schema_subjects: set) -> Path:
    L: list[str] = []
    w = L.append

    titles = [str(t) for s in g.subjects(RDF.type, OWL.Ontology)
              for t in g.objects(s, DCT.title)]
    cls, props = classes_of(g), properties_of(g)
    vocab = vocabularies(g, schema_subjects)
    shapes = shapes_of(g, schema)

    w("# Schema reference\n")
    w("Generated from the Turtle sources. Every description below is the term's "
      "own `rdfs:comment` - the schema documents itself, and this file is a "
      "reading view of it rather than a second copy that can drift.\n")
    w(f"**{len(cls)} classes · {len(props)} properties · {len(vocab)} controlled "
      f"vocabularies · {len(shapes)} SHACL shapes**\n")
    if titles:
        w("Modules: " + ", ".join(f"*{t}*" for t in sorted(titles)) + "\n")

    w("Every class reaches [BFO 2.0](https://github.com/BFO-ontology/BFO) "
      "(ISO/IEC 21838-2) through the shared upper module, and a SHACL "
      "constraint refuses any that does not. The **kind** column is that "
      "anchor: the answer to *what kind of thing is this?*\n")

    w("## Contents\n")
    w("- [Classes](#classes)")
    w("- [Controlled vocabularies](#controlled-vocabularies)")
    w("- [Properties](#properties)")
    w("- [Constraints](#constraints)\n")

    # --- classes, grouped by their BFO kind so the shape of the model shows ---
    w("## Classes\n")
    by_kind: dict[str, list] = defaultdict(list)
    for c in cls:
        by_kind[anchor_of(g, c)].append(c)
    w("| Class | Kind | Parent |")
    w("|---|---|---|")
    for kind in sorted(by_kind):
        for c in by_kind[kind]:
            parents = [qn(g, p) for p in g.objects(c, RDFS.subClassOf)
                       if not isinstance(p, rdflib.BNode)]
            w(f"| [`{qn(g, c)}`](#{anchor_id(qn(g, c))}) | {kind} | "
              f"{', '.join(f'`{p}`' for p in parents) or '-'} |")
    w("")

    for kind in sorted(by_kind):
        w(f"### {kind.capitalize()}\n")
        for c in by_kind[kind]:
            name = qn(g, c)
            w(f"#### `{name}`\n")
            label = one(g, c, RDFS.label)
            if label:
                w(f"**{label}**\n")
            parents = [qn(g, p) for p in g.objects(c, RDFS.subClassOf)
                       if not isinstance(p, rdflib.BNode)]
            if parents:
                w("Subclass of " + ", ".join(f"`{p}`" for p in parents) + ".\n")
            comment = one(g, c, RDFS.comment)
            w((comment.strip() if comment else "_No description._") + "\n")
            scope = one(g, c, SKOS.scopeNote)
            if scope:
                w(f"> **Scope.** {scope.strip()}\n")
            # Properties that take this class as their domain: what you can say
            # about one of these.
            own = [p for p in props if str(c) in
                   {str(o) for o in g.objects(p, RDFS.domain)}]
            if own:
                w("Properties: " + ", ".join(
                    f"[`{qn(g, p)}`](#{anchor_id(qn(g, p))})" for p in own) + "\n")

    # --- vocabularies -------------------------------------------------------
    w("## Controlled vocabularies\n")
    if not vocab:
        w("_None._\n")
    for cls_, members in sorted(vocab.items(), key=lambda kv: str(kv[0])):
        w(f"### `{qn(g, cls_)}`\n")
        c = one(g, cls_, RDFS.comment)
        if c:
            w(c.strip() + "\n")
        w("| Member | Label | Meaning |")
        w("|---|---|---|")
        for m in members:
            w(f"| `{qn(g, m)}` | {one(g, m, RDFS.label) or '-'} | "
              f"{md_escape(one(g, m, RDFS.comment) or '-')} |")
        w("")

    # --- properties ---------------------------------------------------------
    w("## Properties\n")
    w("| Property | Domain | Range |")
    w("|---|---|---|")
    for p in props:
        d, r = domain_range(g, p)
        w(f"| [`{qn(g, p)}`](#{anchor_id(qn(g, p))}) | `{d}` | `{r}` |")
    w("")
    for p in props:
        name = qn(g, p)
        w(f"#### `{name}`\n")
        label = one(g, p, RDFS.label)
        if label:
            w(f"**{label}**\n")
        d, r = domain_range(g, p)
        w(f"`{d}` → `{r}`\n")
        comment = one(g, p, RDFS.comment)
        w((comment.strip() if comment else "_No description._") + "\n")

    # --- constraints --------------------------------------------------------
    w("## Constraints\n")
    w("SHACL shapes, with the message each constraint fails with. The messages "
      "are written to be read by whoever trips them years from now, so they "
      "state the reasoning and cite the standard where there is one. Each is "
      "exercised against a deliberate violation in `tests/fixtures/` - a "
      "constraint that has only ever seen valid data is untested.\n")
    for shape, target, messages in shapes:
        w(f"### `{shape}`\n")
        w(f"Targets `{target}`.\n")
        if not messages:
            w("_No messages._\n")
            continue
        for path_, msg in messages:
            w(f"- **`{path_}`** — {msg.strip()}")
        w("")

    dest = out / "schema-reference.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(HEADER.format(schema=relative(schema), out=relative(out))
                    + "\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return dest


def write_diagram(g: rdflib.Graph, schema: Path, out: Path) -> Path:
    """Mermaid diagrams: rendered by GitHub, diffable, and no build step.

    This is what replaces the committed SVG and PDF class diagrams for
    documentation purposes. An image had to be regenerated by a tool the reader
    might not have, could go stale against the schema without anyone noticing,
    and could not be read at all in a diff.
    """
    L: list[str] = []
    w = L.append
    cls = classes_of(g)

    w("# Class diagrams\n")
    w("Mermaid source, rendered natively by GitHub. Regenerated from the "
      "Turtle, so it cannot drift from the schema the way a checked-in image "
      "can.\n")

    w("## Anchoring\n")
    w("Every domain class by the kind of thing it is. This is the whole content "
      "of the upper-ontology commitment: adding a class means answering this "
      "question, and a SHACL constraint refuses one that does not.\n")
    by_kind: dict[str, list] = defaultdict(list)
    for c in cls:
        by_kind[anchor_of(g, c)].append(c)
    w("```mermaid")
    w("graph TD")
    for i, kind in enumerate(sorted(by_kind)):
        kid = f"K{i}"
        w(f'  {kid}["{kind}"]')
        for j, c in enumerate(by_kind[kind]):
            w(f'  {kid} --> {kid}_{j}["{qn(g, c)}"]')
    w("```\n")

    w("## Subclass hierarchy\n")
    w("Local classes only; the BFO parents are in the anchoring diagram above.\n")
    w("```mermaid")
    w("classDiagram")
    for c in cls:
        for p in g.objects(c, RDFS.subClassOf):
            if is_local(p) and not isinstance(p, rdflib.BNode):
                w(f"  {qn(g, p).replace(':', '_')} <|-- {qn(g, c).replace(':', '_')}")
    w("```\n")

    w("## Relations\n")
    w("Object properties between local classes, labelled with the property. "
      "Datatype properties are omitted - they are in the reference.\n")
    w("```mermaid")
    w("graph LR")
    seen = set()
    for p in properties_of(g):
        if (p, RDF.type, OWL.ObjectProperty) not in g:
            continue
        for d in g.objects(p, RDFS.domain):
            for r in g.objects(p, RDFS.range):
                if isinstance(d, rdflib.BNode) or isinstance(r, rdflib.BNode):
                    continue
                if not (is_local(d) and is_local(r)):
                    continue
                key = (str(d), str(p), str(r))
                if key in seen:
                    continue
                seen.add(key)
                w(f'  {qn(g, d).replace(":", "_")} -->|{qn(g, p)}| '
                  f'{qn(g, r).replace(":", "_")}')
    w("```\n")

    dest = out / "class-diagram.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(HEADER.format(schema=relative(schema), out=relative(out))
                    + "\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return dest


def write_taxonomy(g: rdflib.Graph, schema: Path, out: Path) -> Path | None:
    """The GET levels as a browsable document, if the taxonomy is present.

    The generated Turtle is 61,000 lines and carries several hundred words of
    the monograph's prose per group, which makes it the right thing for a query
    and the wrong thing for a reader. This is the reading view: the full tree
    with codes and names, and the drivers text that decides a bottom-up
    assignment, so the 108 groups can actually be browsed.
    """
    levels: dict[int, list] = defaultdict(list)
    q = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX eios: <https://example.org/eios/>
        PREFIX get:  <https://example.org/get/>
        SELECT ?c ?n ?l ?lev ?drivers WHERE {
          ?c skos:notation ?n ; skos:prefLabel ?l ; eios:getLevel ?lev .
          OPTIONAL { ?c get:keyEcologicalDrivers ?drivers }
        }"""
    for c, n, label, lev, drivers in g.query(q):
        levels[int(lev)].append((str(n), str(label), str(drivers) if drivers else ""))
    if not levels.get(3):
        return None

    L: list[str] = []
    w = L.append
    w("# IUCN Global Ecosystem Typology, Levels 1-3\n")
    w(f"**{len(levels.get(1, []))} realms · {len(levels.get(2, []))} biomes · "
      f"{len(levels.get(3, []))} ecosystem functional groups**\n")
    w("Generated from `schema/get-core.ttl`, which is itself generated from the "
      "monograph. Names and the *drivers* text are reproduced from the source - "
      "see `NOTICE.md`.\n")
    w("Levels 1-3 are constructed top-down from ecosystem function and are "
      "genuinely nested, so `skos:broader` holds between them. **Levels 4 and 5 "
      "are not a continuation of this ladder.** They are alternative pathways "
      "below Level 3, and a Level 5 unit attaches to a Level 3 group by "
      "`eios:assignedToEFG` rather than by nesting under a Level 4 unit "
      "(Keith et al. 2020, p. 5).\n")
    w("The **drivers** column is what a bottom-up assignment should be argued "
      "from: it is usually more diagnostic than composition, and two groups "
      "that share a species list are routinely separated by substrate, fire "
      "regime or salinity. Reading the label alone is how `T2.5 Temperate pyric "
      "humid forests` comes to look like a home for southeastern pine when its "
      "profile describes Australian wet forest 40 to 90 m tall.\n")

    biomes = {n: (label, d) for n, label, d in levels.get(2, [])}
    realms = {n: (label, d) for n, label, d in levels.get(1, [])}
    efgs: dict[str, list] = defaultdict(list)
    for n, label, drivers in sorted(levels[3], key=lambda r: r[0]):
        efgs[n.split(".")[0]].append((n, label, drivers))

    for realm_code in sorted(realms, key=lambda s: (len(s), s)):
        rlabel, _ = realms[realm_code]
        w(f"## {realm_code} — {rlabel}\n")
        for biome_code in sorted((b for b in biomes if b.startswith(realm_code)
                                  and b[len(realm_code):].isdigit()),
                                 key=lambda s: (len(s), s)):
            blabel, _ = biomes[biome_code]
            w(f"### {biome_code} — {blabel}\n")
            rows = efgs.get(biome_code, [])
            if not rows:
                w("_No groups listed._\n")
                continue
            w("| Code | Ecosystem functional group | Key ecological drivers |")
            w("|---|---|---|")
            for n, label, drivers in rows:
                short = (drivers[:300].rsplit(" ", 1)[0] + "…") if len(drivers) > 300 else drivers
                w(f"| `{n}` | {md_escape(label)} | {md_escape(short) or '—'} |")
            w("")

    dest = out / "get-taxonomy.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(HEADER.format(schema=relative(schema), out=relative(out))
                    + "\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return dest


def write_units(g: rdflib.Graph, schema: Path, out: Path) -> Path | None:
    """The proposed Level 5/6 units, grouped by study area.

    Presenting them as a table is not presenting them as findings: the actual
    epistemic status and official Red List status are columns, not footnotes.
    """
    q = """
        PREFIX eios: <https://example.org/eios/>
        PREFIX rle:  <https://example.org/rle/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?u ?label ?lev ?efg ?origin ?epistemic ?status ?note WHERE {
          ?u a ?k . VALUES ?k { eios:GlobalEcosystemType eios:SubGlobalEcosystemType }
          ?u rdfs:label ?label ; eios:getLevel ?lev .
          OPTIONAL { ?u eios:assignedToEFG ?e . ?e skos:notation ?efg }
          OPTIONAL { ?u eios:anthropogenicOrigin ?o . ?o rdfs:label ?origin }
          OPTIONAL { ?u eios:epistemicStatus ?ep . ?ep rdfs:label ?epistemic }
          OPTIONAL { ?u rle:officialStatus ?s . ?s rdfs:label ?status }
          OPTIONAL { ?u eios:diagnosticNote ?note }
        }"""
    rows = list(g.query(q))
    if not rows:
        return None

    by_area: dict[str, list] = defaultdict(list)
    for r in rows:
        # The namespace segment is the study area: .../eios/guis/L5-... .
        parts = str(r[0]).rstrip("/").split("/")
        by_area[parts[-2] if len(parts) > 2 else "units"].append(r)

    L: list[str] = []
    w = L.append
    w("# Proposed classification units\n")
    w(f"**{len(rows)} units across {len(by_area)} landscapes.**\n")
    w("> **RESEARCH HYPOTHESES / WORKED EXAMPLES — NOT AUTHORITATIVE "
      "CLASSIFICATION UNITS.** The table reports values actually present in RDF; "
      "a dash means the status is absent rather than implied. Species composition "
      "and boundaries are not verified against field inventories.\n")
    w("The **origin** column is the anthropogenic flag, a property of the type. "
      "It is not a condition: a constructed system is a kind of ecosystem, not a "
      "damaged one, and a collapse claim attaches to the occurrence that "
      "preceded it. See `schema-reference.md` for `eios:CollapsedState`.\n")

    for area in sorted(by_area):
        w(f"## {area}\n")
        w("| Unit | Level | EFG | Origin | Epistemic status | RLE status |")
        w("|---|---|---|---|---|---|")
        for r in sorted(by_area[area], key=lambda r: (int(r[2]), str(r[1]))):
            w(f"| {md_escape(str(r[1]))} | {int(r[2])} | "
              f"{'`' + str(r[3]) + '`' if r[3] else '—'} | "
              f"{str(r[4]) if r[4] else '—'} | "
              f"{str(r[5]) if r[5] else '—'} | "
              f"{str(r[6]) if r[6] else '—'} |")
        w("")
        notes = [(str(r[1]), str(r[7])) for r in by_area[area] if r[7]]
        if notes:
            w("### What separates these units\n")
            w("The diagnostic notes, which record the reasoning a finished "
              "classification normally discards.\n")
            for label, note in sorted(set(notes)):
                w(f"**{label}**\n")
                w(note.strip() + "\n")

    dest = out / "proposed-units.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(HEADER.format(schema=relative(schema), out=relative(out))
                    + "\n".join(L) + "\n", encoding="utf-8", newline="\n")
    return dest



def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schema", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    if not args.schema.is_dir():
        print(f"error: no schema directory {args.schema}")
        return 1
    g, schema_subjects = load(args.schema)
    print(f"loaded {len(g)} triples from {relative(args.schema)}")
    generated = [write_reference(g, args.schema, args.out, schema_subjects),
                 write_diagram(g, args.schema, args.out),
                 # Emitted only where the data exists: the detection schema has
                 # no taxonomy and no classification units.
                 write_taxonomy(g, args.schema, args.out),
                 write_units(g, args.schema, args.out),
                 *write_indexes(g, args.schema, args.out)]
    for dest in [d for d in generated if d is not None]:
        kb = dest.stat().st_size / 1024
        print(f"wrote {relative(dest)}  ({kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
