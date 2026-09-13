# ADR-0004: Reference-data boundary

Status: Accepted  
Date: 2026-09-13

## Context

A deployment can add many crops, pathogens, sensors, methods, authorities, and jurisdictions. Encoding each as a new core class would turn the ontology into inventory.

## Decision

Specific deployment selections normally enter through external identifiers and project reference/instance data. The core grows only for semantic distinctions needed by competency questions.

## Consequences

The four current host/pathogen pilots are `PilotPathosystem` instances. State rules are `ReportingRule` records. New deployment inventory does not automatically expand the class hierarchy.

## Alternatives rejected

A large local crop/pathogen/sensor subclass tree.

## Revisit if

A deployment entity type requires semantics that cannot be represented with existing classes/properties and external identifiers.
