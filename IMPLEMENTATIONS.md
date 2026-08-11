# Implementations

Known implementations of the Product Definition as Code specification.

| Implementation | Language | Spec version targeted | Conformance | Notes |
| --- | --- | --- | --- | --- |
| [ProductShape](https://github.com/juangcarmona/productshape) | TypeScript | v0.1 (draft) | Passes the published conformance tests (6 of 6 cases, verified 2026-08-11 with `pdac-lint` 0.1.1 and `@prodshape/cli` 0.8.1) | Reference implementation; the spec was extracted from it; implements the citation contract |

## Listing criteria

An implementation is listed when it: (1) is publicly available under an OSI-approved or source-available license, (2) states which spec version it targets, and (3) passes the published conformance tests for that version, run with [`pdac-lint`](https://www.npmjs.com/package/pdac-lint). The tests are published and runnable but not yet a complete normative set, so a listing records the versions used for the verified pass. To be added, open a pull request.
