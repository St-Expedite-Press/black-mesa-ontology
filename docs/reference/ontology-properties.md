<!-- GENERATED FILE - do not hand-edit. -->
<!-- Rebuild with tools/schema_docs.py; see docs/maintainers/generated-artifacts.md. -->

# Ontology property index

Generated from the current ontology import closure. Domain and range are declarations, not closed-world validation guarantees.

| Property | Domain | Range | Description |
|---|---|---|---|
| `bmo:assayApplicability` | `bmo:ConfidenceAssessment` | `xsd:string` | Whether the assay was validated for this pathogen, host, and matrix. The axis most often omitted and the one that matters most: an assay used outside its validation has no sensitivity figure that applies. |
| `bmo:assayed` | `bmo:Assay` | `bmo:Specimen` | The assay takes the specimen as input. |
| `bmo:assertsPathogen` | `bmo:Detection` | `obo:NCBITaxon_1` | The taxon asserted present, referenced by NCBITaxon IRI. Referenced, never restated: the taxonomy is reference data, not schema. The range is the NCBITaxon root, which states the expectation — values are NCBITaxon IRIs and nothing else — without importing 2.4 million taxa to say so. |
| `bmo:calibratedProbability` | `bmo:ConfidenceAssessment` | `xsd:decimal` | Present ONLY where a probabilistic model produced it. Absence is meaningful and must never be imputed. |
| `bmo:checksum` | `bmo:ImageryReference` | `xsd:string` | Content hash, so the reference can be shown to resolve to the bytes that were analysed. |
| `bmo:concernsZone` | `bmo:Detection` | `bmo:Zone` | What the detection is about. A specialisation of IAO is-about, because a detection is information about a place. |
| `bmo:derivedFromResult` | `bmo:Detection` | `bmo:AssayResult` | No source comment. |
| `bmo:evidenceCompleteness` | `bmo:ConfidenceAssessment` | `xsd:string` | No source comment. |
| `bmo:evidenceStrength` | `bmo:ConfidenceAssessment` | `xsd:string` | No source comment. |
| `bmo:hasCustodyChain` | `bmo:Detection` | `bmo:CustodyChain` | No source comment. |
| `bmo:hasTier` | `bmo:ConfidenceAssessment` | `bmo:ConfidenceTier` | No source comment. |
| `bmo:partOfSite` | `up:SurveyedSite` | `up:SurveyedSite` | Zone to field, field to farm. A specialisation of BFO part-of rather than a parallel containment relation. |
| `bmo:presupposesSymptoms` | `bmo:ConfidenceTier` | `xsd:boolean` | Whether the tier can only be reached once symptoms are visible. The property that makes the gap in the adopted enumeration machine-readable. |
| `bmo:producedAnomaly` | `bmo:Flight` | `bmo:SpectralAnomaly` | Flight to spectral anomaly. Zero or more. |
| `bmo:producedResult` | `bmo:Assay` | `bmo:AssayResult` | No source comment. |
| `bmo:provenanceQuality` | `bmo:ConfidenceAssessment` | `xsd:string` | No source comment. |
| `bmo:referencesImagery` | `bmo:SpectralAnomaly` | `bmo:ImageryReference` | Links an anomaly to the imagery it was found in, by reference. The only permitted relation to imagery: no tiling, no per-pixel triples. |
| `bmo:storageURI` | `bmo:ImageryReference` | `xsd:anyURI` | No source comment. |
| `bmo:tierRank` | `bmo:ConfidenceTier` | `xsd:integer` | Ordering within the enumeration. Ranks are not a probability scale and must not be arithmetic. |
| `bmo:triggeredAlert` | `bmo:Detection` | `bmo:Alert` | Detection to alert. At most one, and frequently none. |
| `bmo:triggeredCollection` | `bmo:SpectralAnomaly` | `bmo:SampleCollection` | Anomaly to the collection act it prompted. Exactly one. |
| `bmo:yieldedSpecimen` | `bmo:SampleCollection` | `bmo:Specimen` | No source comment. |
| `up:assertedBy` | `up:Assertion` | `prov:Agent` | The agent or process that produced this assertion. |
| `up:contradictedBy` | `up:Assertion` | `up:EvidenceItem` | Evidence bearing against this assertion, retained rather than discarded. An assertion with no recorded contradiction is not thereby uncontradicted; it may simply never have been challenged. |
| `up:crosswalkFrom` | `up:Crosswalk` | `up:ConceptualUnit` | No source comment. |
| `up:crosswalkTo` | `up:Crosswalk` | `rdfs:Resource` | The external term this crosswalk maps to. The range is deliberately open: the target is an identifier in a foreign vocabulary, and constraining it to a locally declared class would mean restating that vocabulary here, which is the opposite of what a crosswalk is for. |
| `up:discriminates` | `up:RequirementSpecification` | `up:ConceptualUnit` | The candidates a requirement is intended to separate. A requirement that discriminates nothing is a fixed protocol step, not an adaptive request. |
| `up:epistemicStatus` | `up:InformationArtifact` | `up:EpistemicStatus` | No source comment. |
| `up:fidelity` | `up:Crosswalk` | `up:MappingFidelity` | How well the mapping holds: exact, broader, narrower, partial, or none. |
| `up:generatedUnder` | `up:Assertion` | `up:RuleSetVersion` | The rule set or method version in force when the assertion was produced. Without it, a rule change makes every past assertion uninterpretable. |
| `up:hasConfidence` | `up:Assertion` | `up:ConfidenceAssessment` | No source comment. |
| `up:hasSupportDescription` | `obo:IAO_0000027` | `up:SupportDescription` | No source comment. |
| `up:recommendsNext` | `up:Assertion` | `up:RequirementSpecification` | The requirement whose satisfaction would most reduce remaining uncertainty. What makes a system adaptive rather than merely descriptive. |
| `up:supportedBy` | `up:Assertion` | `up:EvidenceItem` | Evidence bearing in favour of this assertion. |
