# Black Mesa ontology — project instructions

This repository contains the semantic/evidentiary core for the Black Mesa agricultural biosecurity platform.

Read `README.md`, `docs/team-guide.md`, and `docs/architecture.md` before changing the ontology.

## Product abstraction

Black Mesa is **sensor-agnostic**.

The expected early platform includes drones, but the ontology must not require flight, spectral imagery, one sensor modality, one assay chemistry, one crop, one pathogen, or one jurisdiction.

Model the evidence chain:

~~~text
survey
-> observation
-> anomaly
-> sensor indication
-> hypotheses
-> next-best observation / sampling
-> specimen + custody
-> diagnostic procedure
-> diagnostic result
-> scientific detection
-> regulatory/reporting evaluation
-> alert
~~~

Do not collapse adjacent stages.

## Non-negotiable semantic rules

1. Observation is not diagnosis.
2. Anomaly is not pathogen presence.
3. `SensorIndicationAssertion` MUST NOT use `assertsPathogen`.
4. Diagnostic disposition is separate from evidence stage and confidence.
5. A calibrated probability exists only when a calibrated model actually generated it.
6. `NotDetected` is a diagnostic disposition, never a synonym for "no anomaly observed."
7. Specimens and aliquots have persistent independent identities.
8. Custody is represented as explicit events with agents and timestamps.
9. Scientific detection is separate from regulatory determination and alert.
10. Raw imagery/dense sensor arrays stay outside RDF and are referenced by URI + checksum.
11. Crops/pathogens/sensors/methods should reuse external canonical identifiers where practical.
12. Jurisdictions are data, not subclasses of detection.

## Sensor agnosticism

Use `bmo:SurveyActivity`, `bmo:SensorObservation`, and `bmo:ObservedAnomaly`.

`bmo:Flight` is only a subtype of `SurveyActivity`.

`bmo:SpectralAnomaly` is only a subtype of `ObservedAnomaly`.

Use SOSA/SSN for sensor and platform semantics. Do not create local hardware taxonomies in the core.

## Epistemic model

Use three independent dimensions.

### Evidence stage

- SensorIndicationStage
- FieldObservationStage
- SpecimenEvidenceStage
- DiagnosticEvidenceStage
- ConfirmatoryEvidenceStage

### Diagnostic disposition

- Confirmed
- Suspected
- NotDetected
- Undetermined

### Confidence assessment

- evidence strength
- evidence completeness
- model applicability
- assay applicability
- provenance quality
- optional calibrated probability

Do not reintroduce a single ranked "confidence tier."

`bmo:ConfidenceTier` and `bmo:PreSymptomatic` exist only for v0.2 compatibility and are deprecated.

## Chain of custody

Chain of custody is a first-class Phase 1 requirement.

Use `SampleCollection`, `TransferEvent`, `ReceiptEvent`, `StorageEvent`, `AliquotEvent`, `CustodyChain`, `CustodyRecord`, `Specimen`, and `Aliquot`.

A legally consequential detection must be traceable to a `CustodyRecord`.

Do not treat a custody chain as a free-text field.

## Diagnostic model

Use `DiagnosticProcedure` as the generic analysis process.

`Assay` is a subtype for compatibility.

Use `DiagnosticProcedureProfile` for validated pathogen, host, specimen matrix, sensitivity, specificity, detection limit, and validation source.

A negative result does not automatically assert biological absence.

## Reporting boundary

Initial operating jurisdictions:

- Arkansas
- Louisiana
- Missouri
- Oklahoma
- Texas

Use `OperationalJurisdiction` instances and versioned `ReportingRule` objects.

NPDN diagnostic dispositions and CAP alert certainty are different semantic dimensions.

See `schema/reporting-crosswalks.ttl`.

## Upper ontology

Every local class must reach BFO 2.0 through `upper/upper-core.ttl`.

BFO is used because the surrounding OBO ecosystem (OBI, PATO, ENVO, Plant Ontology, IAO, RO) is already BFO-aligned.

Do not add a local class without deciding whether it is information, process, material, site, quality, or role.

## Validation

After every schema change:

~~~bash
python tools/validate_ontology.py \
  schema/bmo-core.ttl \
  schema/reporting-crosswalks.ttl \
  --shapes schema/shapes.ttl

python -m pytest tests/ -q

python tools/schema_docs.py --schema schema --out docs
~~~

Every new SHACL rule needs a deliberate failing fixture proving that the rule fires.

## Review audiences

Plant pathology/diagnostics should review method validity, dispositions, and evidentiary sufficiency.

Sensor/ML should review whether the ontology assumes hardware or treats uncalibrated scores as probabilities.

Field operations should review specimen identity, custody events, handoffs, container/seal requirements, and realistic timestamps.

Systems engineering should review graph boundaries, storage architecture, versioning, ingestion constraints, and provenance.

Regulatory/reporting should review jurisdictional rules, external crosswalk fidelity, and the separation of science from policy.

## Scope discipline

The realistic ontology failure mode is still over-building.

Do not add hundreds of crop/pathogen/sensor subclasses.

The core should represent the evidence and decision structure; biological and hardware breadth should primarily enter through external identifiers and instance/reference data.

Every new term must answer an operational competency question.

## Public-repository publishing warning

This repository has historically been assembled from a source monorepo. A future publish can overwrite direct edits made here.

Any accepted change must therefore be ported into the source-of-truth publication workspace before the next automated publish.
