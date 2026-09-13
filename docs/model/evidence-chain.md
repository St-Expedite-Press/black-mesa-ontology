# Evidence chain

The Black Mesa core is an auditable sequence of evidence transformations.

```mermaid
flowchart LR
    SURVEY[SurveyActivity] --> OBS[SensorObservation]
    OBS --> ANOM[ObservedAnomaly]
    ANOM --> IND[SensorIndicationAssertion]
    IND --> HYP[DiagnosticHypothesis]
    HYP --> SAMPLE[SampleCollection]
    SAMPLE --> SPEC[Specimen]
    SPEC --> PROC[DiagnosticProcedure]
    PROC --> RESULT[DiagnosticResult]
    RESULT --> DET[DiagnosticDetectionAssertion]
    DET --> REG[RegulatoryDetermination]
    REG --> REP[ReportingDecision]
    REP --> ALERT[Alert]
```

| Stage | Object | May establish | Must not silently imply |
|---|---|---|---|
| survey | `SurveyActivity` | surveillance occurred | anomaly/pathogen |
| observation | `SensorObservation` | observation occurred | abnormality/diagnosis |
| anomaly | `ObservedAnomaly` | departure from reference | causal agent |
| indication | `SensorIndicationAssertion` | investigation warranted | pathogen presence |
| hypothesis | `DiagnosticHypothesis` | candidate cause | detection |
| collection | `SampleCollection` | identified material collected | diagnosis |
| result | `DiagnosticResult` | procedure outcome | field-wide presence/absence |
| detection | `DiagnosticDetectionAssertion` | scientific diagnostic assertion | regulatory action |
| regulatory determination | `RegulatoryDetermination` | rule-dependent conclusion | altered scientific evidence |
| reporting decision | `ReportingDecision` | external-reporting decision | diagnostic confidence |
| alert | `Alert` | directive/notification | independent scientific proof |

A sensor indication derives from anomaly evidence, concerns a zone, records stage/confidence/version/time, and cannot use `assertsPathogen`.

A diagnostic detection has a higher evidentiary contract: pathogen, diagnostic result(s), evidence stage, disposition, confidence with assay applicability, custody record, generating version, and assertion time. A `ConfirmedDetectionAssertion` additionally requires `Confirmed` at `ConfirmatoryEvidenceStage`.

The scientific assertion remains stable even if policy changes. See [regulatory boundary](regulatory-boundary.md).
