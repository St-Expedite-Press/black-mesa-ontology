<!-- GENERATED FILE — DO NOT EDIT BY HAND. Rebuild with: python tools/schema_docs.py --schema schema --out docs/reference -->

# Class diagrams

These diagrams are generated from the current Turtle schema. For product workflow and rationale, read [system architecture](../overview/system-architecture.md) and [evidence chain](../model/evidence-chain.md).

## Local subclass hierarchy

~~~mermaid
graph TD
  n_bmo_Alert["bmo:Alert"]
  n_bmo_Aliquot["bmo:Aliquot"]
  n_bmo_Specimen["bmo:Specimen"] --> n_bmo_Aliquot
  n_bmo_AliquotEvent["bmo:AliquotEvent"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"] --> n_bmo_AliquotEvent
  n_bmo_ApplicabilityStatus["bmo:ApplicabilityStatus"]
  n_bmo_Assay["bmo:Assay"]
  n_bmo_DiagnosticProcedure["bmo:DiagnosticProcedure"] --> n_bmo_Assay
  n_bmo_AssayResult["bmo:AssayResult"]
  n_bmo_DiagnosticResult["bmo:DiagnosticResult"] --> n_bmo_AssayResult
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_bmo_ConfidenceTier["bmo:ConfidenceTier"]
  n_bmo_ConfirmedDetectionAssertion["bmo:ConfirmedDetectionAssertion"]
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"] --> n_bmo_ConfirmedDetectionAssertion
  n_bmo_Container["bmo:Container"]
  n_bmo_CustodyChain["bmo:CustodyChain"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_bmo_CustodyRecord["bmo:CustodyRecord"]
  n_bmo_Detection["bmo:Detection"]
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"] --> n_bmo_Detection
  n_bmo_DetectionLimit["bmo:DetectionLimit"]
  n_bmo_DiagnosticCandidateSet["bmo:DiagnosticCandidateSet"]
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"]
  n_bmo_DiagnosticDisposition["bmo:DiagnosticDisposition"]
  n_bmo_DiagnosticHypothesis["bmo:DiagnosticHypothesis"]
  n_bmo_DiagnosticProcedure["bmo:DiagnosticProcedure"]
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_bmo_DiagnosticResult["bmo:DiagnosticResult"]
  n_bmo_DiagnosticResultStatus["bmo:DiagnosticResultStatus"]
  n_bmo_EvidenceCompletenessLevel["bmo:EvidenceCompletenessLevel"]
  n_bmo_EvidenceStage["bmo:EvidenceStage"]
  n_bmo_EvidenceStrengthLevel["bmo:EvidenceStrengthLevel"]
  n_bmo_ExternalReportingScheme["bmo:ExternalReportingScheme"]
  n_bmo_ExternalReportingTerm["bmo:ExternalReportingTerm"]
  n_bmo_Farm["bmo:Farm"]
  n_bmo_Field["bmo:Field"]
  n_bmo_Flight["bmo:Flight"]
  n_bmo_SurveyActivity["bmo:SurveyActivity"] --> n_bmo_Flight
  n_bmo_Host["bmo:Host"]
  n_bmo_ImageryReference["bmo:ImageryReference"]
  n_bmo_ObservationRequirement["bmo:ObservationRequirement"]
  n_bmo_ObservedAnomaly["bmo:ObservedAnomaly"]
  n_bmo_OperationalJurisdiction["bmo:OperationalJurisdiction"]
  n_bmo_PilotPathosystem["bmo:PilotPathosystem"]
  n_bmo_PilotScenarioRole["bmo:PilotScenarioRole"]
  n_bmo_ProvenanceQualityStatus["bmo:ProvenanceQualityStatus"]
  n_bmo_ReceiptEvent["bmo:ReceiptEvent"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"] --> n_bmo_ReceiptEvent
  n_bmo_RegulatoryActionType["bmo:RegulatoryActionType"]
  n_bmo_RegulatoryDetermination["bmo:RegulatoryDetermination"]
  n_bmo_ReportingCrosswalk["bmo:ReportingCrosswalk"]
  n_bmo_ReportingDecision["bmo:ReportingDecision"]
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_RuleReviewStatus["bmo:RuleReviewStatus"]
  n_bmo_SampleCollection["bmo:SampleCollection"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"] --> n_bmo_SampleCollection
  n_bmo_SamplingRecommendation["bmo:SamplingRecommendation"]
  n_bmo_SensorIndicationAssertion["bmo:SensorIndicationAssertion"]
  n_bmo_SensorObservation["bmo:SensorObservation"]
  n_bmo_SpatialSupportDescription["bmo:SpatialSupportDescription"]
  n_bmo_Specimen["bmo:Specimen"]
  n_bmo_SpectralAnomaly["bmo:SpectralAnomaly"]
  n_bmo_ObservedAnomaly["bmo:ObservedAnomaly"] --> n_bmo_SpectralAnomaly
  n_bmo_StorageEvent["bmo:StorageEvent"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"] --> n_bmo_StorageEvent
  n_bmo_SupportKind["bmo:SupportKind"]
  n_bmo_SurveyActivity["bmo:SurveyActivity"]
  n_bmo_TransferEvent["bmo:TransferEvent"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"] --> n_bmo_TransferEvent
  n_bmo_Zone["bmo:Zone"]
~~~

## Core relation graph

~~~mermaid
graph LR
  n_up_InformationArtifact["up:InformationArtifact"]
  n_bmo_OperationalJurisdiction["bmo:OperationalJurisdiction"]
  n_up_InformationArtifact -->|"bmo:appliesInJurisdiction"| n_bmo_OperationalJurisdiction
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_bmo_ApplicabilityStatus["bmo:ApplicabilityStatus"]
  n_bmo_ConfidenceAssessment -->|"bmo:assayApplicability"| n_bmo_ApplicabilityStatus
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticDetectionAssertion -->|"bmo:assertsPathogen"| n_rdfs_Resource
  n_bmo_RegulatoryDetermination["bmo:RegulatoryDetermination"]
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"]
  n_bmo_RegulatoryDetermination -->|"bmo:basedOnDetection"| n_bmo_DiagnosticDetectionAssertion
  n_up_Assertion["up:Assertion"]
  n_bmo_Zone["bmo:Zone"]
  n_up_Assertion -->|"bmo:concernsZone"| n_bmo_Zone
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_bmo_Specimen["bmo:Specimen"]
  n_bmo_CustodyEvent -->|"bmo:custodySubject"| n_bmo_Specimen
  n_bmo_SensorIndicationAssertion["bmo:SensorIndicationAssertion"]
  n_bmo_ObservedAnomaly["bmo:ObservedAnomaly"]
  n_bmo_SensorIndicationAssertion -->|"bmo:derivedFromAnomaly"| n_bmo_ObservedAnomaly
  n_bmo_ObservedAnomaly["bmo:ObservedAnomaly"]
  n_bmo_SensorObservation["bmo:SensorObservation"]
  n_bmo_ObservedAnomaly -->|"bmo:derivedFromObservation"| n_bmo_SensorObservation
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"]
  n_bmo_DiagnosticResult["bmo:DiagnosticResult"]
  n_bmo_DiagnosticDetectionAssertion -->|"bmo:derivedFromResult"| n_bmo_DiagnosticResult
  n_bmo_CustodyRecord["bmo:CustodyRecord"]
  n_bmo_CustodyChain["bmo:CustodyChain"]
  n_bmo_CustodyRecord -->|"bmo:describesCustodyChain"| n_bmo_CustodyChain
  n_up_RecordedProcess["up:RecordedProcess"]
  n_prov_Agent["prov:Agent"]
  n_up_RecordedProcess -->|"bmo:eventAgent"| n_prov_Agent
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_bmo_EvidenceCompletenessLevel["bmo:EvidenceCompletenessLevel"]
  n_bmo_ConfidenceAssessment -->|"bmo:evidenceCompleteness"| n_bmo_EvidenceCompletenessLevel
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_bmo_EvidenceStrengthLevel["bmo:EvidenceStrengthLevel"]
  n_bmo_ConfidenceAssessment -->|"bmo:evidenceStrength"| n_bmo_EvidenceStrengthLevel
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_prov_Agent["prov:Agent"]
  n_bmo_CustodyEvent -->|"bmo:fromCustodian"| n_prov_Agent
  n_bmo_DiagnosticCandidateSet["bmo:DiagnosticCandidateSet"]
  n_bmo_DiagnosticHypothesis["bmo:DiagnosticHypothesis"]
  n_bmo_DiagnosticCandidateSet -->|"bmo:hasCandidate"| n_bmo_DiagnosticHypothesis
  n_up_Assertion["up:Assertion"]
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_up_Assertion -->|"bmo:hasConfidenceAssessment"| n_bmo_ConfidenceAssessment
  n_bmo_CustodyRecord["bmo:CustodyRecord"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_bmo_CustodyRecord -->|"bmo:hasCustodyEvent"| n_bmo_CustodyEvent
  n_bmo_DiagnosticDetectionAssertion["bmo:DiagnosticDetectionAssertion"]
  n_bmo_CustodyRecord["bmo:CustodyRecord"]
  n_bmo_DiagnosticDetectionAssertion -->|"bmo:hasCustodyRecord"| n_bmo_CustodyRecord
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_bmo_DetectionLimit["bmo:DetectionLimit"]
  n_bmo_DiagnosticProcedureProfile -->|"bmo:hasDetectionLimit"| n_bmo_DetectionLimit
  n_up_Assertion["up:Assertion"]
  n_bmo_DiagnosticDisposition["bmo:DiagnosticDisposition"]
  n_up_Assertion -->|"bmo:hasDiagnosticDisposition"| n_bmo_DiagnosticDisposition
  n_up_Assertion["up:Assertion"]
  n_bmo_EvidenceStage["bmo:EvidenceStage"]
  n_up_Assertion -->|"bmo:hasEvidenceStage"| n_bmo_EvidenceStage
  n_up_InformationArtifact["up:InformationArtifact"]
  n_bmo_SpatialSupportDescription["bmo:SpatialSupportDescription"]
  n_up_InformationArtifact -->|"bmo:hasSpatialSupport"| n_bmo_SpatialSupportDescription
  n_bmo_SurveyActivity["bmo:SurveyActivity"]
  n_sosa_Platform["sosa:Platform"]
  n_bmo_SurveyActivity -->|"bmo:hostedByPlatform"| n_sosa_Platform
  n_bmo_PilotPathosystem["bmo:PilotPathosystem"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_PilotPathosystem -->|"bmo:hostTaxon"| n_rdfs_Resource
  n_bmo_DiagnosticHypothesis["bmo:DiagnosticHypothesis"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticHypothesis -->|"bmo:hypothesizesAgent"| n_rdfs_Resource
  n_bmo_RegulatoryDetermination["bmo:RegulatoryDetermination"]
  n_prov_Agent["prov:Agent"]
  n_bmo_RegulatoryDetermination -->|"bmo:issuedBy"| n_prov_Agent
  n_bmo_SurveyActivity["bmo:SurveyActivity"]
  n_bmo_SensorObservation["bmo:SensorObservation"]
  n_bmo_SurveyActivity -->|"bmo:madeObservation"| n_bmo_SensorObservation
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_bmo_ApplicabilityStatus["bmo:ApplicabilityStatus"]
  n_bmo_ConfidenceAssessment -->|"bmo:modelApplicability"| n_bmo_ApplicabilityStatus
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_prov_Agent["prov:Agent"]
  n_bmo_ReportingRule -->|"bmo:notificationRecipient"| n_prov_Agent
  n_bmo_SurveyActivity["bmo:SurveyActivity"]
  n_bmo_ObservedAnomaly["bmo:ObservedAnomaly"]
  n_bmo_SurveyActivity -->|"bmo:observedAnomaly"| n_bmo_ObservedAnomaly
  n_up_RecordedProcess["up:RecordedProcess"]
  n_bmo_Zone["bmo:Zone"]
  n_up_RecordedProcess -->|"bmo:occursAtZone"| n_bmo_Zone
  n_up_SurveyedSite["up:SurveyedSite"]
  n_up_SurveyedSite["up:SurveyedSite"]
  n_up_SurveyedSite -->|"bmo:partOfSite"| n_up_SurveyedSite
  n_bmo_PilotPathosystem["bmo:PilotPathosystem"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_PilotPathosystem -->|"bmo:pathogenTaxon"| n_rdfs_Resource
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_bmo_CustodyEvent -->|"bmo:previousCustodyEvent"| n_bmo_CustodyEvent
  n_bmo_AliquotEvent["bmo:AliquotEvent"]
  n_bmo_Aliquot["bmo:Aliquot"]
  n_bmo_AliquotEvent -->|"bmo:producedAliquot"| n_bmo_Aliquot
  n_bmo_DiagnosticResult["bmo:DiagnosticResult"]
  n_bmo_DiagnosticProcedure["bmo:DiagnosticProcedure"]
  n_bmo_DiagnosticResult -->|"bmo:producedByProcedure"| n_bmo_DiagnosticProcedure
  n_bmo_DiagnosticProcedure["bmo:DiagnosticProcedure"]
  n_bmo_DiagnosticResult["bmo:DiagnosticResult"]
  n_bmo_DiagnosticProcedure -->|"bmo:producedResult"| n_bmo_DiagnosticResult
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticProcedureProfile -->|"bmo:profilesMethod"| n_rdfs_Resource
  n_bmo_ConfidenceAssessment["bmo:ConfidenceAssessment"]
  n_bmo_ProvenanceQualityStatus["bmo:ProvenanceQualityStatus"]
  n_bmo_ConfidenceAssessment -->|"bmo:provenanceQuality"| n_bmo_ProvenanceQualityStatus
  n_bmo_ObservedAnomaly["bmo:ObservedAnomaly"]
  n_bmo_ImageryReference["bmo:ImageryReference"]
  n_bmo_ObservedAnomaly -->|"bmo:referencesImagery"| n_bmo_ImageryReference
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_ReportingRule -->|"bmo:regulatedArea"| n_rdfs_Resource
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_ReportingRule -->|"bmo:regulatedCommodity"| n_rdfs_Resource
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_ReportingRule -->|"bmo:regulatedHost"| n_rdfs_Resource
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_ReportingRule -->|"bmo:regulatedTaxon"| n_rdfs_Resource
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_prov_Agent["prov:Agent"]
  n_bmo_ReportingRule -->|"bmo:regulatoryAuthority"| n_prov_Agent
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_RegulatoryActionType["bmo:RegulatoryActionType"]
  n_bmo_ReportingRule -->|"bmo:requiredAction"| n_bmo_RegulatoryActionType
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_ReportingRule -->|"bmo:requiredConfirmationMethod"| n_rdfs_Resource
  n_bmo_DiagnosticResult["bmo:DiagnosticResult"]
  n_bmo_DiagnosticResultStatus["bmo:DiagnosticResultStatus"]
  n_bmo_DiagnosticResult -->|"bmo:resultStatus"| n_bmo_DiagnosticResultStatus
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_RuleReviewStatus["bmo:RuleReviewStatus"]
  n_bmo_ReportingRule -->|"bmo:ruleReviewStatus"| n_bmo_RuleReviewStatus
  n_bmo_PilotPathosystem["bmo:PilotPathosystem"]
  n_bmo_PilotScenarioRole["bmo:PilotScenarioRole"]
  n_bmo_PilotPathosystem -->|"bmo:scenarioRole"| n_bmo_PilotScenarioRole
  n_bmo_AliquotEvent["bmo:AliquotEvent"]
  n_bmo_Specimen["bmo:Specimen"]
  n_bmo_AliquotEvent -->|"bmo:sourceSpecimen"| n_bmo_Specimen
  n_up_Assertion["up:Assertion"]
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_up_Assertion -->|"bmo:subjectToReportingRule"| n_bmo_ReportingRule
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_ReportingRule -->|"bmo:supersedesRule"| n_bmo_ReportingRule
  n_bmo_SpatialSupportDescription["bmo:SpatialSupportDescription"]
  n_bmo_SupportKind["bmo:SupportKind"]
  n_bmo_SpatialSupportDescription -->|"bmo:supportKind"| n_bmo_SupportKind
  n_bmo_ReportingCrosswalk["bmo:ReportingCrosswalk"]
  n_bmo_ExternalReportingScheme["bmo:ExternalReportingScheme"]
  n_bmo_ReportingCrosswalk -->|"bmo:targetScheme"| n_bmo_ExternalReportingScheme
  n_bmo_CustodyEvent["bmo:CustodyEvent"]
  n_prov_Agent["prov:Agent"]
  n_bmo_CustodyEvent -->|"bmo:toCustodian"| n_prov_Agent
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_DiagnosticDisposition["bmo:DiagnosticDisposition"]
  n_bmo_ReportingRule -->|"bmo:triggerDiagnosticDisposition"| n_bmo_DiagnosticDisposition
  n_up_Assertion["up:Assertion"]
  n_bmo_Alert["bmo:Alert"]
  n_up_Assertion -->|"bmo:triggeredAlert"| n_bmo_Alert
  n_bmo_ReportingRule["bmo:ReportingRule"]
  n_bmo_EvidenceStage["bmo:EvidenceStage"]
  n_bmo_ReportingRule -->|"bmo:triggerEvidenceStage"| n_bmo_EvidenceStage
  n_bmo_DiagnosticProcedure["bmo:DiagnosticProcedure"]
  n_bmo_Specimen["bmo:Specimen"]
  n_bmo_DiagnosticProcedure -->|"bmo:usedSpecimen"| n_bmo_Specimen
  n_bmo_SurveyActivity["bmo:SurveyActivity"]
  n_sosa_Sensor["sosa:Sensor"]
  n_bmo_SurveyActivity -->|"bmo:usesSensor"| n_sosa_Sensor
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticProcedureProfile -->|"bmo:validatedForHost"| n_rdfs_Resource
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticProcedureProfile -->|"bmo:validatedForMatrix"| n_rdfs_Resource
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticProcedureProfile -->|"bmo:validatedForPathogen"| n_rdfs_Resource
  n_bmo_DiagnosticProcedureProfile["bmo:DiagnosticProcedureProfile"]
  n_rdfs_Resource["rdfs:Resource"]
  n_bmo_DiagnosticProcedureProfile -->|"bmo:validationSource"| n_rdfs_Resource
  n_bmo_SampleCollection["bmo:SampleCollection"]
  n_bmo_Specimen["bmo:Specimen"]
  n_bmo_SampleCollection -->|"bmo:yieldedSpecimen"| n_bmo_Specimen
~~~
