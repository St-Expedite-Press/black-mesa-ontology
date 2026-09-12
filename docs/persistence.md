# Persistent identifiers

Black Mesa uses W3ID-style persistent identifiers so ontology terms do not depend on the current GitHub repository location.

## Canonical identifiers

- ontology IRI: `https://w3id.org/black-mesa/bmo`
- term namespace: `https://w3id.org/black-mesa/bmo/`
- v0.4.0 version IRI: `https://w3id.org/black-mesa/bmo/releases/0.4.0`
- upper ontology IRI: `https://w3id.org/black-mesa/upper`
- upper term namespace: `https://w3id.org/black-mesa/upper/`

Black Mesa-specific records under `reference/` and `rules/` also use the `https://w3id.org/black-mesa/` base.

## External identifiers

Black Mesa does not mint substitute identifiers for crops, pathogens, standard units, or other well-governed external entities when an adequate authority exists. Initial host and pathogen profiles use OBO-form NCBITaxon IRIs.

## W3ID registration requirement

Declaring these IRIs in RDF does not by itself create the redirect. The `w3id.org` redirect must be registered in the public W3ID registry before the namespace is considered operationally resolvable.

A suitable redirect configuration should route:

~~~text
https://w3id.org/black-mesa/bmo/...
https://w3id.org/black-mesa/upper/...
https://w3id.org/black-mesa/reference/...
https://w3id.org/black-mesa/rules/...
~~~

to the stable published Black Mesa ontology resources.

Ontology validation resolves the upper import locally and therefore does not depend on network availability, but production Linked Data clients should be able to dereference the canonical IRIs.
