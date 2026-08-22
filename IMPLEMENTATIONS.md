# Implementations

Known implementations of the Product Definition as Code specification.

| Implementation | Language | Spec version targeted | Conformance | Notes |
| --- | --- | --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | v0.1 (draft) | Passes the full published conformance suite (16 of 16 runnable cases and 8 of 8 pinned digests; verified 2026-08-20 against spec [`6464948`](https://github.com/product-definition-as-code/spec/commit/6464948), using packed `@prodshape/cli` 0.12.0 and the `pdac-lint` 0.1.2 conformance runner) | Reference implementation; the spec was extracted from it; implements the citation contract |

## Listing criteria

An implementation is listed when it: (1) is publicly available under an OSI-approved or source-available license, (2) states which spec version it targets, and (3) passes the published conformance tests for that version, run with [`pdac-lint`](https://www.npmjs.com/package/pdac-lint). The tests are published and runnable but not yet a complete normative set, so a listing records the versions used for the verified pass. To be added, open a pull request.
