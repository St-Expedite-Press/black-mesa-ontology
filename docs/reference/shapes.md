<!-- GENERATED FILE - do not hand-edit. -->
<!-- Rebuild with tools/schema_docs.py; see docs/maintainers/generated-artifacts.md. -->

# SHACL shape index

Generated from `shapes.ttl`. These are implemented graph-validity checks; they are not a claim of ecological truth or scientific sufficiency.

| Shape | Target | Constraint messages |
|---|---|---|
| `bmo:AssayShape` | `bmo:Assay` | An assay takes exactly one specimen as input.<br>An assay produces exactly one result. A re-run is a different assay. |
| `bmo:ConfidenceAssessmentShape` | `bmo:ConfidenceAssessment` | A confidence assessment names exactly one tier.<br>Calibrated probability must be a single value in [0,1], present only where a probabilistic model produced it. Its absence is meaningful and must not be imputed.<br>Assay applicability must be recorded. An assay used outside its validation has no sensitivity figure that applies to the situation, and omitting this axis hides that. |
| `bmo:ConfidenceTierShape` | `bmo:ConfidenceTier` | Every tier must declare whether it presupposes visible symptoms. This is what makes the gap in the adopted enumeration machine-readable rather than a matter of prose. |
| `bmo:DetectionShape` | `bmo:Detection` | A detection must concern exactly one zone. Asserting at field or farm level overstates what a point sample supports.<br>A detection must derive from at least one assay result. A detection with no result behind it is an opinion.<br>A detection must carry a custody chain. A detection that cannot be resolved back to the flight, collection and assay that produced it is not evidence, and provenance cannot be retrofitted.<br>A detection must record the rule set version in force when it was produced. Without it, a later rule change makes every past detection uninterpretable.<br>A detection triggers at most one alert. Raising an alert is a separate decision from determining presence. |
| `bmo:ImageryReferenceShape` | `bmo:ImageryReference` | An imagery reference must carry exactly one storage URI.<br>An imagery reference must carry a checksum, so it can be shown to resolve to the bytes that were analysed. |
| `bmo:NoTiledImageryShape` | `bmo:ImageryReference` | GRAPH BOUNDARY VIOLATION: imagery must be referenced by URI and checksum, never tiled into the graph. Per-tile, per-pixel, and per-band statements are outside this conceptual schema boundary. |
| `bmo:ObservationRequirementShape` | `bmo:ObservationRequirement` | A requirement must state what it discriminates. A request with no diagnostic purpose is a fixed protocol step, not an adaptive one. |
| `bmo:ReportingCrosswalkShape` | `bmo:ReportingCrosswalk` | A crosswalk must name the internal term it maps from.<br>A crosswalk must state its fidelity: exact, broader, narrower, partial, or none. A mapping with unstated fidelity silently claims exactness it does not have. |
| `bmo:SpectralAnomalyShape` | `bmo:SpectralAnomaly` | An anomaly triggers at most one collection.<br>An anomaly must reference the imagery it was found in, so the finding can be re-examined against the bytes that produced it. |
| `bmo:UpperAnchorShape` | `owl:Class` | UNANCHORED CLASS: every domain class must reach BFO via the shared upper module (upper/upper-core.ttl). Declare what kind of thing it is - an information artifact, a process, a material entity, a site, a quality, or a role. |
