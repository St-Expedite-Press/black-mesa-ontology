# Black Mesa ontology: team guide

This is the non-specialist guide to the repository.

If you work on sensors, machine learning, plant pathology, field operations, laboratory diagnostics, software, regulation, or project management, the ontology is the shared contract that says what each record means and what it is allowed to imply.

You do not need to know ontology engineering to review it.

## 1. What an ontology is doing here

A normal database can store:

~~~text
field = 17
pathogen = X
confidence = 0.82
status = detected
~~~

Those four fields hide nearly every question that matters:

- Was the "detection" a sensor anomaly or a laboratory determination?
- What exactly was sampled?
- Which diagnostic procedure generated the result?
- Was that method validated for this host and specimen matrix?
- Who possessed the specimen between collection and testing?
- What area does the conclusion actually apply to?
- Was 0.82 produced by a calibrated model?
- Which model/rule version produced the conclusion?
- Did Black Mesa make the scientific determination, or did a regulatory authority?
- Does "not detected" mean a negative diagnostic test, or merely that the sensor saw nothing unusual?

The ontology is the project's **meaning layer**.

## 2. RDF

RDF is the graph data model underneath the ontology.

An RDF statement is approximately:

~~~text
subject -- relationship --> object
~~~

Example:

~~~text
Detection-100 -- has disposition --> Confirmed
Transfer-100 -- to custodian --> Lab-A
~~~

Evidence chains are naturally graphs rather than single flat tables.

## 3. Turtle

Turtle (`.ttl`) is the human-readable text format used to write RDF.

Example:

~~~turtle
ex:Detection-100 a bmo:ConfirmedDetectionAssertion ;
    bmo:hasDiagnosticDisposition bmo:Confirmed ;
    bmo:hasEvidenceStage bmo:ConfirmatoryEvidenceStage .
~~~

You do not need to memorize the syntax to review the concepts.

## 4. OWL

OWL describes what kinds of things exist and how classes relate.

Examples:

~~~text
Flight is a kind of SurveyActivity.
TransferEvent is a kind of CustodyEvent.
ConfirmedDetectionAssertion is a kind of DiagnosticDetectionAssertion.
~~~

OWL defines meaning. It is not being used as a hidden workflow engine.

## 5. SHACL

SHACL says:

> A record of this kind is invalid unless it satisfies these constraints.

Black Mesa uses SHACL to enforce things such as:

- a sensor indication must identify the anomaly it came from;
- a sensor indication cannot assert pathogen presence;
- a diagnostic detection must have a pathogen, result, disposition, confidence assessment, rule version, timestamp, and custody record;
- a transfer event must name the releasing and receiving custodians;
- an imagery reference must have a URI and checksum.

OWL describes meaning. SHACL enforces data contracts.

## 6. BFO

BFO is the upper ontology used to prevent category mistakes.

It asks basic questions:

- Is this physical material?
- Is it a place?
- Is it a process?
- Is it information?
- Is it a quality?
- Is it a role?

Examples:

| Black Mesa concept | Kind of thing |
|---|---|
| Specimen | physical material |
| Zone | place |
| Sample collection | process |
| Diagnostic result | information |
| Detection assertion | information/claim |
| Alert | directive information |

A detection assertion is information *about* the crop or place; it is not literally part of the crop.

## 7. SOSA/SSN

SOSA/SSN are W3C vocabularies for sensors, observations, platforms, procedures, and observed properties.

Black Mesa uses them so the core does not become a hardware catalogue.

The core says:

~~~text
SurveyActivity uses Sensor.
Sensor is hosted by Platform.
SensorObservation occurs.
~~~

Specific devices can be supplied later as reference/instance data.

That is what **sensor-agnostic** means here.

## 8. PROV-O

PROV-O is the W3C provenance vocabulary.

Provenance answers:

- what generated this assertion?
- what evidence did it derive from?
- who or what generated it?
- when was it generated?
- what earlier record did it depend on?

For Black Mesa, provenance is part of whether evidence can bear scientific or legal weight.

## 9. GeoSPARQL and spatial support

GeoSPARQL is used for geometry and spatial relationships.

The ontology separates **the place** from **the evidentiary footprint**.

A field may be 300 acres.

A sensor anomaly may cover 0.8 acres.

A specimen may represent one plant.

A diagnostic result from that specimen does not automatically prove that the entire field is infected.

`SpatialSupportDescription` exists to make the supported scope explicit.

## 10. QUDT

QUDT supplies standard quantity and unit semantics.

It becomes important as Black Mesa adds measurements such as temperature, wavelength, concentration, moisture, distance, and diagnostic detection limits.

The rule is: do not invent unit strings when a standard quantity/unit representation exists.

## 11. Assertion

An assertion is a claim.

Claims are first-class objects because they can be supported, contradicted, superseded, reviewed, generated under a rule version, or wrong.

Examples:

- `SensorIndicationAssertion`
- `DiagnosticHypothesis`
- `DiagnosticDetectionAssertion`
- `RegulatoryDetermination`
- `ReportingDecision`

The ontology does not stamp `infected=true` directly onto a field.

## 12. Observation, anomaly, indication, hypothesis

### Sensor observation

The act of observing something with a device or procedure.

### Observed anomaly

A derived record saying the observation differs from an expected/reference condition.

An anomaly means:

> Something is different.

It does **not** mean:

> A pathogen is present.

Possible causes include disease, drought, flooding, nutrient stress, herbicide injury, insects, sensor artifact, or something unknown.

### Sensor indication assertion

A claim that the anomaly is meaningful enough to warrant further investigation.

It can drive sampling.

It cannot assert pathogen presence. That is machine-enforced.

### Diagnostic hypothesis

A candidate causal explanation.

Black Mesa should be allowed to keep several live candidates.

~~~text
Pathogen A             0.55
Water stress           0.31
Nutrient deficiency    0.09
Other                  0.05
~~~

A numeric probability is stored only if a calibrated model produced it. Otherwise candidates can simply be ranked.

## 13. Candidate set and next-best observation

The candidate set is the collection of hypotheses that remain plausible.

It exists because Black Mesa should eventually be able to ask:

> What observation would most efficiently distinguish the remaining candidates?

`ObservationRequirement` and `SamplingRecommendation` can eventually carry expected information gain, cost, delay, required equipment, spatial support, and required precision.

The calculation belongs in the reasoning service. The ontology records the request and why it exists.

## 14. Specimen and aliquot

A specimen is physical material collected from the field.

It has identity independent of the field, container, diagnostic procedure, result, and diagnosis.

An aliquot is a physically separated portion of a specimen.

~~~text
Specimen S
├── Aliquot A -> qPCR
├── Aliquot B -> sequencing
└── retained portion
~~~

Each aliquot gets its own identity and custody history while remaining traceable to the source specimen.

## 15. Chain of custody

Chain of custody is not a field saying `custody = good`.

It is a sequence of explicit events:

~~~text
collection
transfer
receipt
storage
aliquoting
analysis handoff
archive/destruction
~~~

A transfer record should answer:

- what specimen/aliquot?
- from whom?
- to whom?
- when?
- who performed/recorded the event?
- which container?
- which seal?
- what integrity/tamper status?
- what immediately preceded it?

`CustodyChain` represents the real process sequence.

`CustodyRecord` represents the information documenting that sequence.

The distinction matters because a record can have a gap even though the physical specimen continued to exist.

## 16. Diagnostic procedure and result

A diagnostic procedure is something that happens to a specimen or aliquot.

Possible future methods include qPCR, LAMP, ELISA, culture, sequencing, microscopy, and morphological examination.

The core ontology does not assume which chemistry will be selected.

A `DiagnosticResult` is information generated by the procedure.

Current procedure-level result statuses are:

~~~text
positive
negative
inconclusive
below detection limit
~~~

Those are not automatically the final diagnosis.

## 17. Diagnostic procedure profile

A procedure profile says where the method is actually valid.

It can record:

~~~text
validated pathogen
validated host
validated specimen matrix
sensitivity
specificity
limit of detection
validation source
~~~

This distinguishes:

> The test returned negative.

from:

> The test returned negative and is validated for this pathogen, host, and matrix.

Those claims do not carry the same evidentiary weight.

## 18. Evidence stage, disposition, confidence

v0.3 deliberately separates three dimensions.

### Evidence stage

Where in the workflow the evidence comes from:

~~~text
Sensor indication
Field observation
Specimen evidence
Diagnostic evidence
Confirmatory evidence
~~~

### Diagnostic disposition

What diagnostic work concluded:

~~~text
Confirmed
Suspected
Not Detected
Undetermined
~~~

### Confidence assessment

How much weight the assertion can bear:

- evidence strength;
- evidence completeness;
- model applicability;
- assay applicability;
- provenance quality;
- optional calibrated probability.

Do not combine those into one ranked "confidence tier."

## 19. Not Detected

`NotDetected` is a diagnostic disposition.

It does **not** mean:

- the farm was not surveyed;
- the sensor saw no anomaly;
- the field is pathogen-free;
- the organism is absent from the region.

The repository includes `examples/negative-survey.ttl` specifically to preserve this distinction.

## 20. Diagnostic detection assertion

This is the core scientific determination.

A valid diagnostic detection is expected to identify:

- spatial target;
- asserted pathogen;
- diagnostic result(s);
- diagnostic disposition;
- evidence stage;
- confidence assessment;
- custody record;
- rule/method version;
- assertion time.

For a confirmed detection, the evidence stage must also be confirmatory.

## 21. Regulatory determination and reporting

A regulatory determination is made under an authority or rule.

It is intentionally **not** the same object as the scientific detection.

The scientific record can stay the same while policy changes, and two jurisdictions may treat the same evidence differently.

The initial operational cluster is:

- Arkansas
- Louisiana
- Missouri
- Oklahoma
- Texas

These are represented as data. Do not create classes like `ArkansasDetection`.

## 22. Reporting crosswalk

A crosswalk states how an internal concept maps to an external scheme.

Possible fidelity values are:

~~~text
exact
broader
narrower
partial
none
~~~

`none` is a useful result. It means there is no defensible direct translation.

That is better than silently stuffing an internal concept into the nearest external field.

## 23. NPDN

The National Plant Diagnostic Network NDR uses diagnostic-confidence terms including:

~~~text
Confirmed
Suspected
Not Detected
Undetermined
~~~

Black Mesa's diagnostic dispositions crosswalk to those values.

A sensor indication has **no direct NPDN confidence mapping** because it is not yet a diagnostic record.

## 24. CAP

CAP is the Common Alerting Protocol.

CAP alert information includes concepts such as urgency, severity, and certainty.

Those are alert semantics, not diagnostic semantics.

Therefore:

~~~text
Confirmed != CAP Observed
Suspected != CAP Likely
~~~

unless an explicit jurisdiction/reporting rule derives those alert values.

## 25. Rule-set version

Every consequential assertion should record the model/rule version under which it was generated.

If the model changes later, an old assertion does not silently change in history. It can be re-evaluated and a new assertion can be issued.

## 26. Why raw imagery stays outside RDF

RDF is good at relationships. It is not the right store for millions of pixels or dense sensor arrays.

The graph stores:

~~~text
artifact URI
checksum
capture/provenance information
interpretations
~~~

The object/analytical store holds the bulk bytes.

## 27. What each team should review

### Plant pathology / diagnostics

- Does the model overstate what a procedure can conclude?
- Are method applicability and limits represented correctly?
- Are diagnostic dispositions being used properly?

### Sensor / ML

- Does any class assume a sensor modality we have not chosen?
- Is calibrated probability distinguished from score/rank?
- Can old observations be reinterpreted by a new model?

### Field operations

- Can every physical handoff be recorded?
- Can specimen and aliquot identities be scanned and maintained?
- Do timestamps, containers, seals, and integrity checks match real workflow?

### Systems engineering

- Which data belong in the graph versus object storage?
- Can every assertion be traced to source evidence and version?
- Are SHACL constraints enforceable at ingestion boundaries?

### Regulatory / reporting

- Is a scientific result being mistaken for a regulatory determination?
- Are jurisdiction and reporting rules explicit and versioned?
- Does an external mapping silently lose meaning?

## 28. Rule for proposing a new class

Before adding a new Black Mesa class, answer:

1. What operational distinction does it represent?
2. Is that distinction already represented by an external standard?
3. Does it affect observation, inference, custody, diagnostics, validation, or interoperability?
4. What competency question becomes answerable because the class exists?
5. What would break if we did not have it?

If the answer is essentially "it might be useful later," do not add it to the core yet.


## 29. Persistent identifiers

Black Mesa terms now use `https://w3id.org/black-mesa/` rather than `example.org`.

Why this matters: a class identifier such as `bmo:DiagnosticDetectionAssertion` can remain stable even if the GitHub repository, documentation site, or hosting infrastructure changes.

The W3ID redirect still has to be registered externally. The ontology can validate offline before that registration, but production Linked Data clients should eventually be able to dereference the identifier.

## 30. Initial pathosystem profiles

The core ontology does not contain a crop/pathogen family tree. Instead, `reference/pilot-pathosystems.ttl` instantiates four deployment profiles using external NCBITaxon identifiers:

- rice + rice blast;
- soybean + frogeye leaf spot;
- bread wheat + stripe rust;
- bread wheat + Karnal bunt as a regulatory stress test.

This is the preferred pattern for future pilots: add reference data before adding new schema.

## 31. Draft regulatory rules

A `ReportingRule` is a versioned record describing an external legal/regulatory rule as understood by the project.

Every initial state rule is explicitly marked:

`DRAFT — requires legal/regulatory review`

That means it is **not** an operative legal rule inside Black Mesa.

Draft records must retain human review. They cannot authorize autonomous regulator notification, quarantine, destruction, or movement restriction.

The rule registry exists so the team can fill in verified triggers, authorities, recipients, deadlines, effective dates, and movement restrictions without contaminating the scientific detection record.

## 32. Licensing

Ontology and semantic content are CC BY 4.0.

Software and executable tooling are Apache-2.0.

External standards, state source documents, and vendored third-party artifacts remain under their own terms. See `LICENSE` and `NOTICE.md`.
