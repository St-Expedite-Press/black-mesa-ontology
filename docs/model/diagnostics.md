# Diagnostics

A diagnostic procedure is an event. A diagnostic result is information produced by that event.

## Procedure and result

`DiagnosticProcedure` is method-agnostic. `Assay` is a subtype retained for compatibility. Each procedure is constrained to use one specimen/aliquot and produce one result datum; reruns or tests on another specimen should be separate procedure events.

`DiagnosticResult` records the procedure-level outcome. Current statuses include positive, negative, inconclusive, and below detection limit.

These statuses are not automatically the final `DiagnosticDisposition`.

## Method applicability

`DiagnosticProcedureProfile` is where method-validity information belongs. The schema supports information such as validated pathogen, host, specimen matrix, sensitivity, specificity, limit of detection, validation source, and method version.

This distinguishes:

> The procedure returned negative.

from:

> A method validated for this pathogen, host, and specimen matrix returned negative.

They do not carry the same evidentiary weight.

## Negative evidence

A negative result does not automatically establish biological absence over a field or region. Interpretation depends on method applicability, limit of detection, specimen condition, spatial support, sampling design, custody/provenance, and other evidence.

A `NotDetected` disposition is therefore a diagnostic conclusion within the scope of the evidence—not a declaration that a pathogen is globally absent.
