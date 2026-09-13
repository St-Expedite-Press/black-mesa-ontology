# ADR-0005: Persistent identifiers

Status: Accepted  
Date: 2026-09-13

## Context

Ontology terms must remain stable if repository or hosting locations change.

## Decision

Black Mesa uses the `https://w3id.org/black-mesa/` identifier base, with separate ontology, term, version, reference, rule, authority, and example paths.

## Consequences

Repository location is no longer the conceptual identity of a term. Public W3ID redirect registration/resolution remains a separate deployment responsibility and must be verified rather than assumed.

## Alternatives rejected

Temporary placeholder namespaces and repository-URL term identity.

## Revisit if

The persistent identifier authority changes; migration must preserve redirects and historical identity.
