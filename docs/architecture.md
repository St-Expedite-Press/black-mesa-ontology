# Black Mesa architecture

This document explains how the ontology corresponds to the product. It is written for engineers, plant pathologists, operators, data scientists, and project leadership.

The shortest useful description is:

> Black Mesa is a sensor-agnostic agricultural biosecurity evidence system. It discovers anomalies, retains competing causal hypotheses, directs targeted physical sampling, preserves legally defensible specimen custody, integrates diagnostic evidence, and produces auditable scientific determinations that can be evaluated under jurisdiction-specific reporting rules.

The ontology is the semantic contract joining those stages. It is not the computer-vision model, the laboratory information system, the flight controller, the object store, or the regulatory policy engine.

## 1. System layers

~~~mermaid
flowchart TB
    subgraph SENSING["1. Sensing"]
      SA[Survey Activity]
      SO[Sensor Observation]
      OA[Observed Anomaly]
      IR[External Sensor Artifact<br/>URI + checksum]
      SA --> SO --> OA
      OA -. references .-> IR
    end

    subgraph HYP["2. Hypothesis"]
      SI[Sensor Indication Assertion]
      CS[Candidate Set]
      DH[Diagnostic Hypotheses]
      NR[Next-best Requirement]
      SI --> CS --> DH
      DH --> NR
    end

    subgraph PHYS["3. Physical Evidence"]
      SC[Sample Collection]
      SP[Specimen]
      AL[Aliquot]
      CR[Custody Record]
      SC --> SP --> AL
      SC --> CR
    end

    subgraph DIAG["4. Diagnostics"]
      DP[Diagnostic Procedure]
      DR[Diagnostic Result]
      DC[Diagnostic Confidence]
      DP --> DR --> DC
    end

    subgraph SCI["5. Scientific Assertion"]
      DA[Diagnostic Detection Assertion]
      DISP[Diagnostic Disposition]
      ES[Evidence Stage]
      DA --> DISP
      DA --> ES
    end

    subgraph POLICY["6. Policy / Reporting"]
      RD[Regulatory Determination]
      RP[Reporting Decision]
      A[Alert / Notification]
      RD --> RP --> A
    end

    OA --> SI
    NR --> SC
    AL --> DP
    SP --> DP
    DR --> DA
    CR --> DA
    DA --> RD
~~~

The central design rule is that arrows represent transformations of evidence, not synonymy. An anomaly is not a detection. A detection is not a regulatory determination. A regulatory determination is not an alert.

## 2. Sensor-agnostic surveillance

The core schema begins with `SurveyActivity`, not `Flight`.

A drone sortie is represented as `Flight`, a subtype of `SurveyActivity`. Other platforms can enter without redesign:

~~~mermaid
classDiagram
    SurveyActivity <|-- Flight
    SurveyActivity --> SensorObservation : madeObservation
    SurveyActivity --> Sensor : usesSensor
    SurveyActivity --> Platform : hostedByPlatform
    SensorObservation --> ObservedAnomaly : interpreted into
    ObservedAnomaly <|-- SpectralAnomaly
    ObservedAnomaly --> ImageryReference : referencesImagery
~~~

This is why the ontology does not define a Black Mesa list of sensor types. Hardware-specific descriptions belong in SOSA/SSN-aligned instance data or dedicated device modules.

The graph stores survey identity, observation identity, sensor and platform identifiers, timestamps and provenance, anomaly records, spatial support, model/rule versions, derived hypotheses, and links to large sensor artifacts.

The graph does **not** store every pixel, every spectral band value for every pixel, video frames, raw sensor arrays, or dense point clouds. Those belong in object or analytical storage. The graph contains the URI and checksum required to retrieve and verify them.

## 3. Observation, anomaly, indication, hypothesis

These terms are deliberately different.

### Sensor observation

A measurement event performed by some device or procedure.

Example: a multispectral camera captures a pass over a field.

### Observed anomaly

A derived datum saying the observation differs from some expected/reference condition.

Example: a cluster of plants has a statistically unusual reflectance signature.

An anomaly says **something is different**. It does not say why.

### Sensor indication assertion

An evidentiary claim saying the anomaly warrants further investigation.

A sensor indication:

- is an assertion;
- has provenance;
- names the model/rule version that produced it;
- may carry a calibrated probability if one actually exists;
- cannot assert pathogen presence.

SHACL explicitly rejects a `SensorIndicationAssertion` that uses `assertsPathogen`.

### Diagnostic hypothesis

A candidate causal explanation.

Examples might include pathogen X, pathogen Y, water stress, nutrient stress, herbicide injury, insect damage, sensor artifact, or unknown cause.

Black Mesa should retain multiple hypotheses where the evidence does not distinguish them.

~~~mermaid
flowchart LR
    O[Observation] --> A[Anomaly]
    A --> I[Sensor indication]
    I --> H1[Hypothesis: pathogen]
    I --> H2[Hypothesis: water stress]
    I --> H3[Hypothesis: nutrient stress]
    H1 --> Q[What observation would best discriminate?]
    H2 --> Q
    H3 --> Q
~~~

This is the conceptual basis for later adaptive sampling and information-gain logic.

## 4. Next-best action

`ObservationRequirement` and `SamplingRecommendation` are directive information objects. They tell the execution layer what evidence would be most useful next.

They can eventually carry:

- which candidates they discriminate;
- expected information gain;
- expected cost;
- required equipment;
- time sensitivity;
- acceptable methods;
- required spatial support;
- required precision.

The ontology does not decide how expected information gain is calculated. That belongs in the decision service. The ontology records the requirement and why it exists.

## 5. Legally defensible chain of custody

v0.3 makes custody events explicit.

~~~mermaid
sequenceDiagram
    participant Site as Field / Zone
    participant Collector
    participant Courier
    participant Lab
    participant Analysis

    Site->>Collector: SampleCollection creates Specimen S
    Note over Collector: container ID + seal ID + time
    Collector->>Courier: TransferEvent
    Note over Collector,Courier: from / to custodian + integrity
    Courier->>Lab: ReceiptEvent
    Note over Courier,Lab: seal/tamper status + time
    Lab->>Analysis: DiagnosticProcedure uses S or an Aliquot
~~~

A custody event can record specimen/aliquot identity, event time, responsible agent, releasing custodian, receiving custodian, container identifier, seal identifier, tamper/integrity status, and immediately previous custody event.

The model distinguishes the **real custody process** (`CustodyChain`) from the **information record describing it** (`CustodyRecord`).

That distinction matters legally. The actual transfers occurred in the world; the graph contains claims about those transfers. Those claims can be incomplete, challenged, corrected, or audited.

### Specimen and aliquot

A specimen is the material collected from the field.

An aliquot is a physically separated portion of that specimen.

~~~mermaid
flowchart LR
    S[Specimen S-100] --> A1[Aliquot A]
    S --> A2[Aliquot B]
    S --> A3[Retained archive]
    A1 --> P1[qPCR]
    A2 --> P2[Sequencing]
~~~

Each aliquot gets its own identity and custody history while preserving lineage to the source specimen.

This prevents a common evidentiary failure: multiple test results appearing to refer to "the sample" when nobody can reconstruct which physical portion was actually tested.

## 6. Diagnostic procedure versus diagnostic result

`DiagnosticProcedure` is an event. `DiagnosticResult` is information produced by that event.

A result has one result status:

- positive;
- negative;
- inconclusive;
- below detection limit.

Those are **procedure results**, not necessarily the final diagnostic disposition.

A negative result must not automatically become "pathogen absent." The conclusion depends on the spatial and biological representativeness of the specimen, assay applicability, sensitivity/specificity, detection limit, specimen condition, chain-of-custody integrity, and other evidence.

## 7. Procedure applicability

`DiagnosticProcedureProfile` is where method-validity information belongs.

The profile can describe target pathogen, host, specimen matrix, sensitivity, specificity, limit of detection, validation source, and method version.

This lets Black Mesa distinguish:

> The assay returned negative.

from:

> The assay returned negative and is validated for this pathogen, host, and matrix.

Those claims carry different evidentiary weight.

## 8. Evidence stage is not diagnostic disposition

v0.2 put pre-symptomatic indication, suspected, confirmed, not detected, and undetermined into one ranked confidence scale. v0.3 removes that conflation.

### Evidence stage

Where the evidence came from in the workflow:

~~~text
Sensor indication
Field observation
Specimen evidence
Diagnostic evidence
Confirmatory evidence
~~~

### Diagnostic disposition

What the diagnostic process concluded:

~~~text
Confirmed
Suspected
Not Detected
Undetermined
~~~

### Confidence assessment

How much weight the assertion can bear:

~~~text
Evidence strength
Evidence completeness
Model applicability
Assay applicability
Provenance quality
Calibrated probability, when one exists
~~~

These dimensions are orthogonal.

A sensor-stage record might have:

~~~text
Evidence stage:          Sensor indication
Diagnostic disposition: none yet
Model applicability:     validated
Evidence strength:       moderate
Calibrated probability:  0.72
~~~

A later diagnostic record might have:

~~~text
Evidence stage:          Confirmatory evidence
Diagnostic disposition: Confirmed
Assay applicability:     validated
Evidence strength:       very strong
Provenance quality:      complete
~~~

The second record does not overwrite the first. Both describe the investigation history.

## 9. Negative evidence

The ontology must preserve the difference among:

~~~mermaid
flowchart TB
    A[Not surveyed]
    B[Surveyed; no anomaly recorded]
    C[Anomaly recorded; no sample obtained]
    D[Sample obtained; no diagnostic procedure]
    E[Diagnostic procedure negative]
    F[Diagnostic result below detection limit]
    G[Diagnostic disposition: Not Detected]
~~~

These are not interchangeable.

The repository's `examples/negative-survey.ttl` intentionally records a survey with no anomaly and does **not** create a `NotDetected` diagnostic disposition.

## 10. Scientific assertion versus regulatory action

Black Mesa's scientific record must remain stable even when policy changes.

~~~mermaid
flowchart LR
    E[Evidence] --> D[Diagnostic Detection Assertion]
    D --> R[Regulatory Evaluation]
    R --> RD[Regulatory Determination]
    RD --> RP[Reporting Decision]
    RP --> A[Alert / Notification]

    RULE[Jurisdiction + rule version] --> R
~~~

A state authority can change its reporting threshold without rewriting the underlying laboratory result or scientific detection.

This is why Arkansas, Louisiana, Missouri, Oklahoma, and Texas are represented as `OperationalJurisdiction` data rather than subclasses of disease or detection.

## 11. NPDN and CAP

Black Mesa treats NPDN diagnostic confidence as an interoperability target for downstream diagnostic records:

~~~text
Black Mesa Confirmed     -> NPDN Confirmed
Black Mesa Suspected     -> NPDN Suspected
Black Mesa Not Detected  -> NPDN Not Detected
Black Mesa Undetermined  -> NPDN Undetermined
~~~

A sensor-only indication has **no direct NPDN confidence mapping**.

CAP is different. CAP certainty describes the subject event of an alert message. It should therefore be computed by an explicit reporting policy, not inferred mechanically from the diagnostic disposition.

The crosswalk file records deliberate non-mappings so an integration cannot silently equate:

~~~text
Confirmed == CAP Observed
Suspected == CAP Likely
~~~

without an explicit policy decision.

## 12. Initial geography

The first operational cluster is Arkansas, Louisiana, Missouri, Oklahoma, and Texas.

The ontology does not define state-specific disease classes. Instead, a reporting rule or determination may be linked to the jurisdiction in which it applies.

That keeps scientific evidence portable while allowing policy to vary.

## 13. What comes next

The next major modules should be added only after the v0.3 evidence chain is exercised with real pilot data.

Likely sequence:

1. real crop/pathogen identifiers and pilot cases;
2. actual sensor/model descriptions;
3. validated diagnostic-method profiles;
4. environmental context used by inference;
5. spread and neighborhood models;
6. jurisdiction-specific reporting rules;
7. adaptive action selection based on information gain, cost, delay, and risk.

The core evidence model should remain small enough that each added term has an operational reason to exist.


## 14. Persistent identity and external reference data

Black Mesa v0.4 uses the persistent identifier base `https://w3id.org/black-mesa/`.

The ontology itself is `https://w3id.org/black-mesa/bmo`; local terms live beneath `/bmo/`.

Host and pathogen identities are not copied into a Black Mesa taxonomy. The initial pilot profiles reference NCBITaxon IRIs directly.

This keeps the core ontology about evidence and decisions while reference data answers the deployment question: which host/pathogen pair are we exercising?

## 15. Initial pilot pathosystems

~~~mermaid
flowchart TB
    P[PilotPathosystem]
    P --> R[Rice / rice blast]
    P --> S[Soybean / frogeye leaf spot]
    P --> W[Bread wheat / stripe rust]
    P --> K[Bread wheat / Karnal bunt]
    R --> O[OperationalPilot]
    S --> O
    W --> O
    K --> X[RegulatoryStressTest]
~~~

The Karnal bunt profile is deliberately different from the three operational pilots. Its primary purpose is to exercise the evidence-to-regulatory boundary, not to assert that it is the first sensor model Black Mesa should build.

## 16. Jurisdictional rule registry

State law and quarantine policy change independently of scientific evidence. v0.4 therefore represents state rules as versioned records rather than ontology classes.

~~~mermaid
flowchart LR
    D[Scientific detection] --> E[Regulatory evaluation]
    R[ReportingRule] --> E
    J[Jurisdiction] --> R
    A[Regulatory authority] --> R
    S[Authoritative source] --> R
    E --> H[Human review]
    H -->|approved action| N[Notification / restriction / other action]
~~~

The initial Arkansas, Louisiana, Missouri, Oklahoma, and Texas records are intake scaffolds marked **DRAFT — requires legal/regulatory review**. They cite official state sources but intentionally do not encode unverified triggers, deadlines, or enforcement consequences.

A draft rule cannot be treated as autonomous authority for external action.

## 17. Licensing boundary

Semantic content is CC BY 4.0; software/tooling is Apache-2.0. Third-party standards and vendored artifacts retain their own licensing terms. This split permits broad ontology reuse while giving executable code a conventional software license with Apache-2.0 terms.
