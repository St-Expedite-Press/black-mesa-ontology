# Sensing and anomalies

Black Mesa begins with `SurveyActivity`, not flight. `Flight` is a subtype retained for expected aerial deployments; other platforms can enter without redesign.

`SensorObservation` is an observation event. `ObservedAnomaly` is a derived datum saying an observation differs from an expected/reference condition. `SpectralAnomaly` is only one subtype.

The core does not maintain a local hardware taxonomy. Sensors and platforms should use SOSA/SSN-aligned identities.

## External sensor artifacts

`ImageryReference` points to bulk evidence outside RDF and requires a storage URI and checksum. SHACL rejects the project pattern of expanding imagery into per-pixel, per-tile, or per-band local triples.

## Valid sensor indication

```turtle
ex:Indication-100 a bmo:SensorIndicationAssertion ;
    bmo:concernsZone ex:Zone-17 ;
    bmo:derivedFromAnomaly ex:Anomaly-100 ;
    bmo:hasEvidenceStage bmo:SensorIndicationStage ;
    bmo:hasConfidenceAssessment ex:SensorConfidence-100 ;
    up:generatedUnder ex:Model-v3 ;
    prov:generatedAtTime "2026-09-12T15:00:00Z"^^xsd:dateTime .
```

## Prohibited interpretation

```turtle
ex:BadIndication a bmo:SensorIndicationAssertion ;
    bmo:assertsPathogen obo:NCBITaxon_318829 .
```

That pattern fails the semantic contract: a sensor indication cannot assert pathogen presence. Create a `DiagnosticHypothesis` for candidate causes and obtain physical/diagnostic evidence before a diagnostic detection assertion.

An anomaly can be associated with disease, drought, flooding, nutrient stress, chemical injury, insect activity, sensor artifact, or an unknown cause. The anomaly alone does not decide among them.
