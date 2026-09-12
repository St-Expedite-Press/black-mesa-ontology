> **Superseded by v0.4.** This document remains the design history for the sensor-agnostic evidence/custody refactor. The current release adds persistent identifiers, explicit licensing, four pilot pathosystem profiles, and a five-state draft regulatory-rule registry. See [detection-ontology-v0.4.md](detection-ontology-v0.4.md).

---
title: The Black Mesa Detection Ontology v0.3
subtitle: Sensor-agnostic surveillance, hypothesis management, defensible custody, diagnostic evidence, and reporting boundaries
kicker: BLACK MESA / ONTOLOGY
doc_id: BM-ONT-0.3
status: Implemented schema revision
date: 12 September 2026
---

# Summary

v0.3 changes the ontology from a drone-centered detection chain into a sensor-agnostic agricultural biosecurity evidence model.

The revision removes several category errors in v0.2 and formalizes the requirements most likely to matter in field and regulatory use:

1. sensing technology is unknown and must remain replaceable;
2. sensor anomalies precede diagnosis and cannot use diagnostic confidence terms;
3. the system needs explicit competing hypotheses and next-best evidence requests;
4. specimen identity and chain of custody must be defensible;
5. diagnostic results must be interpreted in light of method applicability;
6. scientific determinations must remain distinct from regulatory/reporting decisions;
7. downstream NPDN and CAP semantics must not be conflated.

The initial operating cluster is Arkansas, Louisiana, Missouri, Oklahoma, and Texas. Those jurisdictions are represented as data so the scientific evidence model remains portable.

# 1. Product model

~~~text
Survey
  -> Observation
  -> Anomaly
  -> Sensor indication
  -> Competing diagnostic hypotheses
  -> Next-best observation / sampling recommendation
  -> Physical specimen
  -> Custody events
  -> Diagnostic procedure
  -> Diagnostic result
  -> Scientific detection assertion
  -> Regulatory/reporting evaluation
  -> Alert / notification
~~~

Each arrow is a change in epistemic status or operational state. No arrow is equivalence.

# 2. Sensor agnosticism

v0.2 began with `Flight` and `SpectralAnomaly`. Both remain, but only as subtypes.

The new roots are:

~~~text
SurveyActivity
SensorObservation
ObservedAnomaly
~~~

A `Flight` is a `SurveyActivity`.

A `SpectralAnomaly` is an `ObservedAnomaly`.

The schema uses SOSA/SSN for external sensor and platform semantics rather than creating a local hardware taxonomy.

This permits later integration of thermal, multispectral, hyperspectral, fluorescence, fixed-station, ground-platform, satellite-derived, or other sensing systems without changing the evidence model.

# 3. Confidence refactor

The v0.2 model treated Confirmed, Suspected, PreSymptomatic, NotDetected, and Undetermined as a single ranked `ConfidenceTier`.

That model was internally inconsistent because its own documentation argued that pre-symptomatic indication was not a weaker form of Suspected.

v0.3 separates three axes.

## Evidence stage

- Sensor indication
- Field observation
- Specimen evidence
- Diagnostic evidence
- Confirmatory evidence

## Diagnostic disposition

- Confirmed
- Suspected
- Not Detected
- Undetermined

## Confidence assessment

- evidence strength;
- evidence completeness;
- model applicability;
- assay applicability;
- provenance quality;
- optional calibrated probability.

`PreSymptomatic` is retained only as a deprecated compatibility value.

The correct v0.3 representation is a `SensorIndicationAssertion` with evidence stage `SensorIndicationStage`.

# 4. Sensor indication cannot assert pathogen presence

The sensor stage is weaker than diagnosis in kind, not merely in degree.

A valid sensor indication says:

> An anomaly warrants further investigation.

It does not say:

> Pathogen X is present.

The SHACL suite rejects `assertsPathogen` on a `SensorIndicationAssertion`.

If a model proposes a possible pathogen, that proposal is represented as a `DiagnosticHypothesis`, not a detection.

# 5. Hypothesis management

v0.3 adds:

~~~text
DiagnosticHypothesis
DiagnosticCandidateSet
ObservationRequirement
SamplingRecommendation
~~~

A candidate set allows several causal explanations to remain live.

Each hypothesis may carry a candidate rank, an optional calibrated probability, a proposed causal agent, and supporting/contradicting evidence through the upper assertion model.

The ontology does not define the decision algorithm. It provides the objects needed for an external reasoning service to ask:

> What observation would most efficiently discriminate among the remaining candidates?

# 6. Spatial support

A detection should not automatically inherit the extent of the field containing the sampled plant.

v0.3 introduces `SpatialSupportDescription` and support kinds including point, plant, row, polygon, management zone, field, raster footprint, sensor footprint, and sampling area.

The purpose is to make the evidentiary footprint explicit.

# 7. Custody as explicit events

v0.2 represented a custody chain but did not formalize its constituent events.

v0.3 introduces:

~~~text
CustodyEvent
  SampleCollection
  TransferEvent
  ReceiptEvent
  StorageEvent
  AliquotEvent
~~~

Relevant events can identify the specimen/aliquot, timestamp, responsible agent, releasing custodian, receiving custodian, container identifier, seal identifier, integrity status, and previous custody event.

The model separates `CustodyChain`, the sequence of real processes, from `CustodyRecord`, the information artifact documenting those processes.

This permits the ontology to represent an incomplete or disputed record without pretending the physical history ceased to exist.

# 8. Specimen genealogy

`Specimen` and `Aliquot` are distinct.

An aliquot is a physical portion of a source specimen and receives its own identity.

`AliquotEvent` records the source specimen, produced aliquot, and event time.

This supports parallel testing and retained archives while preserving traceability to the original field collection.

# 9. Diagnostic procedures and applicability

The schema generalizes `Assay` to `DiagnosticProcedure`. An assay remains one subtype.

A diagnostic procedure consumes one specimen/aliquot per procedure event and produces one result datum per event. A repeat is a new procedure event.

`DiagnosticResult` is separate from the final detection assertion and has one procedure-level status:

- PositiveResult
- NegativeResult
- InconclusiveResult
- BelowDetectionLimitResult

`DiagnosticProcedureProfile` represents method-validity information such as validated pathogen, host, specimen matrix, sensitivity, specificity, detection limit, and validation source.

# 10. Negative evidence

v0.3 explicitly rejects flattening all negative-looking events into `NotDetected`.

The following differ:

~~~text
not surveyed
surveyed with no anomaly
anomaly observed but not sampled
sample collected but not tested
negative diagnostic result
result below detection limit
diagnostic disposition Not Detected
~~~

`examples/negative-survey.ttl` demonstrates the distinction.

# 11. Scientific versus regulatory assertions

v0.3 introduces:

~~~text
DiagnosticDetectionAssertion
ConfirmedDetectionAssertion
RegulatoryDetermination
ReportingDecision
Alert
~~~

A scientific detection is a claim about diagnostic evidence.

A regulatory determination is a claim made under an authority or rule.

A reporting decision is a decision about transmission.

An alert is directive information.

They may be causally connected, but they are not the same record.

# 12. Initial jurisdiction model

The first operating cluster is represented by five `OperationalJurisdiction` individuals:

~~~text
Arkansas  US-AR
Louisiana US-LA
Missouri  US-MO
Oklahoma  US-OK
Texas     US-TX
~~~

States are not subclasses of detection.

A `ReportingRule` or determination can be linked to the jurisdiction in which it applies.

# 13. NPDN crosswalk

The NPDN National Data Repository uses four diagnostic-confidence values:

~~~text
Confirmed
Suspected
Not Detected
Undetermined
~~~

v0.3 represents direct mappings from Black Mesa diagnostic dispositions to those terms.

The critical non-mapping is:

~~~text
SensorIndicationStage -> NPDN diagnostic confidence = NoMapping
~~~

A sensor-only indication is not a diagnostic record and must not be collapsed into Suspected.

# 14. CAP boundary

OASIS CAP 1.2 describes alert information using dimensions including urgency, severity, and certainty.

CAP certainty is not diagnostic confidence.

The crosswalk therefore rejects direct equivalence such as:

~~~text
Confirmed == CAP Observed
Suspected == CAP Likely
~~~

A reporting rule may derive CAP values when enough jurisdictional and policy context exists, but the ontology does not assert those equivalences globally.

# 15. Validation contract

The revised SHACL suite is designed to reject:

- local classes with no BFO anchor;
- sensor indications that assert pathogens;
- sensor-stage confidence with no model-applicability assessment;
- diagnostic detections with no disposition;
- diagnostic detections with no custody record;
- diagnostic confidence with no assay-applicability assessment;
- transfer events with missing custodians;
- imagery references with embedded tile/pixel/band properties;
- crosswalks with no fidelity;
- crosswalks claiming a mapping but naming no target term.

The test fixture contains deliberate failures so the project knows these rules actually fire.

# 16. Migration from v0.2

Existing terms retained:

~~~text
Farm
Field
Zone
Flight
SpectralAnomaly
Assay
AssayResult
Detection
ConfidenceTier
PreSymptomatic
~~~

Migration rules:

~~~text
Flight -> keep; subtype of SurveyActivity
SpectralAnomaly -> keep; subtype of ObservedAnomaly
Assay -> keep; subtype of DiagnosticProcedure
AssayResult -> keep; subtype of DiagnosticResult
Detection -> deprecated; use DiagnosticDetectionAssertion
ConfidenceTier -> deprecated
PreSymptomatic -> deprecated; use SensorIndicationAssertion + SensorIndicationStage
~~~

Old data should be transformed rather than silently reinterpreted.

# 17. Deliberate deferrals

v0.3 does not yet attempt to model specific sensor hardware, specific pilot pathogen/crop pairs, full environmental context, epidemiological spread, vector populations, treatment outcomes, state-by-state reporting law, alert transport, automated information-gain algorithms, a full LIMS, or a full crop/pathogen taxonomy.

Those should be added against real use cases.

# 18. Phase 1 success

A Phase 1 demonstration should show:

1. a sensor-agnostic survey record;
2. an anomaly and sensor indication that do not overclaim diagnosis;
3. a ranked candidate set;
4. a targeted sample;
5. continuous specimen/aliquot custody;
6. a diagnostic method and result;
7. a method-applicability assessment;
8. a versioned scientific detection assertion;
9. a jurisdiction-aware reporting evaluation;
10. traceability back to the originating observation and external sensor artifact.

That is the criterion against which further ontology growth should be judged.
