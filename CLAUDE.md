# Black Mesa ontology — project instructions

Workstream 4, Track C of the Black Mesa agricultural biosecurity platform: the Phase 1 conceptual schema for pre-symptomatic crop pathogen detection. Read this before doing anything in this directory.

## What is being built

A **documented conceptual schema** — entities, relationships, controlled vocabularies, a confidence model, and NPDN/CAP crosswalks.

Explicitly **not**: a fully axiomatised OWL ontology, or an upper-ontology commitment. Those belong to a later phase and are out of scope.

The platform detects crop pathogens before symptoms appear. A drone senses a spectral anomaly, a sampling arm collects material, a field assay confirms it, and the result feeds a geospatial early-warning network that growers and state agriculture departments act on. No data model for that chain exists, so it is being authored — narrowly, with most of the surrounding vocabulary imported rather than reinvented.

## Scope discipline

**The realistic failure mode is over-building, not under-building.** A beautifully axiomatised ontology delivered late is worth less to this team than a plainly documented schema delivered on time. Where a modelling choice is defensible either way, take the smaller one and record the larger as future work.

The deliverable must be reviewable by a domain scientist who does not read RDF, and checkable by a systems engineer against production constraints. Optimise for those two readers.

## Reuse before invention

Import wholesale by reference:

| Vocabulary | For |
|---|---|
| SOSA/SSN | the sensing layer |
| QUDT | units |
| GeoSPARQL | geometry |
| Plant Ontology | plant part, growth stage |
| NCBITaxon | pathogen and host identifiers — by reference only, never a full import |

Cherry-pick specific terms: OBI (assay, specimen, detection limit), PATO (necrosis, chlorosis, wilting), Crop Ontology (severity scales).

Adopt existing uncertainty vocabularies rather than authoring one — the NPDN four-level confidence enumeration (Confirmed / Suspected / Not Detected / Undetermined, tracked separately by genus and species) and the CAP severity/certainty/urgency triad for alerting.

## Invent only what nobody has modelled

- A **pre-symptomatic confidence tier**. The earliest existing bucket still assumes visible symptoms; the sensing stage precedes it.
- **Sensor-to-sample chain of custody** — flight, anomaly, collection, container, assay result, as one traceable chain.
- **Assay-specific semantics** for the confirmation chemistry.

## The architecture constraint

**Raw spectral imagery must never enter the graph as per-pixel or per-tile triples.** It inflates the store by roughly two orders of magnitude and destroys query performance. Reference imagery by URI and checksum from object storage; keep the graph to entities, relationships, and provenance.

## Layout

```
sources/          converted programme documents (page anchors preserved)
schema/           .ttl files - entities, provenance, crosswalks, shapes
docs/             working notes, citations register
reports/          rendered PDFs
visualizations/   generated graph diagrams
notebooks/ src/   analysis and reusable code
```

`sources/` holds the status report, workstream assignments, and the ontology lead onboarding brief. The onboarding brief is the working spec — read it first.

## Register

Documents use `style: mesa` — this project's own register — with an explicit `kicker`. See `templates/MESA-GUIDE.md`. The project-neutral `report` register remains available for anything that should not carry the programme's identity. This project may name the programme; the sibling project may not, and the two must not share document text.

## Upper ontology

Every class reaches **BFO 2.0** (ISO/IEC 21838-2) through the shared module at `upper/upper-core.ttl`, and a SHACL constraint refuses any class that does not. Adding a class means answering one question — is it information, a process, matter, a place, a quality, or a role?

The module is project-neutral by rule: it names neither project, and a test asserts that. A shared formal spine is not shared subject matter.

BFO was chosen because the vocabularies both projects already cherry-pick from — OBI, PATO, ENVO, Plant Ontology — are OBO Foundry ontologies built on it. Any other upper ontology would leave those imports in a foreign hierarchy.

See `.claude/skills/ontology-engineering/references/upper-ontology.md`.
All 20 classes in `bmo:` are anchored. `Detection`, `AssayResult`, `SpectralAnomaly` and `Alert` are information; `Flight`, `SampleCollection` and `Assay` are processes; `Specimen`, `Container` and `Host` are material; `Farm`, `Field` and `Zone` are sites.

## Agents

| Agent | Use for |
|---|---|
| `bm-ontology-architect` | Schema design — detection, provenance, confidence, chain of custody |
| `bm-crosswalk-engineer` | NPDN/CAP and external reporting mappings |
| `doc-producer` | Taking a document to a verified PDF |
| `citation-auditor` | Verifying citations before release |
| `graph-visualizer` | Rendering and checking schema diagrams |

## Skills

`ontology-engineering`, `document-production`, `figure-design`, `data-visualization`, `citation-discipline`.

## Commands

```bash
# validate
.venv/Scripts/python.exe tools/validate_ontology.py \
    projects/black-mesa-ontology/schema/*.ttl \
    --shapes projects/black-mesa-ontology/schema/shapes.ttl

# visualise (include the upper module: the anchoring is the point of the diagram)
.venv/Scripts/python.exe tools/visualize_ontology.py \
    upper/upper-core.ttl projects/black-mesa-ontology/schema/*.ttl \
    -o projects/black-mesa-ontology/visualizations/bmo-core

# lint and render
.venv/Scripts/python.exe tools/lint_docs.py projects/black-mesa-ontology/docs/<doc>.md
.venv/Scripts/python.exe tools/render_pdf.py projects/black-mesa-ontology/docs/<doc>.md \
    --style mesa -o projects/black-mesa-ontology/reports/<doc>.pdf
```

## Review path

Domain accuracy for pathogen and assay classes needs review by the microbiologist; production realism needs review by the systems engineer. Bring them class definitions and worked examples, not Turtle.
