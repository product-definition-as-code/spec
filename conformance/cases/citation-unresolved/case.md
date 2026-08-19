# Case: citation-unresolved

**Verifies:** a consumer document cites a target `id` that does not resolve in the model; the status is `unresolved` and the diagnostic is `PRODUCT060`.

**Spec references:**

- [Citation Contract → Statuses](../../../spec/citation-contract.md#statuses) - `unresolved`: the target `id` or `anchor` does not resolve.
- [Citation Contract → Precedence](../../../spec/citation-contract.md#precedence) - row 1 does not hold (the recorded digest is well-formed), so row 2 decides: the target `id` does not resolve.
- [Validation](../../../spec/validation.md) - error `PRODUCT060`.

## Fixture

`repo/` contains the citation-current model unchanged: an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`), established by an archived `CHG-INITIAL`.

The consumer document (`repo/specs/feature-x.md`) carries a sidecar ledger (`repo/specs/feature-x.citations.yml`), a flat list of citation records, citing `FR-VALIDATE-002` - an ID no artifact in the model declares. The recorded digest is deliberately well-formed - it is `sha256:cb93b565e529ada665c37f3c962ed50221bb6cade065fa332a4aa9ee148a4970`, the digest of `FR-VALIDATE-001`'s canonical text, reproducible from the fixture - so resolution, and not digest validity, is the one condition that fails: an implementation that reports `PRODUCT042` here is checking the precedence rows in the wrong order. The record carries no anchor for the same reason: with no anchor there is nothing for row 3 to trip on, and the failing clause is exactly one.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT060` as an error against `FR-VALIDATE-002` in `specs/feature-x.citations.yml`. A citation names what it meant to cite, so the diagnostic carries the unresolved ID even though no artifact answers to it - there is no digest comparison and no staleness to report against a target that does not exist.
