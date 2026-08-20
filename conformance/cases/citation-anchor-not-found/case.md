# Case: citation-anchor-not-found

**Verifies:** the citation's target resolves and its digest is current, but the named `anchor` does not exist within the target; the status is `unresolved` and the diagnostic is `PRODUCT063`, not `PRODUCT060`.

**Spec references:**

- [Citation Contract → Anchors](../../../spec/citation-contract.md#anchors) - in v0.1 an anchor is a verification scenario's stable `id`.
- [Citation Contract → Precedence](../../../spec/citation-contract.md#precedence) - rows 1 and 2 do not hold (well-formed digest, resolving target), so row 3 decides: the `anchor` does not resolve within the target.
- [Validation](../../../spec/validation.md) - error `PRODUCT063`: the target resolves but the named anchor does not exist within it.

## Fixture

`repo/` contains the citation-current model unchanged: an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`) whose only verification scenario carries the stable `id` `S1`, established by an archived `CHG-INITIAL`.

The consumer document (`repo/specs/feature-x.md`) carries a sidecar ledger (`repo/specs/feature-x.citations.yml`), a flat list of citation records, citing `FR-VALIDATE-001` at `sha256:cb93b565e529ada665c37f3c962ed50221bb6cade065fa332a4aa9ee148a4970` - the digest of the artifact's current content - with anchor `S2`, a scenario the artifact does not declare. The pin matching the canonical text is half the construction: with the digest current, the anchor is the only condition that fails, and the digest check verifies the pin stays faithful, so an edit to the requirement cannot quietly turn this case into a two-defect fixture.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT063` as an error against `FR-VALIDATE-001` in `specs/feature-x.citations.yml`. `PRODUCT060` is the wrong answer here - the target `id` resolves, and the anchor clause has its own code precisely so that a citation naming a real artifact and a missing scenario is distinguishable from one naming nothing at all.
