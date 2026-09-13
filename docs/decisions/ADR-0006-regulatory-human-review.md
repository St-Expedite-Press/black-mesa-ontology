# ADR-0006: Regulatory human review

Status: Accepted  
Date: 2026-09-13

## Context

Scientific evidence does not by itself determine jurisdiction-specific notification, quarantine, or movement consequences. Draft legal/regulatory interpretations can be incomplete or wrong.

## Decision

Draft `ReportingRule` records are non-operative and must require human review. Phase 1 external regulatory notification remains human-gated. Scientific detections remain separate from regulatory determinations.

## Consequences

Automation can support evaluation and provenance without treating draft policy records as autonomous authority.

## Alternatives rejected

Automatically notifying external authorities from a sensor indication, diagnostic result, or unreviewed draft rule.

## Revisit if

A future deployment has formally reviewed, versioned rules and governance authorizing a narrower automated action. Such a change requires explicit architecture and safety review.
