# Worked example: confidence

A generic field such as:

```text
confidence = HIGH
```

is insufficient because it hides why an assertion deserves weight.

## Sensor-stage example without probability

```text
evidence strength       = StrongEvidence
evidence completeness   = PartialEvidence
model applicability     = ValidatedApplicability
provenance quality      = CompleteProvenance
calibrated probability  = absent
```

The missing probability is meaningful: no calibrated probability has been asserted.

## With a calibrated probability

```turtle
ex:Confidence a bmo:ConfidenceAssessment ;
    bmo:evidenceStrength bmo:ModerateEvidence ;
    bmo:evidenceCompleteness bmo:PartialEvidence ;
    bmo:modelApplicability bmo:ValidatedApplicability ;
    bmo:provenanceQuality bmo:CompleteProvenance ;
    bmo:calibratedProbability "0.72"^^xsd:decimal .
```

SHACL constrains the value to [0,1], but that range does not prove calibration. Calibration is an external model-validation fact.

A candidate rank or arbitrary model score must not be relabeled as probability without calibration evidence.
