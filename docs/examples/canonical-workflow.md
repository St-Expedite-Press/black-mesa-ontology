# Worked example: canonical workflow

Executable source: [`examples/canonical-workflow.ttl`](../../examples/canonical-workflow.ttl).

The file is intentionally generic. Sensor, crop, pathogen, and assay identities are placeholders; deployments should use governed external identifiers where available.

## 1. Site

The example creates a farm, field, and zone. These are physical/managed places.

## 2. Survey and observation

A `Flight` (subtype of `SurveyActivity`) uses a SOSA sensor/platform and creates a `SensorObservation`.

What may be established: an observation happened. What must not yet be inferred: anomaly or pathogen.

## 3. Anomaly and artifact

The example creates `ObservedAnomaly` and an `ImageryReference` with storage URI + checksum. The anomaly says the observation departed from reference conditions; it does not say why.

## 4. Sensor indication

```turtle
ex:Indication-100 a bmo:SensorIndicationAssertion ;
    bmo:concernsZone ex:Zone-17 ;
    bmo:derivedFromAnomaly ex:Anomaly-100 ;
    bmo:hasEvidenceStage bmo:SensorIndicationStage ;
    bmo:hasConfidenceAssessment ex:SensorConfidence-100 ;
    up:generatedUnder ex:Model-v3 ;
    prov:generatedAtTime "2026-09-12T15:00:00Z"^^xsd:dateTime .
```

SHACL requires stage, provenance, time, anomaly source, zone, and confidence. It prohibits `assertsPathogen`.

## 5. Competing hypotheses

The example retains a pathogen hypothesis and water-stress hypothesis. Candidate probability/rank remain hypothesis metadata, not detection.

## 6. Collection and custody

`SampleCollection` creates `Specimen-100`, assigns collection time/agent/container/seal, and anchors material to the zone. Transfer and receipt events name custodians, time, predecessor, container/seal, and integrity. A `CustodyRecord` gathers those events.

## 7. Diagnostic evidence

An `Assay` uses the specimen and produces an `AssayResult`. The positive result remains separate from the later scientific assertion. A separate confidence assessment records assay applicability and evidentiary axes.

## 8. Scientific detection

```turtle
ex:Detection-100 a bmo:ConfirmedDetectionAssertion ;
    bmo:concernsZone ex:Zone-17 ;
    bmo:assertsPathogen ex:Pathogen-Alpha ;
    bmo:derivedFromResult ex:Result-100 ;
    bmo:hasCustodyRecord ex:CustodyRecord-100 ;
    bmo:hasEvidenceStage bmo:ConfirmatoryEvidenceStage ;
    bmo:hasDiagnosticDisposition bmo:Confirmed ;
    bmo:hasConfidenceAssessment ex:DiagnosticConfidence-100 ;
    up:generatedUnder ex:DiagnosticRule-v2 ;
    prov:generatedAtTime "2026-09-12T19:00:00Z"^^xsd:dateTime .
```

This is the scientific determination. It does not by itself authorize notification or regulated action.
