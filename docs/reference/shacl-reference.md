<!-- GENERATED FILE — DO NOT EDIT BY HAND. Rebuild with: python tools/schema_docs.py --schema schema --out docs/reference -->

# SHACL reference

Generated from `schema/shapes.ttl`. This is a structural index of current validation messages; [validation and CI](../operations/validation-and-ci.md) explains what the constraints do and do not prove.

## `bmo:UpperAnchorShape`

**Target:** `owl:Class`

Validation messages:

- UNANCHORED CLASS: every Black Mesa class must reach BFO via the shared upper module.

## `bmo:ImageryReferenceShape`

**Target:** `bmo:ImageryReference`

Validation messages:

- An imagery reference must carry exactly one storage URI.
- An imagery reference must carry exactly one checksum.

## `bmo:NoTiledImageryShape`

**Target:** `bmo:ImageryReference`

Validation messages:

- GRAPH BOUNDARY VIOLATION: imagery and dense sensor arrays must be referenced, not expanded into per-pixel, per-tile, or per-band triples.

## `bmo:SensorIndicationShape`

**Target:** `bmo:SensorIndicationAssertion`

Validation messages:

- A sensor indication must concern exactly one operational zone.
- A sensor indication must derive from at least one observed anomaly.
- A sensor indication must carry one confidence assessment with model applicability recorded.
- A sensor indication must be explicitly marked as the sensor-indication evidence stage.
- A sensor indication cannot assert pathogen presence. Create a diagnostic hypothesis instead.
- A sensor indication must record the model or rule version that generated it.
- A sensor indication must record its assertion time.

## `bmo:DiagnosticDetectionShape`

**Target:** `bmo:DiagnosticDetectionAssertion`

Validation messages:

- A diagnostic detection must concern exactly one operational zone.
- A diagnostic detection must identify exactly one asserted pathogen taxon or canonical external identifier.
- A diagnostic detection must derive from at least one diagnostic result.
- A diagnostic detection must carry one confidence assessment with assay applicability recorded.
- A diagnostic detection must state its evidence stage.
- A diagnostic detection must state one diagnostic disposition: Confirmed, Suspected, Not Detected, or Undetermined.
- A diagnostic detection must carry one custody record for the physical evidence on which it relies.
- A diagnostic detection must record the rule or method version in force when it was produced.
- A diagnostic detection must record its assertion time.
- A scientific detection may trigger at most one direct alert record; alert policy remains separate.

## `bmo:ConfirmedDetectionShape`

**Target:** `bmo:ConfirmedDetectionAssertion`

Validation messages:

- A ConfirmedDetectionAssertion must have diagnostic disposition Confirmed.
- A ConfirmedDetectionAssertion must be at the confirmatory evidence stage.

## `bmo:ConfidenceAssessmentShape`

**Target:** `bmo:ConfidenceAssessment`

Validation messages:

- Calibrated probability, when present, must be a single decimal in [0,1].
- Confidence must state evidence strength.
- Confidence must state evidence completeness.
- Confidence must state provenance quality.

## `bmo:SensorConfidenceShape`

**Target:** `— nested/node shape`

Validation messages:

- Sensor-stage confidence must record model applicability.

## `bmo:DiagnosticConfidenceShape`

**Target:** `— nested/node shape`

Validation messages:

- Diagnostic confidence must record assay applicability.

## `bmo:SampleCollectionShape`

**Target:** `bmo:SampleCollection`

Validation messages:

- A sample collection must yield at least one identified specimen.
- A sample collection must record the zone in which it occurred.
- A sample collection must record collection time.
- A sample collection must identify the responsible collector or collection system.

## `bmo:CustodyRecordShape`

**Target:** `bmo:CustodyRecord`

Validation messages:

- A custody record must contain at least one custody event.

## `bmo:TransferEventShape`

**Target:** `bmo:TransferEvent`

Validation messages:

- A transfer event must identify exactly one specimen or aliquot.
- A transfer event must identify the releasing custodian.
- A transfer event must identify the receiving custodian.
- A transfer event must record its timestamp.
- A transfer event must identify the responsible agent.
- A custody event may name at most one immediate predecessor.

## `bmo:ReceiptEventShape`

**Target:** `bmo:ReceiptEvent`

Validation messages:

- A receipt event must identify exactly one specimen or aliquot.
- A receipt event must identify the receiving custodian.
- A receipt event must record its timestamp.
- A receipt event must identify the responsible receiving agent.

## `bmo:AliquotEventShape`

**Target:** `bmo:AliquotEvent`

Validation messages:

- An aliquot event must identify the source specimen.
- An aliquot event must identify at least one produced aliquot.
- An aliquot event must record its timestamp.

## `bmo:DiagnosticProcedureShape`

**Target:** `bmo:DiagnosticProcedure`

Validation messages:

- A diagnostic procedure must use exactly one specimen or aliquot input. A rerun or second specimen is a separate procedure event.
- A diagnostic procedure must produce exactly one result datum.

## `bmo:DiagnosticResultShape`

**Target:** `bmo:DiagnosticResult`

Validation messages:

- A diagnostic result must have exactly one result status.
- A diagnostic result must identify the procedure that generated it.

## `bmo:DiagnosticProcedureProfileShape`

**Target:** `bmo:DiagnosticProcedureProfile`

Validation messages:

- Sensitivity, when present, must be a decimal in [0,1].
- Specificity, when present, must be a decimal in [0,1].

## `bmo:ObservationRequirementShape`

**Target:** `bmo:ObservationRequirement`

Validation messages:

- An observation requirement must state which candidates it is intended to discriminate.

## `bmo:ReportingCrosswalkShape`

**Target:** `bmo:ReportingCrosswalk`

Validation messages:

- A reporting crosswalk must name exactly one internal source concept.
- A reporting crosswalk must state the external target scheme.
- A reporting crosswalk must state fidelity: exact, broader, narrower, partial, or none.
- A mapped crosswalk (fidelity other than none) must name exactly one crosswalkTo target term.
- A NoMapping crosswalk records that no defensible target exists and therefore must not name crosswalkTo.

## `bmo:PilotPathosystemShape`

**Target:** `bmo:PilotPathosystem`

Validation messages:

- A pilot pathosystem must identify exactly one canonical host taxon.
- A pilot pathosystem must identify exactly one canonical pathogen taxon.
- A pilot pathosystem must state whether it is an operational pilot or regulatory stress test.

## `bmo:ReportingRuleShape`

**Target:** `bmo:ReportingRule`

Validation messages:

- Every reporting rule must have one stable rule identifier.
- Every reporting rule must identify at least one jurisdiction in which it applies.
- Every jurisdictional reporting rule must identify the regulatory authority responsible for the source rule.
- Every jurisdictional reporting rule must cite at least one authoritative source.
- Every reporting rule must state its legal/regulatory review status.
- Every reporting rule must explicitly state whether human review is required.
- A draft rule must require human review; draft legal interpretations are never machine-executable external-notification authority.
- A draft rule must carry a legal review note identifying what still requires verification.
- An approved rule must record an effective-from date.
