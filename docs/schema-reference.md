# Black Mesa v0.3 schema reference

This is the review-oriented reference for the current ontology. The canonical machine-readable definitions are in:

- [bmo-core.ttl](../schema/bmo-core.ttl)
- [reporting-crosswalks.ttl](../schema/reporting-crosswalks.ttl)
- [shapes.ttl](../schema/shapes.ttl)

For a plain-language introduction, read [team-guide.md](team-guide.md). For end-to-end diagrams and rationale, read [architecture.md](architecture.md).

The exhaustive table/diagram files can be regenerated from Turtle with:

~~~bash
python tools/schema_docs.py --schema schema --out docs
~~~

## Core semantic rule

The ontology keeps the following sequence distinct:

~~~text
observation
!= anomaly
!= sensor indication
!= diagnostic hypothesis
!= diagnostic result
!= scientific detection
!= regulatory determination
!= alert
~~~

## Places and spatial support

| Term | Meaning |
|---|---|
| `Farm` | Managed agricultural holding. |
| `Field` | Bounded cultivated area within a farm. |
| `Zone` | Sub-field operational area used for surveillance, sampling, or management. |
| `SpatialSupportDescription` | Description of the footprint over which evidence or an assertion is warranted. |
| `SupportKind` | Controlled concept for point, plant, row, polygon, management zone, field, raster footprint, sensor footprint, or sampling area. |

Important relations: `partOfSite`, `hasSpatialSupport`, `supportKind`.

## Sensor-agnostic surveillance

| Term | Meaning |
|---|---|
| `SurveyActivity` | Generic surveillance activity independent of platform or modality. |
| `Flight` | Aerial survey subtype retained for the initial drone use case. |
| `SensorObservation` | Observation event aligned to SOSA. |
| `ObservedAnomaly` | Derived record of deviation from an expected/reference condition. |
| `SpectralAnomaly` | Spectral subtype of observed anomaly. |
| `ImageryReference` | URI + checksum reference to a large sensor artifact stored outside RDF. |

Important relations: `usesSensor`, `hostedByPlatform`, `madeObservation`, `observedAnomaly`, `derivedFromObservation`, `referencesImagery`.

## Hypothesis and adaptive evidence gathering

| Term | Meaning |
|---|---|
| `DiagnosticHypothesis` | Revisable causal hypothesis; may concern a pathogen or non-pathogen stressor. |
| `DiagnosticCandidateSet` | Current competing hypotheses retained by the system. |
| `ObservationRequirement` | Request for an observation that would discriminate among candidates. |
| `SamplingRecommendation` | Directive specifying what material should be collected, where, and why. |

Important relations/data: `hasCandidate`, `hypothesizesAgent`, `candidateProbability`, `candidateRank`, `expectedInformationGain`, `expectedCost`.

## Custody and physical evidence

| Term | Meaning |
|---|---|
| `Specimen` | Persistently identified material collected from the field. |
| `Aliquot` | Persistently identified physical portion of a source specimen. |
| `Container` | Physical vessel associated with custody. |
| `CustodyEvent` | Generic process affecting identity, possession, location, or integrity. |
| `SampleCollection` | Collection process and first custody event. |
| `TransferEvent` | Transfer between custodians. |
| `ReceiptEvent` | Receipt by a lab/facility/custodian. |
| `StorageEvent` | Controlled storage event. |
| `AliquotEvent` | Subdivision of a specimen into one or more aliquots. |
| `CustodyChain` | Real ordered sequence of custody-related processes. |
| `CustodyRecord` | Information record describing the custody chain. |

Important relations/data: `yieldedSpecimen`, `custodySubject`, `fromCustodian`, `toCustodian`, `eventAgent`, `eventTime`, `previousCustodyEvent`, `sourceSpecimen`, `producedAliquot`, `containerIdentifier`, `sealIdentifier`, `tamperStatus`.

## Diagnostics

| Term | Meaning |
|---|---|
| `DiagnosticProcedure` | Generic analysis process performed on a specimen/aliquot. |
| `Assay` | Diagnostic-procedure subtype retained for compatibility. |
| `DiagnosticResult` | Result datum produced by one diagnostic procedure. |
| `AssayResult` | Assay-specific subtype of diagnostic result. |
| `DiagnosticProcedureProfile` | Versioned record of method validation and applicability. |
| `DetectionLimit` | Validated threshold below which a method cannot reliably distinguish presence from absence. |
| `DiagnosticResultStatus` | Procedure-level status: positive, negative, inconclusive, below detection limit. |

Important relations/data: `usedSpecimen`, `producedResult`, `producedByProcedure`, `resultStatus`, `validatedForPathogen`, `validatedForHost`, `validatedForMatrix`, `sensitivity`, `specificity`, `hasDetectionLimit`, `validationSource`.

## Evidence stage

`EvidenceStage` answers: **where in the investigation did this evidence come from?**

Current values:

- `SensorIndicationStage`
- `FieldObservationStage`
- `SpecimenEvidenceStage`
- `DiagnosticEvidenceStage`
- `ConfirmatoryEvidenceStage`

Evidence stage is not a confidence ranking.

## Diagnostic disposition

`DiagnosticDisposition` answers: **what did the diagnostic work conclude?**

Current values:

- `Confirmed`
- `Suspected`
- `NotDetected`
- `Undetermined`

`NotDetected` is reserved for diagnostic interpretation. It does not mean “surveyed with no sensor anomaly.”

## Confidence

`ConfidenceAssessment` is separate from both evidence stage and diagnostic disposition.

It may carry:

| Axis | Vocabulary / value |
|---|---|
| calibrated probability | decimal in [0,1], only when produced by a calibrated model |
| evidence strength | weak / moderate / strong / very strong |
| evidence completeness | incomplete / partial / substantial / complete |
| model applicability | validated / partial / outside validated scope / unknown |
| assay applicability | validated / partial / outside validated scope / unknown |
| provenance quality | complete / minor gap / major gap / compromised |

The old `ConfidenceTier` and `PreSymptomatic` terms are deprecated compatibility terms.

## Assertion layers

| Term | What it is allowed to claim |
|---|---|
| `SensorIndicationAssertion` | An anomaly warrants investigation. It may not assert pathogen presence. |
| `DiagnosticHypothesis` | A possible causal explanation. |
| `DiagnosticDetectionAssertion` | Scientific determination about a specified pathogen based on diagnostic evidence. |
| `ConfirmedDetectionAssertion` | Detection with Confirmed disposition and confirmatory evidence stage. |
| `RegulatoryDetermination` | Determination under an authorized regulatory/reporting rule. |
| `ReportingDecision` | Decision about whether/how to transmit the scientific record externally. |
| `Alert` | Directive/notification generated in the policy layer. |

Important relations: `derivedFromAnomaly`, `assertsPathogen`, `derivedFromResult`, `hasCustodyRecord`, `hasEvidenceStage`, `hasDiagnosticDisposition`, `hasConfidenceAssessment`, `triggeredAlert`.

## Jurisdiction and reporting

| Term | Meaning |
|---|---|
| `OperationalJurisdiction` | Jurisdiction relevant to deployment or reporting. |
| `ReportingRule` | Versioned rule governing when/how a record should be reported. |
| `ExternalReportingScheme` | External vocabulary, repository, or message standard. |
| `ExternalReportingTerm` | Project-local proxy for an external term where no stable RDF identifier is published. |
| `ReportingCrosswalk` | Directional mapping carrying explicit fidelity. |

Initial jurisdiction individuals:

- `Arkansas` — US-AR
- `Louisiana` — US-LA
- `Missouri` — US-MO
- `Oklahoma` — US-OK
- `Texas` — US-TX

Crosswalk fidelity comes from the shared upper module:

- `Exact`
- `Broader`
- `Narrower`
- `Partial`
- `NoMapping`

`NoMapping` is a valid scientific/interoperability finding, not an error.

## NPDN crosswalk

Black Mesa diagnostic dispositions map directly to the NPDN NDR diagnostic-confidence values:

| Black Mesa | NPDN |
|---|---|
| Confirmed | Confirmed |
| Suspected | Suspected |
| NotDetected | Not Detected |
| Undetermined | Undetermined |

`SensorIndicationStage` explicitly has `NoMapping` to NPDN diagnostic confidence.

## CAP boundary

CAP 1.2 is represented as an external alert scheme.

The ontology explicitly refuses global direct mappings from diagnostic dispositions to CAP certainty. Alert certainty is derived under a reporting policy, not inferred by synonymy.

## High-consequence SHACL contracts

The validation layer currently enforces, among other things:

- every local class reaches BFO;
- imagery references have one URI and one checksum;
- dense pixel/tile/band content is rejected from imagery references;
- sensor indications derive from anomalies and cannot assert pathogen presence;
- sensor-stage confidence records model applicability;
- diagnostic detections identify pathogen, result, evidence stage, disposition, confidence, custody record, rule version, and assertion time;
- confirmed detections have Confirmed disposition and confirmatory evidence stage;
- sample collections create identified specimens and record place/time/agent;
- transfer events identify both custodians;
- diagnostic procedures use one specimen/aliquot and produce one result per procedure event;
- reporting crosswalks state source, target scheme, and fidelity;
- a non-`NoMapping` crosswalk names a target term;
- a `NoMapping` crosswalk must not pretend to have a target term.

## Compatibility terms

The following v0.2 terms remain only to make migration explicit:

- `Detection` → deprecated; use `DiagnosticDetectionAssertion`
- `ConfidenceTier` → deprecated
- `PreSymptomatic` → deprecated; use `SensorIndicationAssertion` + `SensorIndicationStage`

Do not create new data using the deprecated terms.


## v0.4 persistent identity

- Ontology IRI: `https://w3id.org/black-mesa/bmo`
- Term namespace: `https://w3id.org/black-mesa/bmo/`
- Version IRI: `https://w3id.org/black-mesa/bmo/releases/0.4.0`
- Upper ontology IRI: `https://w3id.org/black-mesa/upper`
- Ontology license: CC BY 4.0

## Pilot pathosystem profile

| Term | Meaning |
|---|---|
| `PilotPathosystem` | Reference-data profile selecting one host/pathogen pair for a pilot or stress test. |
| `PilotScenarioRole` | Role of the profile in the program. |
| `OperationalPilot` | End-to-end operational evidence workflow pilot. |
| `RegulatoryStressTest` | Scenario selected primarily to exercise regulatory/reporting behavior. |
| `hostTaxon` | Canonical external host taxon IRI. |
| `pathogenTaxon` | Canonical external pathogen taxon IRI. |
| `scenarioRole` | Operational-pilot or regulatory-stress-test role. |

## Reporting-rule governance additions

| Term | Meaning |
|---|---|
| `RuleReviewStatus` | Governance status of a jurisdictional rule record. |
| `DraftRequiresLegalRegulatoryReview` | Non-operative draft; cannot authorize external action. |
| `ApprovedRule` | Rule record reviewed for operational decision support. |
| `SupersededRule` | Historical rule retained for interpretation. |
| `RegulatoryActionType` | Controlled action concept such as regulatory evaluation or external notification. |
| `ruleIdentifier` | Stable identifier for the rule record. |
| `regulatoryAuthority` | Responsible external authority. |
| `effectiveFrom` / `effectiveUntil` | Temporal validity after verification. |
| `regulatedTaxon` / `regulatedHost` / `regulatedCommodity` / `regulatedArea` | Scope of the verified rule. |
| `triggerEvidenceStage` | Evidence stage capable of activating the reviewed rule. |
| `triggerDiagnosticDisposition` | Diagnostic disposition capable of activating the reviewed rule. |
| `requiredConfirmationMethod` | Confirmation method required by the reviewed rule. |
| `requiresHumanReview` | Human-approval gate. |
| `requiredAction` | Action required under the reviewed rule. |
| `notificationRecipient` / `notificationDeadline` | Verified reporting destination and timing. |
| `movementRestrictionRequired` | Whether movement restriction is part of the reviewed rule. |
| `supersedesRule` | Historical-version relation. |
| `ruleReviewStatus` | Current governance state. |
| `legalReviewNote` | Outstanding interpretation questions. |

SHACL requires all jurisdictional rule records to identify jurisdiction, authority, authoritative source, review status, and the human-review setting. Drafts must require human review and carry a review note. Approved rules must record an effective-from date.
