# Mission and scope

Black Mesa provides a shared meaning layer for agricultural biosecurity evidence.

The core problem is not storing a Boolean named `detected`. The system must preserve how a conclusion was reached: what was observed, what was anomalous, what causal hypotheses remained plausible, what physical material was collected, how that material moved, which diagnostic procedure generated a result, what scientific assertion was warranted, and which jurisdictional rule was later evaluated.

## What the core is

The ontology is a semantic contract connecting surveillance, physical evidence, diagnostics, provenance, and regulated-action evaluation.

It supports questions such as: What evidence generated this assertion? Was the evidence sensor-stage or diagnostic-stage? Which physical specimen was tested? Can custody events be reconstructed? Was the method applicable? What spatial area does the assertion warrant? Which model or rule version generated it? Did a scientific or regulatory determination create the record?

## What it is not

The core is not a computer-vision model, flight controller, sensor hardware taxonomy, laboratory information-management system, raw imagery database, exhaustive crop/pathogen taxonomy, autonomous legal decision maker, or substitute for plant-pathology and regulatory review.

## Scope discipline

The core represents semantic distinctions. Deployment inventories normally belong in reference data.

A new crop/pathogen pilot should usually instantiate `PilotPathosystem` with external identifiers. A new sensor should normally use SOSA/SSN-aligned instance data. A new state rule should be a versioned `ReportingRule` record.

## Phase 1

```text
survey → observation → anomaly → sensor indication → hypotheses
→ targeted sampling → specimen + custody → diagnostic procedure
→ diagnostic result → scientific assertion → jurisdictional rule evaluation
→ reviewed reporting / alerting
```

Environmental context, spread inference, fully reviewed state/pest rules, production sensor/model profiles, and validated diagnostic-method profiles remain separate deployment work where not already instantiated.
