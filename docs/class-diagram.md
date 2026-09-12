# Black Mesa v0.3 class diagrams

This page gives the review-oriented diagrams for the v0.3 ontology. The canonical declarations are in `schema/bmo-core.ttl`; `tools/schema_docs.py` can regenerate an exhaustive structural diagram after schema changes.

For the operational story, see [architecture.md](architecture.md).

## 1. Evidence pipeline

~~~mermaid
flowchart LR
    SA[SurveyActivity] --> SO[SensorObservation]
    SO --> OA[ObservedAnomaly]
    OA --> SI[SensorIndicationAssertion]
    SI --> DH[DiagnosticHypothesis]
    DH --> CS[DiagnosticCandidateSet]
    CS --> OR[ObservationRequirement / SamplingRecommendation]
    OR --> SC[SampleCollection]
    SC --> SP[Specimen]
    SP --> DP[DiagnosticProcedure]
    DP --> DR[DiagnosticResult]
    DR --> DD[DiagnosticDetectionAssertion]
    DD --> RD[RegulatoryDetermination]
    RD --> RP[ReportingDecision]
    RP --> AL[Alert]

    OA -. "not equivalent" .-> DD
    DD -. "not equivalent" .-> RD
    RD -. "not equivalent" .-> AL
~~~

## 2. Sensor-agnostic class structure

~~~mermaid
classDiagram
    class SurveyActivity
    class Flight
    class SensorObservation
    class ObservedAnomaly
    class SpectralAnomaly
    class ImageryReference
    class SpatialSupportDescription

    SurveyActivity <|-- Flight
    ObservedAnomaly <|-- SpectralAnomaly
    SurveyActivity --> SensorObservation : madeObservation
    SurveyActivity --> ObservedAnomaly : observedAnomaly
    ObservedAnomaly --> SensorObservation : derivedFromObservation
    ObservedAnomaly --> ImageryReference : referencesImagery
    ObservedAnomaly --> SpatialSupportDescription : hasSpatialSupport
~~~

`Flight` and `SpectralAnomaly` remain useful for the initial drone use case, but neither is the root concept.

## 3. Hypothesis and adaptive-observation structure

~~~mermaid
classDiagram
    class SensorIndicationAssertion
    class DiagnosticHypothesis
    class DiagnosticCandidateSet
    class ObservationRequirement
    class SamplingRecommendation

    SensorIndicationAssertion --> ObservedAnomaly : derivedFromAnomaly
    DiagnosticCandidateSet --> DiagnosticHypothesis : hasCandidate
    ObservationRequirement --> DiagnosticHypothesis : discriminates
    SamplingRecommendation --> DiagnosticHypothesis : discriminates
~~~

A sensor indication may cause hypotheses to be created. It does not itself assert pathogen presence.

## 4. Physical evidence and custody

~~~mermaid
classDiagram
    class CustodyEvent
    class SampleCollection
    class TransferEvent
    class ReceiptEvent
    class StorageEvent
    class AliquotEvent
    class CustodyChain
    class CustodyRecord
    class Specimen
    class Aliquot
    class Container

    CustodyEvent <|-- SampleCollection
    CustodyEvent <|-- TransferEvent
    CustodyEvent <|-- ReceiptEvent
    CustodyEvent <|-- StorageEvent
    CustodyEvent <|-- AliquotEvent

    Specimen <|-- Aliquot
    SampleCollection --> Specimen : yieldedSpecimen
    TransferEvent --> Specimen : custodySubject
    ReceiptEvent --> Specimen : custodySubject
    AliquotEvent --> Specimen : sourceSpecimen
    AliquotEvent --> Aliquot : producedAliquot
    CustodyRecord --> CustodyEvent : hasCustodyEvent
    CustodyRecord --> CustodyChain : describesCustodyChain
~~~

The real custody history and the record describing it are intentionally separate.

## 5. Diagnostic layer

~~~mermaid
classDiagram
    class DiagnosticProcedure
    class Assay
    class DiagnosticResult
    class AssayResult
    class DiagnosticProcedureProfile
    class DetectionLimit
    class DiagnosticResultStatus

    DiagnosticProcedure <|-- Assay
    DiagnosticResult <|-- AssayResult
    DiagnosticProcedure --> Specimen : usedSpecimen
    DiagnosticProcedure --> DiagnosticResult : producedResult
    DiagnosticResult --> DiagnosticResultStatus : resultStatus
    DiagnosticProcedureProfile --> DetectionLimit : hasDetectionLimit
~~~

The method profile states where a method is validated. The result states what happened in one procedure event.

## 6. Epistemic model

~~~mermaid
classDiagram
    class EvidenceStage
    class DiagnosticDisposition
    class ConfidenceAssessment
    class EvidenceStrengthLevel
    class EvidenceCompletenessLevel
    class ApplicabilityStatus
    class ProvenanceQualityStatus

    ConfidenceAssessment --> EvidenceStrengthLevel : evidenceStrength
    ConfidenceAssessment --> EvidenceCompletenessLevel : evidenceCompleteness
    ConfidenceAssessment --> ApplicabilityStatus : modelApplicability
    ConfidenceAssessment --> ApplicabilityStatus : assayApplicability
    ConfidenceAssessment --> ProvenanceQualityStatus : provenanceQuality
~~~

These are independent dimensions. The ontology deliberately does not recreate the old single ranked confidence tier.

## 7. Assertion hierarchy

~~~mermaid
classDiagram
    class Assertion
    class SensorIndicationAssertion
    class DiagnosticHypothesis
    class DiagnosticDetectionAssertion
    class ConfirmedDetectionAssertion
    class RegulatoryDetermination
    class ReportingDecision

    Assertion <|-- SensorIndicationAssertion
    Assertion <|-- DiagnosticHypothesis
    Assertion <|-- DiagnosticDetectionAssertion
    DiagnosticDetectionAssertion <|-- ConfirmedDetectionAssertion
    Assertion <|-- RegulatoryDetermination
    Assertion <|-- ReportingDecision
~~~

All of these are claims. They are preserved as first-class information objects so that evidence, provenance, version, disagreement, and later revision can be represented.

## 8. Reporting and jurisdiction

~~~mermaid
classDiagram
    class OperationalJurisdiction
    class ReportingRule
    class ExternalReportingScheme
    class ExternalReportingTerm
    class ReportingCrosswalk
    class DiagnosticDetectionAssertion
    class RegulatoryDetermination

    DiagnosticDetectionAssertion --> ReportingRule : subjectToReportingRule
    ReportingRule --> OperationalJurisdiction : appliesInJurisdiction
    RegulatoryDetermination --> DiagnosticDetectionAssertion : basedOnDetection
    ReportingCrosswalk --> ExternalReportingScheme : targetScheme
    ReportingCrosswalk --> ExternalReportingTerm : crosswalkTo
~~~

Arkansas, Louisiana, Missouri, Oklahoma, and Texas are individuals of `OperationalJurisdiction`, not subclasses.

## 9. BFO anchoring by category

~~~mermaid
flowchart TB
    BFO[BFO 2.0]
    INFO[Information / assertions]
    PROC[Processes]
    MAT[Material entities]
    SITE[Sites / places]

    BFO --> INFO
    BFO --> PROC
    BFO --> MAT
    BFO --> SITE

    INFO --> SI[SensorIndicationAssertion]
    INFO --> DH[DiagnosticHypothesis]
    INFO --> DR[DiagnosticResult]
    INFO --> DD[DiagnosticDetectionAssertion]
    INFO --> RR[ReportingRule]

    PROC --> SA[SurveyActivity]
    PROC --> CE[CustodyEvent]
    PROC --> DP[DiagnosticProcedure]

    MAT --> SP[Specimen]
    MAT --> AQ[Aliquot]
    MAT --> CT[Container]

    SITE --> F[Farm]
    SITE --> FI[Field]
    SITE --> Z[Zone]
~~~

The shared upper module exists to make category mistakes visible. A diagnostic result, for example, is information about a physical specimen; it is not itself material.


## 10. Pilot and regulatory governance additions

~~~mermaid
classDiagram
    class PilotPathosystem
    class PilotScenarioRole
    class ReportingRule
    class RuleReviewStatus
    class RegulatoryActionType
    class OperationalJurisdiction

    PilotPathosystem --> PilotScenarioRole : scenarioRole
    ReportingRule --> OperationalJurisdiction : appliesInJurisdiction
    ReportingRule --> RuleReviewStatus : ruleReviewStatus
    ReportingRule --> RegulatoryActionType : requiredAction
~~~

Pilot pathosystems are reference-data profiles. Reporting rules are versioned governance records; state names, crops, and pathogens are not turned into subclasses.
