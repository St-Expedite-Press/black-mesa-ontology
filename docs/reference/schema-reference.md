<!-- GENERATED FILE — DO NOT EDIT BY HAND. Rebuild with: python tools/schema_docs.py --schema schema --out docs/reference -->

# Schema reference

Structural reference generated directly from Turtle. For conceptual guidance, read [modeling principles](../model/modeling-principles.md) and [evidence chain](../model/evidence-chain.md).

**58 local classes · 66 object properties · 20 datatype properties**

## Classes

| Class | Parent(s) | Meaning |
|---|---|---|
| [bmo:Alert](#bmo-alert) | obo:IAO_0000033 | A directive or notification issued on the basis of one or more determinations. Alert semantics belong to the policy layer and are not equivalent to diagnostic confidence. |
| [bmo:Aliquot](#bmo-aliquot) | bmo:Specimen | A physically separated portion of a specimen that has its own identity and custody history while remaining genealogically linked to the source specimen. |
| [bmo:AliquotEvent](#bmo-aliquotevent) | bmo:CustodyEvent | A custody event in which one specimen is subdivided into one or more aliquots while preserving genealogy back to the source specimen. |
| [bmo:ApplicabilityStatus](#bmo-applicabilitystatus) | up:ConceptualUnit | Controlled vocabulary for whether a model or diagnostic method is being used within supported validation conditions. |
| [bmo:Assay](#bmo-assay) | bmo:DiagnosticProcedure | A diagnostic procedure implemented as an assay. Retained for compatibility with the original Phase 1 model. |
| [bmo:AssayResult](#bmo-assayresult) | bmo:DiagnosticResult | A diagnostic result produced specifically by an assay. |
| [bmo:ConfidenceAssessment](#bmo-confidenceassessment) | up:ConfidenceAssessment | A multi-axis statement of how much weight an assertion can bear. Confidence is not collapsed into a single ordinal tier. |
| [bmo:ConfidenceTier](#bmo-confidencetier) | up:ConceptualUnit | Deprecated in v0.3. The former single tier conflated evidence stage, diagnostic disposition, and confidence. Use EvidenceStage, DiagnosticDisposition, and ConfidenceAssessment separately. |
| [bmo:ConfirmedDetectionAssertion](#bmo-confirmeddetectionassertion) | bmo:DiagnosticDetectionAssertion | A diagnostic detection assertion whose disposition is Confirmed and whose evidence has reached the confirmatory stage. |
| [bmo:Container](#bmo-container) | obo:BFO_0000030 | The physical vessel holding a specimen or aliquot. Container identity may be required to establish continuity of custody. |
| [bmo:CustodyChain](#bmo-custodychain) | up:ProvenanceChain | The real sequence of custody-related processes from collection through transfer, receipt, storage, analysis, and disposition. |
| [bmo:CustodyEvent](#bmo-custodyevent) | up:RecordedProcess | A recorded event affecting possession, location, identity, or integrity of a specimen or aliquot. Custody is represented as explicit events, not a single opaque provenance string. |
| [bmo:CustodyRecord](#bmo-custodyrecord) | up:InformationArtifact | The legally relevant information record describing a custody chain. It identifies custody events, their order, agents, timestamps, containers, seals, and integrity observations. |
| [bmo:Detection](#bmo-detection) | bmo:DiagnosticDetectionAssertion | Deprecated compatibility class from v0.2. New data should use DiagnosticDetectionAssertion or ConfirmedDetectionAssertion. |
| [bmo:DetectionLimit](#bmo-detectionlimit) | up:ThresholdSpecification | A validated threshold below which a procedure cannot reliably distinguish presence from absence. |
| [bmo:DiagnosticCandidateSet](#bmo-diagnosticcandidateset) | up:CandidateSet | The live competing hypotheses retained by the system at a point in the evidence-gathering workflow. |
| [bmo:DiagnosticDetectionAssertion](#bmo-diagnosticdetectionassertion) | up:Assertion | A scientific assertion about whether a specified pathogen is detected at a specified spatial support, derived from diagnostic evidence and carrying provenance, custody, method applicability, and rule version. |
| [bmo:DiagnosticDisposition](#bmo-diagnosticdisposition) | up:ConceptualUnit | Overall diagnostic status of a pathogen determination. These values are kept separate from evidence stage and from quantitative or qualitative confidence. |
| [bmo:DiagnosticHypothesis](#bmo-diagnostichypothesis) | up:Assertion | A revisable hypothesis about the cause of an observed anomaly. It may concern a pathogen, an abiotic stressor, or another causal agent and is explicitly not a detection. |
| [bmo:DiagnosticProcedure](#bmo-diagnosticprocedure) | up:AnalysisProcess | An analysis process performed on a specimen or aliquot to produce diagnostic evidence. It is method-agnostic and may include molecular, serological, morphological, culture, sequencing, or future methods. |
| [bmo:DiagnosticProcedureProfile](#bmo-diagnosticprocedureprofile) | up:InformationArtifact | A versioned description of where a diagnostic method is validated and how it performs: target organism, host, specimen matrix, sensitivity, specificity, limit of detection, and source of validation. |
| [bmo:DiagnosticResult](#bmo-diagnosticresult) | obo:IAO_0000109 | The result datum generated by a diagnostic procedure. A result is distinct from the later interpretation or detection assertion based on it. |
| [bmo:DiagnosticResultStatus](#bmo-diagnosticresultstatus) | up:ConceptualUnit | Status of the result produced by a diagnostic procedure. It is not the same thing as an overall diagnostic disposition. |
| [bmo:EvidenceCompletenessLevel](#bmo-evidencecompletenesslevel) | up:ConceptualUnit | Controlled vocabulary for how complete the desired evidentiary record is. |
| [bmo:EvidenceStage](#bmo-evidencestage) | up:ConceptualUnit | Where an assertion sits in the evidence-gathering workflow. This is not a confidence scale. |
| [bmo:EvidenceStrengthLevel](#bmo-evidencestrengthlevel) | up:ConceptualUnit | Controlled vocabulary for qualitative strength of evidence supporting an assertion. |
| [bmo:ExternalReportingScheme](#bmo-externalreportingscheme) | up:ConceptualUnit | An external controlled vocabulary, repository, message standard, or reporting scheme to which Black Mesa data may be mapped. |
| [bmo:ExternalReportingTerm](#bmo-externalreportingterm) | up:ConceptualUnit | A project-local proxy describing a term in an external reporting scheme when that scheme does not publish a stable RDF identifier. The source URL and notation are mandatory in crosswalk data. |
| [bmo:Farm](#bmo-farm) | up:SurveyedSite | A managed agricultural holding under one operator. Access, consent, and many reporting obligations attach at this level. |
| [bmo:Field](#bmo-field) | up:SurveyedSite | A bounded cultivated area within a farm, normally under a crop and management regime. |
| [bmo:Flight](#bmo-flight) | bmo:SurveyActivity | An aerial survey sortie. Retained as a subtype because drones are an expected early platform, but the core ontology does not depend on flight. |
| [bmo:Host](#bmo-host) | obo:BFO_0000027 | The crop plants occupying a surveyed site. Taxonomic identity should be referenced to an external authority rather than replicated as local classes. |
| [bmo:ImageryReference](#bmo-imageryreference) | up:InformationArtifact | A pointer to imagery or another large sensor artifact held outside the RDF graph. It carries a storage URI and content checksum so the evidence bytes can be retrieved and verified. |
| [bmo:ObservationRequirement](#bmo-observationrequirement) | up:RequirementSpecification | A request for the observation that would most reduce uncertainty among live hypotheses. |
| [bmo:ObservedAnomaly](#bmo-observedanomaly) | up:DerivedDatum | A derived record that some observation differs from an expected or reference condition. It is evidence that something warrants investigation, not a diagnosis. |
| [bmo:OperationalJurisdiction](#bmo-operationaljurisdiction) | up:ConceptualUnit | A jurisdiction relevant to deployment, reporting, or regulatory evaluation. States are represented as data, not ontology subclasses. |
| [bmo:PilotPathosystem](#bmo-pilotpathosystem) | up:InformationArtifact | A versionable profile selecting a host/pathogen pair for an operational pilot or regulatory stress test. The host and pathogen are referenced by canonical external taxon IRIs rather than redefined locally. |
| [bmo:PilotScenarioRole](#bmo-pilotscenariorole) | up:ConceptualUnit | Controlled role describing whether a pathosystem profile is intended for operational evidence-chain testing or primarily for regulatory stress testing. |
| [bmo:ProvenanceQualityStatus](#bmo-provenancequalitystatus) | up:ConceptualUnit | Controlled vocabulary for the integrity and completeness of the provenance and custody record. |
| [bmo:ReceiptEvent](#bmo-receiptevent) | bmo:CustodyEvent | A custody event recording receipt by a laboratory, facility, or other custodian. |
| [bmo:RegulatoryActionType](#bmo-regulatoryactiontype) | up:ConceptualUnit | Controlled action category used by reviewed reporting rules to describe the kind of follow-up a rule may require. |
| [bmo:RegulatoryDetermination](#bmo-regulatorydetermination) | up:Assertion | A determination made by an authorized body under a reporting or regulatory rule. It is deliberately separate from the underlying scientific detection assertion. |
| [bmo:ReportingCrosswalk](#bmo-reportingcrosswalk) | up:Crosswalk | A directional, evidence-bearing mapping from an internal concept to an external reporting term or scheme. Fidelity is explicit; NoMapping is a legitimate result. |
| [bmo:ReportingDecision](#bmo-reportingdecision) | up:Assertion | A decision about whether and how a scientific assertion is transmitted to an external reporting system or authority. |
| [bmo:ReportingRule](#bmo-reportingrule) | up:RuleSetVersion | A versioned rule specifying when, to whom, and in what representation a detection or determination should be reported. |
| [bmo:RuleReviewStatus](#bmo-rulereviewstatus) | up:ConceptualUnit | Governance status for a jurisdictional reporting rule. Draft rules are non-operative until reviewed and approved by an authorized legal/regulatory reviewer. |
| [bmo:SampleCollection](#bmo-samplecollection) | up:SamplingProcess, bmo:CustodyEvent | The act of removing material from a site or host and creating a specimen with a persistent identity. It is simultaneously a sampling process and the first custody event. |
| [bmo:SamplingRecommendation](#bmo-samplingrecommendation) | up:RequirementSpecification | A directive specifying what material should be collected, where, and why. It is generated from evidence and hypotheses rather than hard-coded to a sensor modality. |
| [bmo:SensorIndicationAssertion](#bmo-sensorindicationassertion) | up:Assertion | An assertion that sensor evidence warrants further investigation. It does not assert that a pathogen is present and must not be flattened into a diagnostic disposition such as Suspected. |
| [bmo:SensorObservation](#bmo-sensorobservation) | up:ObservationProcess, sosa:Observation | An observation made by a sensing device under a procedure. The observation is an event; its result and later interpretation are separate. |
| [bmo:SpatialSupportDescription](#bmo-spatialsupportdescription) | up:SupportDescription | A description of the spatial footprint over which an observation or assertion is warranted: point, plant, row, polygon, field, raster footprint, sensor footprint, or sampling area. |
| [bmo:Specimen](#bmo-specimen) | up:Specimen | Material removed from a sampling target and assigned a persistent identity. The specimen remains distinct from any data or diagnosis produced about it. |
| [bmo:SpectralAnomaly](#bmo-spectralanomaly) | bmo:ObservedAnomaly | An observed anomaly derived specifically from spectral data. This subtype preserves the original drone use case without making spectral sensing part of the core contract. |
| [bmo:StorageEvent](#bmo-storageevent) | bmo:CustodyEvent | A custody event recording controlled storage of a specimen or aliquot under stated conditions. |
| [bmo:SupportKind](#bmo-supportkind) | up:ConceptualUnit | Controlled vocabulary describing the kind of spatial support represented by a support description. |
| [bmo:SurveyActivity](#bmo-surveyactivity) | up:ObservationProcess | A surveillance activity using one or more sensors or observation procedures over one or more sites. It is intentionally independent of platform and sensor modality. |
| [bmo:TransferEvent](#bmo-transferevent) | bmo:CustodyEvent | A custody event in which possession of a specimen or aliquot passes from one custodian to another. |
| [bmo:Zone](#bmo-zone) | up:SurveyedSite | A sub-field place used for surveillance, sampling, or management. A zone is not assumed to be the finest spatial support of every observation. |

## Object properties

| Property | Domain | Range | Meaning |
|---|---|---|---|
| bmo:appliesInJurisdiction | up:InformationArtifact | bmo:OperationalJurisdiction | _No description supplied._ |
| bmo:assayApplicability | bmo:ConfidenceAssessment | bmo:ApplicabilityStatus | Whether the diagnostic procedure is validated for the relevant pathogen, host, and specimen matrix. |
| bmo:assertsPathogen | bmo:DiagnosticDetectionAssertion | rdfs:Resource | The pathogen taxon asserted in a diagnostic determination. Use an external canonical identifier; Black Mesa does not mint a local pathogen taxonomy. |
| bmo:basedOnDetection | bmo:RegulatoryDetermination | bmo:DiagnosticDetectionAssertion | _No description supplied._ |
| bmo:concernsZone | up:Assertion | bmo:Zone | _No description supplied._ |
| bmo:custodySubject | bmo:CustodyEvent | bmo:Specimen | The specimen or aliquot whose custody is affected by an event. |
| bmo:derivedFromAnomaly | bmo:SensorIndicationAssertion | bmo:ObservedAnomaly | _No description supplied._ |
| bmo:derivedFromObservation | bmo:ObservedAnomaly | bmo:SensorObservation | _No description supplied._ |
| bmo:derivedFromResult | bmo:DiagnosticDetectionAssertion | bmo:DiagnosticResult | _No description supplied._ |
| bmo:describesCustodyChain | bmo:CustodyRecord | bmo:CustodyChain | _No description supplied._ |
| bmo:eventAgent | up:RecordedProcess | prov:Agent | The person, organization, device, or service responsible for recording or performing the event. |
| bmo:evidenceCompleteness | bmo:ConfidenceAssessment | bmo:EvidenceCompletenessLevel | _No description supplied._ |
| bmo:evidenceStrength | bmo:ConfidenceAssessment | bmo:EvidenceStrengthLevel | _No description supplied._ |
| bmo:fromCustodian | bmo:CustodyEvent | prov:Agent | _No description supplied._ |
| bmo:hasCandidate | bmo:DiagnosticCandidateSet | bmo:DiagnosticHypothesis | _No description supplied._ |
| bmo:hasConfidenceAssessment | up:Assertion | bmo:ConfidenceAssessment | _No description supplied._ |
| bmo:hasCustodyEvent | bmo:CustodyRecord | bmo:CustodyEvent | _No description supplied._ |
| bmo:hasCustodyRecord | bmo:DiagnosticDetectionAssertion | bmo:CustodyRecord | Links a diagnostic determination to the record establishing the identity and custody history of the physical evidence on which it relies. |
| bmo:hasDetectionLimit | bmo:DiagnosticProcedureProfile | bmo:DetectionLimit | _No description supplied._ |
| bmo:hasDiagnosticDisposition | up:Assertion | bmo:DiagnosticDisposition | _No description supplied._ |
| bmo:hasEvidenceStage | up:Assertion | bmo:EvidenceStage | _No description supplied._ |
| bmo:hasSpatialSupport | up:InformationArtifact | bmo:SpatialSupportDescription | Links an information artifact to the explicit description of the area, point, plant, row, or footprint over which it is warranted. |
| bmo:hostTaxon | bmo:PilotPathosystem | rdfs:Resource | Canonical external identifier for the crop or host taxon represented by a pilot profile. |
| bmo:hostedByPlatform | bmo:SurveyActivity | sosa:Platform | The physical platform carrying the sensor, such as a UAS, ground vehicle, fixed station, aircraft, or other host. |
| bmo:hypothesizesAgent | bmo:DiagnosticHypothesis | rdfs:Resource | The organism, abiotic cause, or other agent proposed by a diagnostic hypothesis. Canonical external identifiers should be used where available. |
| bmo:issuedBy | bmo:RegulatoryDetermination | prov:Agent | _No description supplied._ |
| bmo:madeObservation | bmo:SurveyActivity | bmo:SensorObservation | _No description supplied._ |
| bmo:modelApplicability | bmo:ConfidenceAssessment | bmo:ApplicabilityStatus | Whether the sensing or inference model is being applied within the conditions for which its performance is supported. |
| bmo:notificationRecipient | bmo:ReportingRule | prov:Agent | _No description supplied._ |
| bmo:observedAnomaly | bmo:SurveyActivity | bmo:ObservedAnomaly | A survey may yield zero or more anomaly records. Zero is a meaningful negative surveillance outcome, not missing data. |
| bmo:occursAtZone | up:RecordedProcess | bmo:Zone | _No description supplied._ |
| bmo:partOfSite | up:SurveyedSite | up:SurveyedSite | Spatial containment among surveyed sites, for example zone to field and field to farm. |
| bmo:pathogenTaxon | bmo:PilotPathosystem | rdfs:Resource | Canonical external identifier for the pathogen represented by a pilot profile. |
| bmo:previousCustodyEvent | bmo:CustodyEvent | bmo:CustodyEvent | The immediately preceding custody event for the same specimen or aliquot. Used to expose breaks in continuity rather than hiding them. |
| bmo:producedAliquot | bmo:AliquotEvent | bmo:Aliquot | _No description supplied._ |
| bmo:producedByProcedure | bmo:DiagnosticResult | bmo:DiagnosticProcedure | _No description supplied._ |
| bmo:producedResult | bmo:DiagnosticProcedure | bmo:DiagnosticResult | _No description supplied._ |
| bmo:profilesMethod | bmo:DiagnosticProcedureProfile | rdfs:Resource | The diagnostic method or procedure specification described by a validation profile. |
| bmo:provenanceQuality | bmo:ConfidenceAssessment | bmo:ProvenanceQualityStatus | _No description supplied._ |
| bmo:referencesImagery | bmo:ObservedAnomaly | bmo:ImageryReference | Links an anomaly to the external imagery or sensor artifact from which it was derived. Raw imagery is referenced, never tiled into the graph. |
| bmo:regulatedArea | bmo:ReportingRule | rdfs:Resource | _No description supplied._ |
| bmo:regulatedCommodity | bmo:ReportingRule | rdfs:Resource | _No description supplied._ |
| bmo:regulatedHost | bmo:ReportingRule | rdfs:Resource | _No description supplied._ |
| bmo:regulatedTaxon | bmo:ReportingRule | rdfs:Resource | _No description supplied._ |
| bmo:regulatoryAuthority | bmo:ReportingRule | prov:Agent | _No description supplied._ |
| bmo:requiredAction | bmo:ReportingRule | bmo:RegulatoryActionType | _No description supplied._ |
| bmo:requiredConfirmationMethod | bmo:ReportingRule | rdfs:Resource | _No description supplied._ |
| bmo:resultStatus | bmo:DiagnosticResult | bmo:DiagnosticResultStatus | _No description supplied._ |
| bmo:ruleReviewStatus | bmo:ReportingRule | bmo:RuleReviewStatus | _No description supplied._ |
| bmo:scenarioRole | bmo:PilotPathosystem | bmo:PilotScenarioRole | _No description supplied._ |
| bmo:sourceSpecimen | bmo:AliquotEvent | bmo:Specimen | _No description supplied._ |
| bmo:subjectToReportingRule | up:Assertion | bmo:ReportingRule | _No description supplied._ |
| bmo:supersedesRule | bmo:ReportingRule | bmo:ReportingRule | _No description supplied._ |
| bmo:supportKind | bmo:SpatialSupportDescription | bmo:SupportKind | _No description supplied._ |
| bmo:targetScheme | bmo:ReportingCrosswalk | bmo:ExternalReportingScheme | _No description supplied._ |
| bmo:toCustodian | bmo:CustodyEvent | prov:Agent | _No description supplied._ |
| bmo:triggerDiagnosticDisposition | bmo:ReportingRule | bmo:DiagnosticDisposition | _No description supplied._ |
| bmo:triggerEvidenceStage | bmo:ReportingRule | bmo:EvidenceStage | _No description supplied._ |
| bmo:triggeredAlert | up:Assertion | bmo:Alert | Links a scientific or regulatory assertion to an alert. Alert issuance remains a separate policy decision. |
| bmo:usedSpecimen | bmo:DiagnosticProcedure | bmo:Specimen | _No description supplied._ |
| bmo:usesSensor | bmo:SurveyActivity | sosa:Sensor | The sensor used during a survey or observation. External sensor descriptions should use SOSA/SSN rather than a Black Mesa sensor taxonomy. |
| bmo:validatedForHost | bmo:DiagnosticProcedureProfile | rdfs:Resource | _No description supplied._ |
| bmo:validatedForMatrix | bmo:DiagnosticProcedureProfile | rdfs:Resource | _No description supplied._ |
| bmo:validatedForPathogen | bmo:DiagnosticProcedureProfile | rdfs:Resource | _No description supplied._ |
| bmo:validationSource | bmo:DiagnosticProcedureProfile | rdfs:Resource | _No description supplied._ |
| bmo:yieldedSpecimen | bmo:SampleCollection | bmo:Specimen | _No description supplied._ |

## Datatype properties

| Property | Domain | Range | Meaning |
|---|---|---|---|
| bmo:calibratedProbability | bmo:ConfidenceAssessment | xsd:decimal | Present only where a calibrated probabilistic model produced it. Absence is meaningful and must never be imputed. |
| bmo:candidateProbability | bmo:DiagnosticHypothesis | xsd:decimal | Optional calibrated probability attached to a hypothesis only when produced by a calibrated model. It must not be invented from an ordinal rank. |
| bmo:candidateRank | bmo:DiagnosticHypothesis | xsd:integer | Ordinal rank among candidates. A rank is not a probability. |
| bmo:checksum | bmo:ImageryReference | xsd:string | Content hash used to verify that a reference resolves to the exact bytes that were analyzed. |
| bmo:containerIdentifier | bmo:CustodyEvent | xsd:string | _No description supplied._ |
| bmo:effectiveFrom | bmo:ReportingRule | xsd:date | _No description supplied._ |
| bmo:effectiveUntil | bmo:ReportingRule | xsd:date | _No description supplied._ |
| bmo:eventTime | up:RecordedProcess | xsd:dateTime | Timestamp of a physical or recorded process event. |
| bmo:expectedCost | up:RequirementSpecification | xsd:decimal | Optional cost estimate used by the decision layer when comparing next-best observations or actions. |
| bmo:expectedInformationGain | up:RequirementSpecification | xsd:decimal | Optional estimate of how much a requested observation is expected to reduce uncertainty among live candidates. |
| bmo:legalReviewNote | bmo:ReportingRule | rdfs:Literal | Human-readable note recording unresolved legal or regulatory interpretation questions. It is not a substitute for source citation or formal review status. |
| bmo:movementRestrictionRequired | bmo:ReportingRule | xsd:boolean | _No description supplied._ |
| bmo:notificationDeadline | bmo:ReportingRule | xsd:duration | _No description supplied._ |
| bmo:requiresHumanReview | bmo:ReportingRule | xsd:boolean | Whether a human reviewer must approve the rule application before an external action is taken. Black Mesa Phase 1 policy requires human approval for external regulatory notification. |
| bmo:ruleIdentifier | bmo:ReportingRule | xsd:string | _No description supplied._ |
| bmo:sealIdentifier | bmo:CustodyEvent | xsd:string | _No description supplied._ |
| bmo:sensitivity | bmo:DiagnosticProcedureProfile | xsd:decimal | _No description supplied._ |
| bmo:specificity | bmo:DiagnosticProcedureProfile | xsd:decimal | _No description supplied._ |
| bmo:storageURI | bmo:ImageryReference | xsd:anyURI | _No description supplied._ |
| bmo:tamperStatus | bmo:CustodyEvent | xsd:string | Recorded integrity status of a container or seal at a custody event. A controlled vocabulary may replace the literal when operational requirements settle. |

## Detailed class definitions

### bmo:Alert

**Alert**

A directive or notification issued on the basis of one or more determinations. Alert semantics belong to the policy layer and are not equivalent to diagnostic confidence.

### bmo:Aliquot

**Aliquot**

A physically separated portion of a specimen that has its own identity and custody history while remaining genealogically linked to the source specimen.

### bmo:AliquotEvent

**Aliquot event**

A custody event in which one specimen is subdivided into one or more aliquots while preserving genealogy back to the source specimen.

### bmo:ApplicabilityStatus

**Applicability status**

Controlled vocabulary for whether a model or diagnostic method is being used within supported validation conditions.

### bmo:Assay

**Assay**

A diagnostic procedure implemented as an assay. Retained for compatibility with the original Phase 1 model.

### bmo:AssayResult

**Assay result**

A diagnostic result produced specifically by an assay.

### bmo:ConfidenceAssessment

**Confidence assessment**

A multi-axis statement of how much weight an assertion can bear. Confidence is not collapsed into a single ordinal tier.

### bmo:ConfidenceTier

**Confidence tier (deprecated)**

Deprecated in v0.3. The former single tier conflated evidence stage, diagnostic disposition, and confidence. Use EvidenceStage, DiagnosticDisposition, and ConfidenceAssessment separately.

### bmo:ConfirmedDetectionAssertion

**Confirmed detection assertion**

A diagnostic detection assertion whose disposition is Confirmed and whose evidence has reached the confirmatory stage.

### bmo:Container

**Container**

The physical vessel holding a specimen or aliquot. Container identity may be required to establish continuity of custody.

### bmo:CustodyChain

**Custody chain**

The real sequence of custody-related processes from collection through transfer, receipt, storage, analysis, and disposition.

### bmo:CustodyEvent

**Custody event**

A recorded event affecting possession, location, identity, or integrity of a specimen or aliquot. Custody is represented as explicit events, not a single opaque provenance string.

### bmo:CustodyRecord

**Custody record**

The legally relevant information record describing a custody chain. It identifies custody events, their order, agents, timestamps, containers, seals, and integrity observations.

### bmo:Detection

**Detection (legacy term)**

Deprecated compatibility class from v0.2. New data should use DiagnosticDetectionAssertion or ConfirmedDetectionAssertion.

### bmo:DetectionLimit

**Detection limit**

A validated threshold below which a procedure cannot reliably distinguish presence from absence.

### bmo:DiagnosticCandidateSet

**Diagnostic candidate set**

The live competing hypotheses retained by the system at a point in the evidence-gathering workflow.

### bmo:DiagnosticDetectionAssertion

**Diagnostic detection assertion**

A scientific assertion about whether a specified pathogen is detected at a specified spatial support, derived from diagnostic evidence and carrying provenance, custody, method applicability, and rule version.

### bmo:DiagnosticDisposition

**Diagnostic disposition**

Overall diagnostic status of a pathogen determination. These values are kept separate from evidence stage and from quantitative or qualitative confidence.

### bmo:DiagnosticHypothesis

**Diagnostic hypothesis**

A revisable hypothesis about the cause of an observed anomaly. It may concern a pathogen, an abiotic stressor, or another causal agent and is explicitly not a detection.

### bmo:DiagnosticProcedure

**Diagnostic procedure**

An analysis process performed on a specimen or aliquot to produce diagnostic evidence. It is method-agnostic and may include molecular, serological, morphological, culture, sequencing, or future methods.

### bmo:DiagnosticProcedureProfile

**Diagnostic procedure profile**

A versioned description of where a diagnostic method is validated and how it performs: target organism, host, specimen matrix, sensitivity, specificity, limit of detection, and source of validation.

### bmo:DiagnosticResult

**Diagnostic result**

The result datum generated by a diagnostic procedure. A result is distinct from the later interpretation or detection assertion based on it.

### bmo:DiagnosticResultStatus

**Diagnostic result status**

Status of the result produced by a diagnostic procedure. It is not the same thing as an overall diagnostic disposition.

### bmo:EvidenceCompletenessLevel

**Evidence completeness level**

Controlled vocabulary for how complete the desired evidentiary record is.

### bmo:EvidenceStage

**Evidence stage**

Where an assertion sits in the evidence-gathering workflow. This is not a confidence scale.

### bmo:EvidenceStrengthLevel

**Evidence strength level**

Controlled vocabulary for qualitative strength of evidence supporting an assertion.

### bmo:ExternalReportingScheme

**External reporting scheme**

An external controlled vocabulary, repository, message standard, or reporting scheme to which Black Mesa data may be mapped.

### bmo:ExternalReportingTerm

**External reporting term**

A project-local proxy describing a term in an external reporting scheme when that scheme does not publish a stable RDF identifier. The source URL and notation are mandatory in crosswalk data.

### bmo:Farm

**Farm**

A managed agricultural holding under one operator. Access, consent, and many reporting obligations attach at this level.

### bmo:Field

**Field**

A bounded cultivated area within a farm, normally under a crop and management regime.

### bmo:Flight

**Flight**

An aerial survey sortie. Retained as a subtype because drones are an expected early platform, but the core ontology does not depend on flight.

### bmo:Host

**Host population**

The crop plants occupying a surveyed site. Taxonomic identity should be referenced to an external authority rather than replicated as local classes.

### bmo:ImageryReference

**Imagery reference**

A pointer to imagery or another large sensor artifact held outside the RDF graph. It carries a storage URI and content checksum so the evidence bytes can be retrieved and verified.

### bmo:ObservationRequirement

**Observation requirement**

A request for the observation that would most reduce uncertainty among live hypotheses.

### bmo:ObservedAnomaly

**Observed anomaly**

A derived record that some observation differs from an expected or reference condition. It is evidence that something warrants investigation, not a diagnosis.

### bmo:OperationalJurisdiction

**Operational jurisdiction**

A jurisdiction relevant to deployment, reporting, or regulatory evaluation. States are represented as data, not ontology subclasses.

### bmo:PilotPathosystem

**Pilot pathosystem profile**

A versionable profile selecting a host/pathogen pair for an operational pilot or regulatory stress test. The host and pathogen are referenced by canonical external taxon IRIs rather than redefined locally.

### bmo:PilotScenarioRole

**Pilot scenario role**

Controlled role describing whether a pathosystem profile is intended for operational evidence-chain testing or primarily for regulatory stress testing.

### bmo:ProvenanceQualityStatus

**Provenance quality status**

Controlled vocabulary for the integrity and completeness of the provenance and custody record.

### bmo:ReceiptEvent

**Receipt event**

A custody event recording receipt by a laboratory, facility, or other custodian.

### bmo:RegulatoryActionType

**regulatory action type**

Controlled action category used by reviewed reporting rules to describe the kind of follow-up a rule may require.

### bmo:RegulatoryDetermination

**Regulatory determination**

A determination made by an authorized body under a reporting or regulatory rule. It is deliberately separate from the underlying scientific detection assertion.

### bmo:ReportingCrosswalk

**Reporting crosswalk**

A directional, evidence-bearing mapping from an internal concept to an external reporting term or scheme. Fidelity is explicit; NoMapping is a legitimate result.

### bmo:ReportingDecision

**Reporting decision**

A decision about whether and how a scientific assertion is transmitted to an external reporting system or authority.

### bmo:ReportingRule

**Reporting rule**

A versioned rule specifying when, to whom, and in what representation a detection or determination should be reported.

### bmo:RuleReviewStatus

**rule review status**

Governance status for a jurisdictional reporting rule. Draft rules are non-operative until reviewed and approved by an authorized legal/regulatory reviewer.

### bmo:SampleCollection

**Sample collection**

The act of removing material from a site or host and creating a specimen with a persistent identity. It is simultaneously a sampling process and the first custody event.

### bmo:SamplingRecommendation

**Sampling recommendation**

A directive specifying what material should be collected, where, and why. It is generated from evidence and hypotheses rather than hard-coded to a sensor modality.

### bmo:SensorIndicationAssertion

**Sensor indication assertion**

An assertion that sensor evidence warrants further investigation. It does not assert that a pathogen is present and must not be flattened into a diagnostic disposition such as Suspected.

### bmo:SensorObservation

**Sensor observation**

An observation made by a sensing device under a procedure. The observation is an event; its result and later interpretation are separate.

### bmo:SpatialSupportDescription

**Spatial support description**

A description of the spatial footprint over which an observation or assertion is warranted: point, plant, row, polygon, field, raster footprint, sensor footprint, or sampling area.

### bmo:Specimen

**Specimen**

Material removed from a sampling target and assigned a persistent identity. The specimen remains distinct from any data or diagnosis produced about it.

### bmo:SpectralAnomaly

**Spectral anomaly**

An observed anomaly derived specifically from spectral data. This subtype preserves the original drone use case without making spectral sensing part of the core contract.

### bmo:StorageEvent

**Storage event**

A custody event recording controlled storage of a specimen or aliquot under stated conditions.

### bmo:SupportKind

**Support kind**

Controlled vocabulary describing the kind of spatial support represented by a support description.

### bmo:SurveyActivity

**Survey activity**

A surveillance activity using one or more sensors or observation procedures over one or more sites. It is intentionally independent of platform and sensor modality.

### bmo:TransferEvent

**Transfer event**

A custody event in which possession of a specimen or aliquot passes from one custodian to another.

### bmo:Zone

**Zone**

A sub-field place used for surveillance, sampling, or management. A zone is not assumed to be the finest spatial support of every observation.
