# Implementations

Known implementations of the Product Definition as Code specification.

| Implementation | Language | Spec version targeted | Conformance | Notes |
| --- | --- | --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | v0.1 (draft) | **Last verified pass:** 16 of 16 runnable cases and 8 of 8 pinned digests.<br>**Record:** 2026-08-23, spec [`2c95e77`](https://github.com/product-definition-as-code/spec/commit/2c95e77), published `@prodshape/cli` 0.13.0 installed from npm, `pdac-lint` 0.1.2 conformance runner.<br>This is a dated record of one run, not a live status. It says nothing about releases of the spec or the implementation made after that date. | Reference implementation; the spec was extracted from it; implements the citation contract |

## Conformance tooling

[`pdac-lint`](https://github.com/product-definition-as-code/pdac-lint) is listed here because implementers need it, not because it is an implementation. It is a separately versioned conformance runner: it runs the published conformance tests in this repository against an implementation command, and it verifies the digests those tests pin. It is neutral tooling hosted in this organization ([GOVERNANCE.md](GOVERNANCE.md)).

| Tool | Language | Scope |
| --- | --- | --- |
| [`pdac-lint`](https://www.npmjs.com/package/pdac-lint) | TypeScript | Runs the published conformance cases against an implementation command and verifies pinned digests |

What it is not: it is not independent validation of the specification, and it is not a second independent implementation of the reference profile. It executes the cases this repository publishes, so it can only find what those cases already assert. The gates in [MATURITY.md](MATURITY.md) are unaffected by its existence.

It does read the specification for itself where the tests depend on it, and that has mattered once: its digest implementation disagreed with the reference implementation's, which produced [RFC 0038](rfcs/0038-digest-bytes.md) and the `digest-bytes-not-text` case.

## Listing criteria

An implementation is listed when it: (1) is publicly available under an OSI-approved or source-available license, (2) states which spec version it targets, and (3) passes the published conformance tests for that version, run with [`pdac-lint`](https://www.npmjs.com/package/pdac-lint). The tests are published and runnable but not yet a complete normative set, so a listing records the versions used for the verified pass. To be added, open a pull request.
