# Implementations

Known implementations of the Product Definition as Code specification.

| Implementation | Language | Spec version targeted | Conformance | Notes |
| --- | --- | --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | v0.1 (draft) | Passes the published conformance tests (7 of 7 cases and 5 of 5 pinned digests; verified 2026-08-17 by [this pinned run](https://github.com/juangcarmona/productshape/actions/runs/32011531635) using ProductShape [`02576bc`](https://github.com/juangcarmona/productshape/commit/02576bc65b9bdc5ebfa6b75f2ebd4b77057b4ad3), packed `@prodshape/cli` 0.9.0, spec [`89b43b7`](https://github.com/product-definition-as-code/spec/commit/89b43b78a6547c9dea709b6d261212c2fe4f3c4b), and `pdac-lint` 0.1.2) | Reference implementation; the spec was extracted from it; implements the citation contract |

## Listing criteria

An implementation is listed when it: (1) is publicly available under an OSI-approved or source-available license, (2) states which spec version it targets, and (3) passes the published conformance tests for that version, run with [`pdac-lint`](https://www.npmjs.com/package/pdac-lint). The tests are published and runnable but not yet a complete normative set, so a listing records the versions used for the verified pass. To be added, open a pull request.
