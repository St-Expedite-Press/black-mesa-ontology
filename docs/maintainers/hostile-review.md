---
title: Hostile review
subtitle: Independent review findings and dispositions
style: mesa
---

## Review scope

An independent read-only review examined the rebuilt Black Mesa documentation,
local schema, SHACL shapes, tests, and publication tooling. It did not review
internal source records as public evidence and did not make changes.

## Findings and disposition

| Perspective | Finding | Disposition |
|---|---|---|
| Maintainer | Generated-reference freshness and the prior publisher README used obsolete paths. | Regenerated `docs/reference/`; publisher now uses the project README as its one durable source. |
| Ontologist | BFO anchors and structural SHACL checks exist, but there is no complete axiomatization, durable identifier design, or authored NPDN/CAP mapping. | Documented as current boundary and unresolved work. |
| Domain/scientific reviewer | No empirical sensing, assay, biology, or regulatory evidence is committed. Pre-symptomatic indication is a project hypothesis. | Examples and methodology explicitly label the absence of empirical validation. |
| Security/assurance reviewer | No access control, integrity verification at retrieval, privacy treatment, threat model, endpoint, or operational custody mechanism is implemented. | Documentation states that URI/checksum references do not prove authenticity, access, or authorization. |
| First-time user | The new index and README provide an accurate path; the old flat-assembly README would have led to dead links. | Fixed by assembling the project README instead of a stale template. |

## Release blockers retained

No reuse license or adequate third-party notice review is committed. Publication
therefore requires a separate legal or maintainer decision. No empirical,
operational, security, integration, or scientific-validation claim is ready for
release. These are capability and authorization limits, not failures of the
structural schema checks.
