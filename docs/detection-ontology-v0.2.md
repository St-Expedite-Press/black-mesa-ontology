---
title: The Detection Ontology
subtitle: A conceptual schema for pre-symptomatic agricultural pathogen detection — entities, provenance, confidence, and the boundary of the graph
kicker: BLACK MESA / ONTOLOGY
doc_id: BM-ONT-0.2
style: mesa
meta:
  Subject: Phase 1 conceptual schema, detection core
  Status: Design settled; schema authored and validating
  Scope: Ontology only. Programme scheduling and workstream matters are out of scope.
  Date: 11 September 2026
footer: Conceptual schema design. Class-count and sizing figures derive from the Data Architecture Assessment and are second-hand. Crosswalk entries are not yet authored.
---

[TOC]

## Summary

This paper states the conceptual schema for a platform that detects crop pathogens before symptoms appear, and argues the modelling decisions behind it.

Four decisions carry the design. **Detection is a chain, not an event**, so the schema represents flight, anomaly, sample, assay, and detection as distinct objects joined by stated cardinalities. **Confidence needs a tier that does not exist** in any adopted vocabulary, because every published enumeration presupposes visible symptoms. **The graph has a hard boundary** at raw imagery, and crossing it inflates the store by roughly two orders of magnitude. And **a detection is an assertion**, carrying evidence and provenance, rather than a property stamped on a field.

Roughly 140 net-new classes, most surrounding vocabulary imported, three things invented. Section 8 argues why the deliverable is a documented conceptual schema rather than an axiomatised ontology, including the case against that choice.

---

## 1. What the domain actually contains

Existing agricultural diagnostic data models begin where a human notices something wrong. A sample arrives, a laboratory confirms it, a record is filed. The vocabularies built around that workflow assume a symptomatic starting point because historically there was no other kind.

This platform starts earlier. A spectral anomaly is not a symptom; it is a signal that something may be worth sampling. Between that signal and a confirmed diagnosis sits a chain of physical events, each of which can fail, be repeated, or be performed on the wrong thing.

Two modelling consequences follow, and they are the reason a new schema is needed rather than an adaptation of an existing one.

**The confidence vocabulary has no bucket for the platform's first-order output.** The earliest tier in the adopted diagnostic enumeration still presupposes visible symptoms. A pre-symptomatic anomaly is a different epistemic object, and mapping it to the nearest available label destroys the distinction the platform exists to create.

**Nothing spans the join.** Sensing vocabularies stop at the observation. Laboratory vocabularies start at the specimen. The platform lives precisely at the seam, and the chain of custody across it has no published representation.

---

## 2. The detection chain

<figure>
<svg viewBox="0 0 760 250" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-labelledby="fig1-title fig1-desc">
  <title id="fig1-title">Figure 1. The detection chain from flight to alert.</title>
  <desc id="fig1-desc">A left-to-right chain of five objects: flight, spectral anomaly, sample,
    assay result, and detection, with an alert hanging below the detection. Cardinalities are
    marked on each link: a flight produces zero or more anomalies, an anomaly triggers one
    sample, a sample yields one assay result, a result becomes at most one detection, and a
    detection may or may not trigger an alert. Imagery branches off the flight into object
    storage and is referenced by identifier and checksum rather than entering the graph.</desc>
  <defs>
    <marker id="ar-bm2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#14161a"/>
    </marker>
    <marker id="ar-bm2g" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#8b8d87"/>
    </marker>
    <style>
      .m-l  { font: 600 12px 'Segoe UI', Arial, sans-serif; fill: #14161a; }
      .m-s  { font: 10px 'Cascadia Code', Consolas, monospace; fill: #4a4f57; }
      .m-g  { font: 10px 'Cascadia Code', Consolas, monospace; fill: #2f6f4f; }
      .m-b  { fill: #e7e6de; stroke: #14161a; stroke-width: 1.8; }
      .m-b2 { fill: #f0eee7; stroke: #8b8d87; stroke-width: 1.4; stroke-dasharray: 4 3; }
      .m-a  { stroke: #14161a; stroke-width: 1.8; fill: none; marker-end: url(#ar-bm2); }
      .m-a2 { stroke: #8b8d87; stroke-width: 1.4; fill: none; marker-end: url(#ar-bm2g); }
    </style>
  </defs>
  <rect x="0" y="0" width="760" height="250" fill="#f0eee7"/>

  <rect x="16"  y="92" width="106" height="44" class="m-b"/>
  <text x="69"  y="112" text-anchor="middle" class="m-l">Flight</text>
  <text x="69"  y="127" text-anchor="middle" class="m-s">sortie</text>

  <rect x="158" y="92" width="106" height="44" class="m-b"/>
  <text x="211" y="112" text-anchor="middle" class="m-l">Anomaly</text>
  <text x="211" y="127" text-anchor="middle" class="m-s">spectral</text>

  <rect x="300" y="92" width="106" height="44" class="m-b"/>
  <text x="353" y="112" text-anchor="middle" class="m-l">Sample</text>
  <text x="353" y="127" text-anchor="middle" class="m-s">collected</text>

  <rect x="442" y="92" width="106" height="44" class="m-b"/>
  <text x="495" y="112" text-anchor="middle" class="m-l">Assay</text>
  <text x="495" y="127" text-anchor="middle" class="m-s">result</text>

  <rect x="584" y="92" width="106" height="44" class="m-b"/>
  <text x="637" y="112" text-anchor="middle" class="m-l">Detection</text>
  <text x="637" y="127" text-anchor="middle" class="m-s">assertion</text>

  <path d="M 122 114 L 154 114" class="m-a"/>
  <path d="M 264 114 L 296 114" class="m-a"/>
  <path d="M 406 114 L 438 114" class="m-a"/>
  <path d="M 548 114 L 580 114" class="m-a"/>

  <text x="138" y="106" text-anchor="middle" class="m-s">0..n</text>
  <text x="280" y="106" text-anchor="middle" class="m-s">1</text>
  <text x="422" y="106" text-anchor="middle" class="m-s">1</text>
  <text x="564" y="106" text-anchor="middle" class="m-s">0..1</text>

  <rect x="584" y="184" width="106" height="40" class="m-b2"/>
  <text x="637" y="209" text-anchor="middle" class="m-s">Alert</text>
  <path d="M 637 136 L 637 180" class="m-a2"/>
  <text x="676" y="164" class="m-s">may</text>

  <rect x="16" y="26" width="250" height="40" class="m-b2"/>
  <text x="141" y="51" text-anchor="middle" class="m-s">imagery &#8594; object store (URI + checksum)</text>
  <path d="M 69 92 L 69 70" class="m-a2"/>

  <text x="300" y="45" class="m-g">never tiled into the graph</text>
  <text x="300" y="60" class="m-s">see section 4</text>
  <text x="16" y="238" class="m-s">every link carries provenance; any detection resolves back to its flight</text>
</svg>
<figcaption><strong>Figure 1.</strong> The detection chain. The cardinalities carry most of the modelling content.</figcaption>
</figure>

A **flight** produces **zero or more** anomalies. A sortie that finds nothing is still a recorded event with a negative result, not an absence of data — a distinction that matters as soon as anyone asks how much of a season was surveyed.

An **anomaly** triggers **one** sample; a **sample** yields **one** assay result; a confirmed result becomes **at most one** detection.

A **detection may** trigger an alert, and frequently should not. This is the link where the schema touches policy. An alert has consequences for a grower, a state programme, and potentially a market, and the decision to raise one is not the same claim as the determination that a pathogen is present. Keeping detection and alert as separate objects joined by a defeasible link is what allows alerting policy to change without rewriting the diagnostic record.

### 2.1 Detection is an assertion

The most consequential modelling decision in the schema is that a detection is not a property of a field, a flag on a sample, or a row in a results table. It is an **assertion object** carrying what concluded it, from what evidence, under which rule version, at what time, and with what confidence.

```turtle
:Detection-4417 a bm:Detection ;
    bm:concerns        :Zone-8812 ;
    bm:derivedFrom     :AssayResult-9930 ;
    bm:assertsPathogen <NCBITaxon:5518> ;
    bm:confidence      :Conf-4417 ;
    bm:custodyChain    :Chain-4417 ;
    bm:generatedUnder  :RuleSet-1.2 ;
    prov:generatedAtTime "2026-09-11T14:02:00Z"^^xsd:dateTime .
```

The cost is one extra hop in every query. The benefit is that a later change to an inference rule does not silently rewrite conclusions already drawn, and that any detection can be explained rather than merely reported. For a system whose output may inform a quarantine decision, an unexplainable detection is not evidence.

---

## 3. Confidence, and the tier that does not exist

The platform adopts the established four-level diagnostic enumeration — confirmed, suspected, not detected, undetermined — tracked separately by genus and species. Adoption rather than invention is deliberate: the receiving diagnostic network already implements it, and a parallel scale would guarantee a lossy translation at exactly the boundary where fidelity matters.

The problem is that the enumeration's earliest positive tier, *suspected*, presupposes visible symptoms. The platform's first-order output precedes that stage entirely.

So the schema extends the enumeration with a **pre-symptomatic tier** sitting below *suspected*: a sensor-derived indication that a sample is warranted, carrying no claim that disease is present. It is defined by what produced it and what it licenses — it licenses sampling, and nothing else.

Three properties of this term are worth stating because they constrain everything downstream.

**It is not a weaker *suspected*.** It is a different kind of claim, made on different evidence, warranting a different action. Modelling it as a lower confidence value on the same scale would be a category error, and would let it be compared numerically against claims it is not commensurate with.

**It is the term most at risk at every boundary.** Mapping it to the nearest existing bucket is the path of least resistance in every integration, and each individual decision to do so looks locally reasonable. The cumulative effect is a platform whose distinguishing output is indistinguishable from everyone else's by the time it reaches a recipient.

**The schema cannot prevent that.** What it can do is make the loss explicit and attributable at the point it occurs, which is the purpose of recording crosswalk fidelity in Section 5.

### 3.1 Confidence is multi-dimensional

A single number cannot distinguish a calibrated model output from an expert guess rendered as a decimal. The schema separates the axes, and the absence of a value is itself meaningful:

| Axis | Records |
|---|---|
| Calibrated probability | Populated **only** where a probabilistic model produced it. Never imputed |
| Evidence strength | How strongly the available evidence bears on the claim |
| Evidence completeness | How much of what the diagnostic model asked for was obtained |
| Assay applicability | Whether the assay was validated for this pathogen, host, and matrix |
| Provenance quality | Reliability of the chain from sensing to assertion |

Assay applicability is the axis most often omitted and the one that matters most here. An assay validated for one host and applied to another is not merely less accurate — its reported sensitivity is not a property of the situation it is being used in. Keeping this separate is what lets the system decline to trust its own number.

---

## 4. The boundary of the graph

The schema draws a hard line: **raw spectral imagery never enters the graph.** Imagery is held in object storage and referenced by identifier and checksum. The graph holds entities, relationships, and provenance.

The magnitude makes this structural rather than stylistic. At ten thousand farms over five years, the correct architecture is on the order of **373 million triples** — ordinary, and well within what a production store handles. The same system with imagery tiled into the graph is on the order of **248 billion**, an inflation factor of roughly **665×**.

The per-sortie figure is the more intuitive one. A single twelve-acre sortie at working resolution produces on the order of **24,300 triples** of imagery metadata if tiled and stored. Across a season, one farm's imagery bookkeeping alone exceeds the whole-graph total of a hundred-farm pilot.

Three observations, because the reasoning matters more than the number.

**The failure is not gradual.** A store at 373 million triples and the same store at 248 billion are not one system at two scales. Query planning, index behaviour, and backup economics all change character. This cannot be deferred and corrected later by adding hardware.

**The temptation recurs.** Putting imagery in the graph is genuinely convenient — one query language, one access-control model, one backup story. Someone will propose it again, in good faith, after the current team has moved on. The decision therefore belongs in the schema's own documentation with its reasoning attached, not only in a design note.

**Referencing is not free.** A checksum reference means the graph cannot answer questions about imagery content without a second system. That is the correct trade, but it is a trade, and the queries that become two-step should be identified before anything is designed around the assumption that they are one-step.

---

## 5. Reuse, invention, and crosswalk fidelity

### 5.1 Imported by reference

| Vocabulary | Covers |
|---|---|
| SOSA/SSN | Sensor, platform, procedure, observation, result |
| QUDT | Units and quantity kinds on every measured value |
| GeoSPARQL | Geometry for farm, field, zone, collection point |
| Plant Ontology | Plant part and growth stage |
| NCBITaxon | Pathogen and host identifiers — by reference only, never a full import |
| PROV-O | Provenance on every assertion |

Cherry-picked rather than imported whole: assay, specimen, and detection-limit terms from OBI; phenotypic qualities such as necrosis and chlorosis from PATO; severity scales from Crop Ontology. Each term is recorded with its source and the reason it was chosen.

### 5.2 The three inventions

**The pre-symptomatic confidence tier**, because no published enumeration has a bucket for a claim made before symptoms exist.

**The sensor-to-sample chain of custody**, because sensing vocabularies end at the observation and laboratory vocabularies begin at the specimen, and the platform's entire value sits across that gap.

**Assay-specific result semantics**, defining what a positive, negative, or inconclusive result licenses for the particular confirmation chemistry — and specifically what an inconclusive result does *not* license.

Everything else must be traceable to something already published. A term that cannot survive that test has not earned its place.

### 5.3 Mapping is a membership claim

A crosswalk to an external reporting vocabulary records **direction and fidelity**, not equivalence:

| Fidelity | Meaning |
|---|---|
| exact | The terms coincide |
| broader / narrower | One side is coarser |
| partial | Overlapping, neither containing the other |
| **none** | No defensible mapping exists |

The `none` entries are the valuable output. The pre-symptomatic tier is the known case, and three responses are possible, each with a different cost borne by a different party: map it to the nearest tier and lose the distinction; withhold pre-symptomatic detections from submission until they reach a symptomatic tier; or submit with an extension field that most receivers will ignore. The choice is not yet made, and the schema should not pre-empt it — it should make all three expressible and record which was taken.

The collapse rule from internal confidence to an external level must be written explicitly and **must never be run in reverse**. An external level cannot be expanded back into dimensions it never carried.

### 5.4 Upper-ontology anchoring

Every class in the schema reaches **BFO 2.0** (ISO/IEC 21838-2) through a shared upper module. The choice is not stylistic: OBI, PATO, and Plant Ontology — all of which this schema cherry-picks from — are OBO Foundry ontologies built on BFO. Any other upper ontology would leave the imported terms in a foreign hierarchy.

The anchoring settles questions that would otherwise be argued repeatedly:

| Class | Kind of thing |
|---|---|
| `Detection`, `AssayResult`, `SpectralAnomaly`, `Alert` | Information — about the world, not part of it |
| `Flight`, `SampleCollection`, `Assay` | Processes — they happen and have temporal parts |
| `Specimen`, `Container`, `Host` | Material entities |
| `Farm`, `Field`, `Zone` | Sites — the place, not what occupies it |

Twenty of the schema's classes are information artifacts, which is the formal restatement of Section 2.1: most of what this system holds is claims, and claims can be wrong, versioned, and disagreed with in a way properties cannot.

A SHACL constraint refuses any class that does not reach BFO, and the violation fixtures include a deliberately unanchored class so the constraint is known to fire.

---

## 6. Scope

| Phase | Scope | Net-new classes |
|---|---|---|
| 1 | Detection core: farm, field, zone, flight, anomaly, sample, assay, confidence, alert | ~140 |
| 2 | Environmental context: weather, soil, growth stage, spread propagation | ~320 cumulative |
| 3 | Full platform: regulatory state, hardware telemetry, grower response, treatment outcomes | ~600 cumulative |

Only Phase 1 is being built. The full-scope figure is benchmark context rather than a target — larger than the Infectious Disease Ontology at 362 classes, an order of magnitude smaller than OBI at 5,240. The Phase 1 figure of ~140 is a **ceiling, not a floor**; a smaller honest schema beats a padded one, and padding is the easiest way to look productive while producing nothing reviewable.

---

## 7. Current state

| Component | State |
|---|---|
| Detection chain model | Designed, documented here |
| Confidence model | Designed, documented here |
| Storage boundary | Decided |
| Reuse and invention decisions | Settled |
| Entity and relationship definitions | Authored — `schema/bmo-core.ttl`, 20 classes and 22 properties |
| Upper-ontology anchoring | Every class reaches BFO 2.0 via `upper/upper-core.ttl`, enforced |
| Constraints | `schema/shapes.ttl`, 10 shapes, tested against 7 planted violations |
| Crosswalk table | **Structure defined; no entries authored** |

The schema exists and validates: lint, an OWL-RL closure over the BFO import, and SHACL all run clean, and the constraints are exercised against a fixture of deliberate violations rather than only against valid data.

The **crosswalk table remains the substantive gap.** `bmo:ReportingCrosswalk` is defined, and a shape refuses any entry that does not declare its fidelity — but no entry exists. Not one NPDN or CAP term appears anywhere in the schema. The mapping that section 5 argues is the most fragile part of the whole design is, as of this version, entirely unwritten, and the pre-symptomatic tier's `up:NoMapping` entry — the one the section calls the valuable output — is the first thing owed.

---

## 8. Discussion

### 8.1 Conceptual schema or axiomatised ontology

The deliverable is a documented conceptual schema — entities, relationships, controlled vocabularies, a confidence model, crosswalks — rather than a fully axiomatised OWL ontology with an upper-ontology commitment. This is the most consequential choice in the design and deserves argument rather than assertion.

**For.** The two people who must review the result are a domain scientist who does not read RDF and a systems engineer checking it against production constraints. Both are better served by plain-language definitions and worked examples than by axioms. Full formal treatment of the detection core is estimated at six to ten weeks against a three-week horizon, and a schema that arrives after the decisions it was meant to inform has no effect on anything. The historical failure mode for small-team ontology work is over-building.

**Against.** A conceptual schema does not catch its own contradictions. Without axioms and a reasoner, an inconsistency survives until a human notices it by reading, and humans do not reliably notice. There is also a ratchet risk: a conceptual schema that works well enough tends to stay conceptual, and the formalisation may never be funded once the thing appears to function.

**Judgement.** The case for is stronger under the actual constraint, but the case against identifies a hazard the scope decision does not address. Two mitigations are cheap enough to take now and preserve the option: write entity definitions so they *could* be axiomatised without restructuring, and record the axioms being deferred rather than leaving them implicit. Neither costs meaningful time; both prevent the deferral from becoming permanent by accident.

**What was taken.** Both mitigations were, and a third that the argument above did not anticipate. The schema is anchored to BFO 2.0 through a shared upper module, so every class has had to answer what kind of thing it is; an OWL-RL closure runs over that import on every validation; and the constraints that could be stated in SHACL were, then tested against planted violations. This does not make the schema axiomatised — there are still no disjointness axioms, no necessary and sufficient conditions, and no existential restrictions on relations — but it narrows the case against. The inconsistencies a reasoner can catch are now caught by a reasoner rather than by reading.

### 8.2 Why provenance is not an engineering nicety

It would be straightforward to treat the custody chain as a later addition and model detections without it. That would be a mistake for reasons that have little to do with data modelling.

A detection that cannot be traced to the flight, the collection, and the assay that produced it is not evidence. If the platform's output ever informs a regulatory action, a quarantine, or a market-relevant disclosure, the chain is the part that will be examined. Adding provenance later means retrofitting it onto records created without it, which in practice means the early records are unusable.

The regulatory use is a later phase. The records that use will require are being created now, which is the whole argument for building the chain into Phase 1.

### 8.3 What the schema cannot do

**It cannot make the pre-symptomatic tier survive integration.** It can express the tier, record what is lost in each mapping, and make the loss attributable. Whether recipients preserve the distinction is a matter of negotiation with them, not of modelling.

**It cannot validate ecological or epidemiological correctness.** Whether a given spectral signature warrants sampling for a given pathogen is a domain question the schema represents but does not answer.

**It cannot prevent the graph boundary from being crossed later.** It can document the decision and its magnitude prominently enough that crossing it is a visible choice rather than a drift.

### 8.4 A note on the sibling project

This repository holds a second ontology effort, in ecosystem classification, sharing a toolchain and a set of modelling patterns with this one — assertions as objects, provenance on every claim, multi-dimensional confidence, observation support determining evidential weight.

The instructive difference is in what each treats as given. That project's central difficulty is that an authoritative standard is subtler than its usual encoding, so the work is faithful representation of an existing structure. Here there is no authoritative structure for the pre-symptomatic chain, so the work is authoring one that external standards can still consume. One fights a misreading of a standard; the other fights the absence of one.

### 8.5 Confidence in the figures

The class-count estimates and the sizing model derive from a Data Architecture Assessment that is not in this repository. Every quantitative figure in this paper is therefore second-hand and uncheckable from here. The ~140 estimate is treated as a ceiling, which limits the damage if it is wrong in the direction of being too small and is harmless if it is too large. The 665× factor is load-bearing for a decision already taken, and obtaining the underlying document is the cheapest available risk reduction.

---

## 9. Conclusion

The schema has a narrow job: represent the chain from flight to alert so that a detection can be traced, a confidence can be interpreted correctly, and a result can reach the systems that consume it without silently losing the distinction that makes the platform worth building.

Four decisions carry it. Detection is a chain of distinct objects with stated cardinalities. A detection is an assertion carrying evidence and provenance, not a property. Confidence is multi-dimensional and includes a tier no adopted vocabulary provides. And the graph stops at raw imagery, at a factor of roughly 665× in avoided inflation.

One question remains genuinely open: how the pre-symptomatic tier survives the reporting boundary. That is a question about what the platform is for as much as about vocabulary, and it cannot be settled by modelling alone.

Nothing is authored yet. The value of settling the design first is that the remaining time can be spent writing rather than deciding.
