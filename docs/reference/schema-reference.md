<!-- GENERATED FILE - do not hand-edit. -->
<!-- Rebuild with tools/schema_docs.py; see docs/maintainers/generated-artifacts.md. -->

# Schema reference

Generated from the Turtle sources. Every description below is the term's own `rdfs:comment` - the schema documents itself, and this file is a reading view of it rather than a second copy that can drift.

**48 classes · 34 properties · 3 controlled vocabularies · 10 SHACL shapes**

Modules: *Detection core*, *Shared upper module*

Every class reaches [BFO 2.0](https://github.com/BFO-ontology/BFO) (ISO/IEC 21838-2) through the shared upper module, and a SHACL constraint refuses any that does not. The **kind** column is that anchor: the answer to *what kind of thing is this?*

## Contents

- [Classes](#classes)
- [Controlled vocabularies](#controlled-vocabularies)
- [Properties](#properties)
- [Constraints](#constraints)

## Classes

| Class | Kind | Parent |
|---|---|---|
| [`up:Capability`](#up-capability) | disposition | `obo:BFO_0000016` |
| [`bmo:Alert`](#bmo-alert) | information | `obo:IAO_0000033` |
| [`bmo:AssayResult`](#bmo-assayresult) | information | `obo:IAO_0000109` |
| [`bmo:ConfidenceAssessment`](#bmo-confidenceassessment) | information | `up:ConfidenceAssessment` |
| [`bmo:ConfidenceTier`](#bmo-confidencetier) | information | `up:ConceptualUnit` |
| [`bmo:Detection`](#bmo-detection) | information | `up:Assertion` |
| [`bmo:DetectionLimit`](#bmo-detectionlimit) | information | `up:ThresholdSpecification` |
| [`bmo:ImageryReference`](#bmo-imageryreference) | information | `up:InformationArtifact` |
| [`bmo:ObservationRequirement`](#bmo-observationrequirement) | information | `up:RequirementSpecification` |
| [`bmo:ReportingCrosswalk`](#bmo-reportingcrosswalk) | information | `up:Crosswalk` |
| [`bmo:SpectralAnomaly`](#bmo-spectralanomaly) | information | `up:DerivedDatum` |
| [`up:Assertion`](#up-assertion) | information | `up:InformationArtifact` |
| [`up:CandidateSet`](#up-candidateset) | information | `up:InformationArtifact` |
| [`up:ConceptualUnit`](#up-conceptualunit) | information | `up:InformationArtifact` |
| [`up:ConfidenceAssessment`](#up-confidenceassessment) | information | `up:InformationArtifact` |
| [`up:Crosswalk`](#up-crosswalk) | information | `up:InformationArtifact` |
| [`up:DerivedDatum`](#up-deriveddatum) | information | `obo:IAO_0000027` |
| [`up:EpistemicStatus`](#up-epistemicstatus) | information | `up:InformationArtifact` |
| [`up:EvidenceItem`](#up-evidenceitem) | information | `up:InformationArtifact` |
| [`up:ExternalAssignment`](#up-externalassignment) | information | `up:InformationArtifact` |
| [`up:InformationArtifact`](#up-informationartifact) | information | `obo:IAO_0000030` |
| [`up:MappingFidelity`](#up-mappingfidelity) | information | `up:InformationArtifact` |
| [`up:RequirementSpecification`](#up-requirementspecification) | information | `obo:IAO_0000007` |
| [`up:RuleSetVersion`](#up-rulesetversion) | information | `up:InformationArtifact` |
| [`up:SupportDescription`](#up-supportdescription) | information | `up:InformationArtifact` |
| [`up:ThresholdSpecification`](#up-thresholdspecification) | information | `obo:IAO_0000005` |
| [`bmo:Specimen`](#bmo-specimen) | matter | `up:Specimen` |
| [`up:Specimen`](#up-specimen) | matter | `obo:BFO_0000040` |
| [`bmo:Host`](#bmo-host) | matter (object aggregate) | `obo:BFO_0000027` |
| [`up:OccurrentAggregate`](#up-occurrentaggregate) | matter (object aggregate) | `obo:BFO_0000027` |
| [`bmo:Container`](#bmo-container) | matter (object) | `obo:BFO_0000030` |
| [`bmo:Farm`](#bmo-farm) | place (site) | `up:SurveyedSite` |
| [`bmo:Field`](#bmo-field) | place (site) | `up:SurveyedSite` |
| [`bmo:Zone`](#bmo-zone) | place (site) | `up:SurveyedSite` |
| [`up:SurveyedSite`](#up-surveyedsite) | place (site) | `obo:BFO_0000029` |
| [`bmo:Assay`](#bmo-assay) | process | `up:AnalysisProcess` |
| [`bmo:CustodyChain`](#bmo-custodychain) | process | `up:ProvenanceChain` |
| [`bmo:Flight`](#bmo-flight) | process | `up:ObservationProcess` |
| [`bmo:SampleCollection`](#bmo-samplecollection) | process | `up:SamplingProcess` |
| [`up:AnalysisProcess`](#up-analysisprocess) | process | `up:RecordedProcess` |
| [`up:DisturbanceEvent`](#up-disturbanceevent) | process | `up:RecordedProcess` |
| [`up:ObservationProcess`](#up-observationprocess) | process | `up:RecordedProcess` |
| [`up:ProvenanceChain`](#up-provenancechain) | process | `up:RecordedProcess` |
| [`up:RecordedProcess`](#up-recordedprocess) | process | `obo:BFO_0000015` |
| [`up:SamplingProcess`](#up-samplingprocess) | process | `up:RecordedProcess` |
| [`up:TransformationEvent`](#up-transformationevent) | process | `up:RecordedProcess` |
| [`up:Condition`](#up-condition) | quality | `obo:BFO_0000019` |
| [`up:EvidentialRole`](#up-evidentialrole) | role | `obo:BFO_0000023` |

### Disposition

#### `up:Capability`

**Capability**

Subclass of `obo:BFO_0000016`.

What an observer, instrument, or method is able to determine. A disposition: it exists whether or not it is exercised, and it is what makes a requirement satisfiable by one channel and not another.

### Information

#### `bmo:Alert`

**Alert**

Subclass of `obo:IAO_0000033`.

A directive issued to a recipient on the basis of one or more detections.

Deliberately separate from Detection and joined by a defeasible link. Raising an alert has consequences for a grower, a programme, and possibly a market, and that decision is not the same claim as the determination that a pathogen is present. Keeping them apart lets alerting policy change without rewriting the diagnostic record.

#### `bmo:AssayResult`

**Assay result**

Subclass of `obo:IAO_0000109`.

The datum produced by an assay: a determination for a target pathogen, with the assay's own detection limit and validity conditions attached.

#### `bmo:ConfidenceAssessment`

**Confidence assessment**

Subclass of `up:ConfidenceAssessment`.

The multi-axis confidence attached to a detection. A single number cannot distinguish a calibrated model output from an expert guess rendered as a decimal.

Properties: [`bmo:assayApplicability`](#bmo-assayapplicability), [`bmo:calibratedProbability`](#bmo-calibratedprobability), [`bmo:evidenceCompleteness`](#bmo-evidencecompleteness), [`bmo:evidenceStrength`](#bmo-evidencestrength), [`bmo:hasTier`](#bmo-hastier), [`bmo:provenanceQuality`](#bmo-provenancequality)

#### `bmo:ConfidenceTier`

**Confidence tier**

Subclass of `up:ConceptualUnit`.

A term in the adopted diagnostic confidence enumeration, extended with the pre-symptomatic tier.

Properties: [`bmo:presupposesSymptoms`](#bmo-presupposessymptoms), [`bmo:tierRank`](#bmo-tierrank)

#### `bmo:Detection`

**Detection**

Subclass of `up:Assertion`.

The assertion that a pathogen is present at a zone at a time.

Not a property of the zone, not a flag on a sample, not a row in a results table. An assertion carrying what concluded it, from what evidence, under which rule version, and with what confidence - because a detection that cannot be explained cannot be reviewed, and a rule change must not silently rewrite conclusions already drawn.

Properties: [`bmo:assertsPathogen`](#bmo-assertspathogen), [`bmo:concernsZone`](#bmo-concernszone), [`bmo:derivedFromResult`](#bmo-derivedfromresult), [`bmo:hasCustodyChain`](#bmo-hascustodychain), [`bmo:triggeredAlert`](#bmo-triggeredalert)

#### `bmo:DetectionLimit`

**Detection limit**

Subclass of `up:ThresholdSpecification`.

The concentration below which an assay cannot distinguish presence from absence. A specification: chosen and validated rather than discovered, so it carries its validation evidence.

#### `bmo:ImageryReference`

**Imagery reference**

Subclass of `up:InformationArtifact`.

A pointer to imagery held in object storage: a URI, a checksum, and the capture parameters needed to interpret it.

THE GRAPH BOUNDARY. Raw spectral imagery is never tiled into the graph. The graph retains the reference and provenance needed to locate the bytes, while raw imagery remains in an external storage system. This is a conceptual boundary, not a benchmark or storage implementation claim.

Properties: [`bmo:checksum`](#bmo-checksum), [`bmo:storageURI`](#bmo-storageuri)

#### `bmo:ObservationRequirement`

**Observation requirement**

Subclass of `up:RequirementSpecification`.

A request for the observation that would most reduce uncertainty: target property, required accuracy, spatial support, purpose, acceptable methods. Observer-neutral by construction.

#### `bmo:ReportingCrosswalk`

**Reporting crosswalk**

Subclass of `up:Crosswalk`.

A mapping from an internal term to an external reporting vocabulary, carrying direction and fidelity. Entries with fidelity up:NoMapping are the valuable output: the pre-symptomatic tier is the known case.

#### `bmo:SpectralAnomaly`

**Spectral anomaly**

Subclass of `up:DerivedDatum`.

A record of a deviation detected in sensed imagery, localised to a zone.

Information, not a material condition: the anomaly is a pattern found in data that may or may not correspond to anything in the field. Treating it as a condition of the crop is the first place this domain slips from evidence into conclusion.

Properties: [`bmo:referencesImagery`](#bmo-referencesimagery), [`bmo:triggeredCollection`](#bmo-triggeredcollection)

#### `up:Assertion`

**Assertion**

Subclass of `up:InformationArtifact`.

A claim reached from evidence by some agent at some time, under some version of a rule set.

The defining test: if two competent people could disagree about it, or if revising the producing rule should not silently rewrite history, it is an assertion rather than a property. Every assertion carries its evidence, its provenance, and its time.

Properties: [`up:assertedBy`](#up-assertedby), [`up:contradictedBy`](#up-contradictedby), [`up:generatedUnder`](#up-generatedunder), [`up:hasConfidence`](#up-hasconfidence), [`up:recommendsNext`](#up-recommendsnext), [`up:supportedBy`](#up-supportedby)

#### `up:CandidateSet`

**Candidate set**

Subclass of `up:InformationArtifact`.

The live hypotheses under consideration, with their support. Retaining alternatives is a requirement in both projects, so the set is a first-class object rather than an implicit by-product.

#### `up:ConceptualUnit`

**Conceptual unit**

Subclass of `up:InformationArtifact`.

A term in a classification scheme: an ecosystem type, a diagnostic category, a risk category.

Modelled as information rather than as a universal because what the system holds is the CONCEPT as published in a scheme - with a label, a notation, a source, and a revision history - not the universal it denotes. The denotation is recorded with obo:IAO_0000219 (denotes). Conflating the two is what makes classification schemes impossible to version.

#### `up:ConfidenceAssessment`

**Confidence assessment**

Subclass of `up:InformationArtifact`.

A multi-axis statement of how much weight an assertion can bear. Separate from the assertion so that the same claim can be reassessed without being restated.

#### `up:Crosswalk`

**Crosswalk**

Subclass of `up:InformationArtifact`.

A directed, defeasible mapping between a local conceptual unit and an external one, carrying a fidelity and the evidence for it. Deliberately not owl:equivalentClass: a crosswalk can be partial, contested, or absent, and 'absent' is a finding.

Properties: [`up:crosswalkFrom`](#up-crosswalkfrom), [`up:crosswalkTo`](#up-crosswalkto), [`up:fidelity`](#up-fidelity)

#### `up:DerivedDatum`

**Derived datum**

Subclass of `obo:IAO_0000027`.

An interpretation computed from one or more measurements, kept separate from them so the interpretation can be revised without touching what was measured.

#### `up:EpistemicStatus`

**Epistemic status**

Subclass of `up:InformationArtifact`.

The standing of a unit or assignment: established in a published source, proposed as a hypothesis, or a candidate awaiting governance. Declared structurally so nothing enters a graph without saying what it is.

#### `up:EvidenceItem`

**Evidence item**

Subclass of `up:InformationArtifact`.

The bearing of an observation or derived datum on a candidate conclusion - supporting, contradicting, or discriminating. Evidence is itself information: the same measurement can be strong evidence for one hypothesis and none at all for another.

#### `up:ExternalAssignment`

**External assignment**

Subclass of `up:InformationArtifact`.

What some pre-existing external source says about a location or entity - a map unit, a prior record, a legacy label. Information, and therefore evidence, never ground truth.

#### `up:InformationArtifact`

**Information artifact**

Subclass of `obo:IAO_0000030`.

Anything in either project that is about the world rather than part of it. Root of the information family; specialise rather than using directly.

Properties: [`up:epistemicStatus`](#up-epistemicstatus)

#### `up:MappingFidelity`

**Mapping fidelity**

Subclass of `up:InformationArtifact`.

How completely a crosswalk entry preserves the meaning of the term it maps. An enumeration rather than a score, because the distinctions are kinds of mismatch and not degrees of one: the value that matters most is none, which records that a term has no counterpart and that mapping it to the nearest available label would lose the thing it was minted to express.

#### `up:RequirementSpecification`

**Requirement specification**

Subclass of `obo:IAO_0000007`.

A specification of an action to be performed - what must be observed or measured, to what accuracy, over what support, and why. A directive rather than a description, which is why it anchors to IAO's action specification.

Properties: [`up:discriminates`](#up-discriminates)

#### `up:RuleSetVersion`

**Rule set version**

Subclass of `up:InformationArtifact`.

An identified version of the rules, thresholds or method by which assertions are produced. It exists as a class rather than a version string so that the rules in force can be described, superseded and cited, which a literal cannot be: reinterpreting an old assertion means retrieving the rules it was made under, not guessing at them.

#### `up:SupportDescription`

**Support description**

Subclass of `up:InformationArtifact`.

A record of the spatial footprint, resolution, positional uncertainty and temporal extent over which an observation holds.

Note it is a DESCRIPTION of a spatiotemporal region, not the region itself. The region is an occurrent (obo:BFO_0000011); what the system stores is information about it, which can be wrong.

#### `up:ThresholdSpecification`

**Threshold specification**

Subclass of `obo:IAO_0000005`.

A specified boundary value at which a determination changes - a collapse threshold, a detection limit, a reporting cut-off. An objective specification: it states an endpoint against which something is judged, and it is chosen rather than discovered, so it must carry its justification.

### Matter

#### `bmo:Specimen`

**Specimen**

Subclass of `up:Specimen`.

Plant or soil material removed from a zone and held in a container. A material entity with its own identity: the same specimen can be split, re-assayed, or lost, and each of those is a fact about the specimen rather than about the zone.

#### `up:Specimen`

**Specimen**

Subclass of `obo:BFO_0000040`.

Material removed from a site for analysis. A material entity with its own identity and custody history, distinct both from the site it came from and from any datum produced about it.

### Matter (object aggregate)

#### `bmo:Host`

**Host population**

Subclass of `obo:BFO_0000027`.

The crop plants occupying a zone. An object aggregate; the taxon it instantiates is referenced by NCBITaxon IRI rather than restated here.

#### `up:OccurrentAggregate`

**Occurrent aggregate**

Subclass of `obo:BFO_0000027`.

A material aggregate occupying a site over an interval - the actual organisms and material present, as opposed to the concept under which they are classified.

The name is unfortunate in one respect: 'occurrent' here follows domain usage (an occurrence of a type at a place) and NOT the BFO sense of occurrent. It is a continuant. Domain ontologies should use their own clearer label.

### Matter (object)

#### `bmo:Container`

**Container**

Subclass of `obo:BFO_0000030`.

The vessel a specimen is held in. Tracked because container identity is how custody is demonstrated between collection and assay.

### Place (site)

#### `bmo:Farm`

**Farm**

Subclass of `up:SurveyedSite`.

A managed holding under one operator. The unit at which access, consent, and reporting obligations attach.

#### `bmo:Field`

**Field**

Subclass of `up:SurveyedSite`.

A bounded cultivated area within a farm, normally under a single crop and management regime.

#### `bmo:Zone`

**Zone**

Subclass of `up:SurveyedSite`.

A sub-field area distinguished for sampling or management. The finest place at which a detection is asserted, because asserting at field level would overstate what a point sample supports.

#### `up:SurveyedSite`

**Surveyed site**

Subclass of `obo:BFO_0000029`.

A bounded place that observations are made of and assertions are made about - a field, a zone, a stand, a plot. A site in BFO is immaterial: it is the place, not what occupies it.

Properties: [`bmo:partOfSite`](#bmo-partofsite)

### Process

#### `bmo:Assay`

**Assay**

Subclass of `up:AnalysisProcess`.

The confirmation analysis performed on a specimen, producing an assay result. Aligned with OBI's assay, which is likewise a planned process.

Properties: [`bmo:assayed`](#bmo-assayed), [`bmo:producedResult`](#bmo-producedresult)

#### `bmo:CustodyChain`

**Custody chain**

Subclass of `up:ProvenanceChain`.

The ordered whole of the acts producing a detection: flight, anomaly registration, collection, transfer, assay.

A process aggregate, not a document. A detection that cannot be resolved back along this chain is not evidence, and retrofitting the chain onto records created without it is what makes early records unusable.

#### `bmo:Flight`

**Flight**

Subclass of `up:ObservationProcess`.

A single sortie over one or more sites, producing imagery and zero or more anomaly records.

Zero is the important cardinality: a sortie that finds nothing is a recorded event with a negative result, not an absence of data. Without it nobody can say how much of a season was surveyed.

Properties: [`bmo:producedAnomaly`](#bmo-producedanomaly)

#### `bmo:SampleCollection`

**Sample collection**

Subclass of `up:SamplingProcess`.

The act of the sampling arm removing plant or soil material at a zone, producing a specimen.

Properties: [`bmo:yieldedSpecimen`](#bmo-yieldedspecimen)

#### `up:AnalysisProcess`

**Analysis process**

Subclass of `up:RecordedProcess`.

An act performed on a specimen or datum that yields a determination - an assay, a laboratory analysis, a classifier run.

#### `up:DisturbanceEvent`

**Disturbance event**

Subclass of `up:RecordedProcess`.

An act of nature or of people that resets or perturbs a system without necessarily changing what kind of thing it is: a storm, a fire, a flood, a harvest, an outbreak.

The contrast with TransformationEvent is the whole point of having both. A disturbance leaves the entity instantiating the same type in a different condition - a burnt pine woodland is still a pine woodland. A transformation leaves it instantiating a different type, or none. Recurrent disturbance is often the very process that MAINTAINS a type, so recording disturbances as damage would invert the ecology.

#### `up:ObservationProcess`

**Observation process**

Subclass of `up:RecordedProcess`.

An act of observing or measuring, carried out by an agent or instrument upon some entity, producing a measurement datum as output. Aligned with sosa:Observation, which is likewise an activity rather than a result.

#### `up:ProvenanceChain`

**Provenance chain**

Subclass of `up:RecordedProcess`.

The ordered whole made of the processes that produced a result, from first observation to final determination.

A process aggregate rather than an information artifact: the chain IS the sequence of acts. What is recorded about it is separate, and may be incomplete.

#### `up:RecordedProcess`

**Recorded process**

Subclass of `obo:BFO_0000015`.

An act the system keeps a record of: an observation, a sampling, an analysis, a disturbance, a transformation.

The common ancestor of every process either project tracks. It exists so that the properties shared by all of them are declared once, and so that a query for 'everything that happened at this place' does not have to enumerate process types and silently miss the one added last month.

Membership test: if the act needs to be dated, attributed, and placed in order against other acts, it belongs here. A process nobody records - wind, photosynthesis, erosion in general - does not, and adding it would make the class mean nothing.

#### `up:SamplingProcess`

**Sampling process**

Subclass of `up:RecordedProcess`.

An act of collecting material from a site, producing a specimen as output. Distinct from observation: it removes matter rather than only recording.

#### `up:TransformationEvent`

**Transformation event**

Subclass of `up:RecordedProcess`.

A process that changes what a site or entity is, rather than merely its condition: conversion, construction, restoration, collapse. What makes a transformation different from a state change is that the entity afterwards may no longer instantiate the type it did before. See DisturbanceEvent for the case where only the condition changes.

### Quality

#### `up:Condition`

**Condition**

Subclass of `obo:BFO_0000019`.

The condition of a real entity at a time - disturbed, recovering, suppressed, mature, degraded.

A quality inhering in the entity, related with obo:RO_0000052 (characteristic of). RESERVED for actual entities. A claim about what an entity was or could be is an Assertion, never a Condition: that separation is what stops a hypothesis about the past becoming a property of the present.

### Role

#### `up:EvidentialRole`

**Evidential role**

Subclass of `obo:BFO_0000023`.

The role a conceptual unit plays within a particular assertion - serving as a reference condition, a prior, a comparator.

A role rather than a class because the same unit plays different roles in different assertions. Modelling each role as a class would produce parallel hierarchies of the same concepts, which is the error this term exists to prevent.

## Controlled vocabularies

### `bmo:ConfidenceTier`

A term in the adopted diagnostic confidence enumeration, extended with the pre-symptomatic tier.

| Member | Label | Meaning |
|---|---|---|
| `bmo:Confirmed` | Confirmed | Adopted level. Diagnosis established to the standard the receiving network requires. |
| `bmo:NotDetected` | Not detected | Adopted level. The assay ran and returned negative, which is not the same as not having looked. |
| `bmo:PreSymptomatic` | Pre-symptomatic indication | THE INVENTED TERM. A sensor-derived indication that a sample is warranted, carrying no claim that disease is present.<br><br>It licenses sampling and nothing else. It is NOT a weaker 'suspected': it is a different kind of claim, made on different evidence, warranting a different action, and modelling it as a lower value on the same scale would let it be compared numerically against claims it is not commensurate with.<br><br>It is also the term most at risk at every integration boundary, because mapping it to the nearest existing bucket is locally reasonable every time and cumulatively destroys the platform's distinguishing output. The schema cannot prevent that; it can only make the loss explicit through a ReportingCrosswalk with fidelity up:NoMapping. |
| `bmo:Suspected` | Suspected | Adopted level. PRESUPPOSES VISIBLE SYMPTOMS - which is precisely why it cannot absorb a pre-symptomatic indication. |
| `bmo:Undetermined` | Undetermined | Adopted level. The assay ran and could not conclude. |

### `up:EpistemicStatus`

The standing of a unit or assignment: established in a published source, proposed as a hypothesis, or a candidate awaiting governance. Declared structurally so nothing enters a graph without saying what it is.

| Member | Label | Meaning |
|---|---|---|
| `up:Candidate` | candidate | A recurrent pattern that has met replication criteria but not passed governance review. |
| `up:Established` | established | A published unit in an existing authoritative source. |
| `up:Hypothesis` | hypothesis | Proposed by this work, for testing. Never an endorsement by the body owning the scheme. |

### `up:MappingFidelity`

How completely a crosswalk entry preserves the meaning of the term it maps. An enumeration rather than a score, because the distinctions are kinds of mismatch and not degrees of one: the value that matters most is none, which records that a term has no counterpart and that mapping it to the nearest available label would lose the thing it was minted to express.

| Member | Label | Meaning |
|---|---|---|
| `up:Broader` | broader | - |
| `up:Exact` | exact | - |
| `up:Narrower` | narrower | - |
| `up:NoMapping` | none | No defensible mapping exists. A finding to be reported, not a gap to be filled with the nearest available term. |
| `up:Partial` | partial | - |

## Properties

| Property | Domain | Range |
|---|---|---|
| [`bmo:assayApplicability`](#bmo-assayapplicability) | `bmo:ConfidenceAssessment` | `xsd:string` |
| [`bmo:assayed`](#bmo-assayed) | `bmo:Assay` | `bmo:Specimen` |
| [`bmo:assertsPathogen`](#bmo-assertspathogen) | `bmo:Detection` | `obo:NCBITaxon_1` |
| [`bmo:calibratedProbability`](#bmo-calibratedprobability) | `bmo:ConfidenceAssessment` | `xsd:decimal` |
| [`bmo:checksum`](#bmo-checksum) | `bmo:ImageryReference` | `xsd:string` |
| [`bmo:concernsZone`](#bmo-concernszone) | `bmo:Detection` | `bmo:Zone` |
| [`bmo:derivedFromResult`](#bmo-derivedfromresult) | `bmo:Detection` | `bmo:AssayResult` |
| [`bmo:evidenceCompleteness`](#bmo-evidencecompleteness) | `bmo:ConfidenceAssessment` | `xsd:string` |
| [`bmo:evidenceStrength`](#bmo-evidencestrength) | `bmo:ConfidenceAssessment` | `xsd:string` |
| [`bmo:hasCustodyChain`](#bmo-hascustodychain) | `bmo:Detection` | `bmo:CustodyChain` |
| [`bmo:hasTier`](#bmo-hastier) | `bmo:ConfidenceAssessment` | `bmo:ConfidenceTier` |
| [`bmo:partOfSite`](#bmo-partofsite) | `up:SurveyedSite` | `up:SurveyedSite` |
| [`bmo:presupposesSymptoms`](#bmo-presupposessymptoms) | `bmo:ConfidenceTier` | `xsd:boolean` |
| [`bmo:producedAnomaly`](#bmo-producedanomaly) | `bmo:Flight` | `bmo:SpectralAnomaly` |
| [`bmo:producedResult`](#bmo-producedresult) | `bmo:Assay` | `bmo:AssayResult` |
| [`bmo:provenanceQuality`](#bmo-provenancequality) | `bmo:ConfidenceAssessment` | `xsd:string` |
| [`bmo:referencesImagery`](#bmo-referencesimagery) | `bmo:SpectralAnomaly` | `bmo:ImageryReference` |
| [`bmo:storageURI`](#bmo-storageuri) | `bmo:ImageryReference` | `xsd:anyURI` |
| [`bmo:tierRank`](#bmo-tierrank) | `bmo:ConfidenceTier` | `xsd:integer` |
| [`bmo:triggeredAlert`](#bmo-triggeredalert) | `bmo:Detection` | `bmo:Alert` |
| [`bmo:triggeredCollection`](#bmo-triggeredcollection) | `bmo:SpectralAnomaly` | `bmo:SampleCollection` |
| [`bmo:yieldedSpecimen`](#bmo-yieldedspecimen) | `bmo:SampleCollection` | `bmo:Specimen` |
| [`up:assertedBy`](#up-assertedby) | `up:Assertion` | `prov:Agent` |
| [`up:contradictedBy`](#up-contradictedby) | `up:Assertion` | `up:EvidenceItem` |
| [`up:crosswalkFrom`](#up-crosswalkfrom) | `up:Crosswalk` | `up:ConceptualUnit` |
| [`up:crosswalkTo`](#up-crosswalkto) | `up:Crosswalk` | `rdfs:Resource` |
| [`up:discriminates`](#up-discriminates) | `up:RequirementSpecification` | `up:ConceptualUnit` |
| [`up:epistemicStatus`](#up-epistemicstatus) | `up:InformationArtifact` | `up:EpistemicStatus` |
| [`up:fidelity`](#up-fidelity) | `up:Crosswalk` | `up:MappingFidelity` |
| [`up:generatedUnder`](#up-generatedunder) | `up:Assertion` | `up:RuleSetVersion` |
| [`up:hasConfidence`](#up-hasconfidence) | `up:Assertion` | `up:ConfidenceAssessment` |
| [`up:hasSupportDescription`](#up-hassupportdescription) | `obo:IAO_0000027` | `up:SupportDescription` |
| [`up:recommendsNext`](#up-recommendsnext) | `up:Assertion` | `up:RequirementSpecification` |
| [`up:supportedBy`](#up-supportedby) | `up:Assertion` | `up:EvidenceItem` |

#### `bmo:assayApplicability`

**assay applicability**

`bmo:ConfidenceAssessment` → `xsd:string`

Whether the assay was validated for this pathogen, host, and matrix. The axis most often omitted and the one that matters most: an assay used outside its validation has no sensitivity figure that applies.

#### `bmo:assayed`

**assayed**

`bmo:Assay` → `bmo:Specimen`

The assay takes the specimen as input.

#### `bmo:assertsPathogen`

**asserts pathogen**

`bmo:Detection` → `obo:NCBITaxon_1`

The taxon asserted present, referenced by NCBITaxon IRI. Referenced, never restated: the taxonomy is reference data, not schema. The range is the NCBITaxon root, which states the expectation — values are NCBITaxon IRIs and nothing else — without importing 2.4 million taxa to say so.

#### `bmo:calibratedProbability`

**calibrated probability**

`bmo:ConfidenceAssessment` → `xsd:decimal`

Present ONLY where a probabilistic model produced it. Absence is meaningful and must never be imputed.

#### `bmo:checksum`

**checksum**

`bmo:ImageryReference` → `xsd:string`

Content hash, so the reference can be shown to resolve to the bytes that were analysed.

#### `bmo:concernsZone`

**concerns zone**

`bmo:Detection` → `bmo:Zone`

What the detection is about. A specialisation of IAO is-about, because a detection is information about a place.

#### `bmo:derivedFromResult`

**derived from result**

`bmo:Detection` → `bmo:AssayResult`

_No description._

#### `bmo:evidenceCompleteness`

**evidence completeness**

`bmo:ConfidenceAssessment` → `xsd:string`

_No description._

#### `bmo:evidenceStrength`

**evidence strength**

`bmo:ConfidenceAssessment` → `xsd:string`

_No description._

#### `bmo:hasCustodyChain`

**has custody chain**

`bmo:Detection` → `bmo:CustodyChain`

_No description._

#### `bmo:hasTier`

**has tier**

`bmo:ConfidenceAssessment` → `bmo:ConfidenceTier`

_No description._

#### `bmo:partOfSite`

**part of site**

`up:SurveyedSite` → `up:SurveyedSite`

Zone to field, field to farm. A specialisation of BFO part-of rather than a parallel containment relation.

#### `bmo:presupposesSymptoms`

**presupposes symptoms**

`bmo:ConfidenceTier` → `xsd:boolean`

Whether the tier can only be reached once symptoms are visible. The property that makes the gap in the adopted enumeration machine-readable.

#### `bmo:producedAnomaly`

**produced anomaly**

`bmo:Flight` → `bmo:SpectralAnomaly`

Flight to spectral anomaly. Zero or more.

#### `bmo:producedResult`

**produced result**

`bmo:Assay` → `bmo:AssayResult`

_No description._

#### `bmo:provenanceQuality`

**provenance quality**

`bmo:ConfidenceAssessment` → `xsd:string`

_No description._

#### `bmo:referencesImagery`

**references imagery**

`bmo:SpectralAnomaly` → `bmo:ImageryReference`

Links an anomaly to the imagery it was found in, by reference. The only permitted relation to imagery: no tiling, no per-pixel triples.

#### `bmo:storageURI`

**storage URI**

`bmo:ImageryReference` → `xsd:anyURI`

_No description._

#### `bmo:tierRank`

**tier rank**

`bmo:ConfidenceTier` → `xsd:integer`

Ordering within the enumeration. Ranks are not a probability scale and must not be arithmetic.

#### `bmo:triggeredAlert`

**triggered alert**

`bmo:Detection` → `bmo:Alert`

Detection to alert. At most one, and frequently none.

#### `bmo:triggeredCollection`

**triggered collection**

`bmo:SpectralAnomaly` → `bmo:SampleCollection`

Anomaly to the collection act it prompted. Exactly one.

#### `bmo:yieldedSpecimen`

**yielded specimen**

`bmo:SampleCollection` → `bmo:Specimen`

_No description._

#### `up:assertedBy`

**asserted by**

`up:Assertion` → `prov:Agent`

The agent or process that produced this assertion.

#### `up:contradictedBy`

**contradicted by**

`up:Assertion` → `up:EvidenceItem`

Evidence bearing against this assertion, retained rather than discarded. An assertion with no recorded contradiction is not thereby uncontradicted; it may simply never have been challenged.

#### `up:crosswalkFrom`

**crosswalk from**

`up:Crosswalk` → `up:ConceptualUnit`

_No description._

#### `up:crosswalkTo`

**crosswalk to**

`up:Crosswalk` → `rdfs:Resource`

The external term this crosswalk maps to. The range is deliberately open: the target is an identifier in a foreign vocabulary, and constraining it to a locally declared class would mean restating that vocabulary here, which is the opposite of what a crosswalk is for.

#### `up:discriminates`

**discriminates**

`up:RequirementSpecification` → `up:ConceptualUnit`

The candidates a requirement is intended to separate. A requirement that discriminates nothing is a fixed protocol step, not an adaptive request.

#### `up:epistemicStatus`

**epistemic status**

`up:InformationArtifact` → `up:EpistemicStatus`

_No description._

#### `up:fidelity`

**fidelity**

`up:Crosswalk` → `up:MappingFidelity`

How well the mapping holds: exact, broader, narrower, partial, or none.

#### `up:generatedUnder`

**generated under**

`up:Assertion` → `up:RuleSetVersion`

The rule set or method version in force when the assertion was produced. Without it, a rule change makes every past assertion uninterpretable.

#### `up:hasConfidence`

**has confidence**

`up:Assertion` → `up:ConfidenceAssessment`

_No description._

#### `up:hasSupportDescription`

**has support description**

`obo:IAO_0000027` → `up:SupportDescription`

_No description._

#### `up:recommendsNext`

**recommends next**

`up:Assertion` → `up:RequirementSpecification`

The requirement whose satisfaction would most reduce remaining uncertainty. What makes a system adaptive rather than merely descriptive.

#### `up:supportedBy`

**supported by**

`up:Assertion` → `up:EvidenceItem`

Evidence bearing in favour of this assertion.

## Constraints

SHACL shapes, with the message each constraint fails with. The messages are written to be read by whoever trips them years from now, so they state the reasoning and cite the standard where there is one. Each is exercised against a deliberate violation in `tests/fixtures/` - a constraint that has only ever seen valid data is untested.

### `bmo:AssayShape`

Targets `bmo:Assay`.

- **`bmo:assayed`** — An assay takes exactly one specimen as input.
- **`bmo:producedResult`** — An assay produces exactly one result. A re-run is a different assay.

### `bmo:ConfidenceAssessmentShape`

Targets `bmo:ConfidenceAssessment`.

- **`bmo:hasTier`** — A confidence assessment names exactly one tier.
- **`bmo:calibratedProbability`** — Calibrated probability must be a single value in [0,1], present only where a probabilistic model produced it. Its absence is meaningful and must not be imputed.
- **`bmo:assayApplicability`** — Assay applicability must be recorded. An assay used outside its validation has no sensitivity figure that applies to the situation, and omitting this axis hides that.

### `bmo:ConfidenceTierShape`

Targets `bmo:ConfidenceTier`.

- **`bmo:presupposesSymptoms`** — Every tier must declare whether it presupposes visible symptoms. This is what makes the gap in the adopted enumeration machine-readable rather than a matter of prose.

### `bmo:DetectionShape`

Targets `bmo:Detection`.

- **`bmo:concernsZone`** — A detection must concern exactly one zone. Asserting at field or farm level overstates what a point sample supports.
- **`bmo:derivedFromResult`** — A detection must derive from at least one assay result. A detection with no result behind it is an opinion.
- **`bmo:hasCustodyChain`** — A detection must carry a custody chain. A detection that cannot be resolved back to the flight, collection and assay that produced it is not evidence, and provenance cannot be retrofitted.
- **`up:generatedUnder`** — A detection must record the rule set version in force when it was produced. Without it, a later rule change makes every past detection uninterpretable.
- **`bmo:triggeredAlert`** — A detection triggers at most one alert. Raising an alert is a separate decision from determining presence.

### `bmo:ImageryReferenceShape`

Targets `bmo:ImageryReference`.

- **`bmo:storageURI`** — An imagery reference must carry exactly one storage URI.
- **`bmo:checksum`** — An imagery reference must carry a checksum, so it can be shown to resolve to the bytes that were analysed.

### `bmo:NoTiledImageryShape`

Targets `bmo:ImageryReference`.

- **`(SPARQL)`** — GRAPH BOUNDARY VIOLATION: imagery must be referenced by URI and checksum, never tiled into the graph. Per-tile, per-pixel, and per-band statements are outside this conceptual schema boundary.

### `bmo:ObservationRequirementShape`

Targets `bmo:ObservationRequirement`.

- **`up:discriminates`** — A requirement must state what it discriminates. A request with no diagnostic purpose is a fixed protocol step, not an adaptive one.

### `bmo:ReportingCrosswalkShape`

Targets `bmo:ReportingCrosswalk`.

- **`up:crosswalkFrom`** — A crosswalk must name the internal term it maps from.
- **`up:fidelity`** — A crosswalk must state its fidelity: exact, broader, narrower, partial, or none. A mapping with unstated fidelity silently claims exactness it does not have.

### `bmo:SpectralAnomalyShape`

Targets `bmo:SpectralAnomaly`.

- **`bmo:triggeredCollection`** — An anomaly triggers at most one collection.
- **`bmo:referencesImagery`** — An anomaly must reference the imagery it was found in, so the finding can be re-examined against the bytes that produced it.

### `bmo:UpperAnchorShape`

Targets `owl:Class`.

- **`(SPARQL)`** — UNANCHORED CLASS: every domain class must reach BFO via the shared upper module (upper/upper-core.ttl). Declare what kind of thing it is - an information artifact, a process, a material entity, a site, a quality, or a role.

