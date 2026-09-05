# Implementations

Known implementations of the Product Definition as Code specification.

| Implementation | Language | Spec version targeted | Conformance | Notes |
| --- | --- | --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | 0.2.0, v1alpha1 serialization | **Last verified pass:** 44 of 44 cases and 12 of 12 pinned digests.<br>**Record:** 2026-09-05, spec [`7feb4ec`](https://github.com/product-definition-as-code/spec/commit/7feb4ec), published `@prodshape/cli` 0.19.0 installed from npm (shasum `6f504607e6ed415c7a24cb8125b7ec230a64f4bc`), `pdac-conformance` 1.0.1 runner, claimed as specification 0.2.0 on serialization v1alpha1.<br>This is a dated record of one run, not a live status. It says nothing about releases of the spec or the implementation made after that date. | Reference implementation; the spec was extracted from it; implements the citation contract and Structured Behaviour, and hosts the product workflow in OpenSpec and Spec Kit |

## Conformance tooling

[`pdac-conformance`](https://github.com/product-definition-as-code/pdac-conformance) is listed here because implementers need it, not because it is an implementation. It is a separately versioned conformance runner: it runs the published conformance tests in this repository against an implementation command, and it verifies the digests those tests pin. It is neutral tooling hosted in this organization ([GOVERNANCE.md](GOVERNANCE.md)).

| Tool | Language | Scope |
| --- | --- | --- |
| [`pdac-conformance`](https://www.npmjs.com/package/pdac-conformance) | TypeScript | Runs the published conformance cases against an implementation command and verifies pinned digests |

What it is not: it is not independent validation of the specification, and it is not a second independent implementation of the reference profile. A conformance result is bounded by the cases this repository publishes; uncovered rules remain uncovered. The gates in [MATURITY.md](MATURITY.md) are unaffected by its existence.

It does read the specification for itself where the tests depend on it, and that has mattered once: its digest implementation disagreed with the reference implementation's, which produced [RFC 0038](rfcs/0038-digest-bytes.md) and the `digest-bytes-not-text` case.

## Listing criteria

An implementation is listed when it: (1) is publicly available under an OSI-approved or source-available license, (2) states which method/spec and serialization versions it targets, and (3) passes the published conformance tests for that version pair, run with [`pdac-conformance`](https://www.npmjs.com/package/pdac-conformance). The tests are published and runnable but not yet a complete normative set, so a listing records the versions used for the verified pass. To be added, open a pull request.
