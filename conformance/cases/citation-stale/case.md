# Case: citation-stale

**Verifies:** the canonical Functional Requirement was amended after the citation was recorded; the target resolves, no projection is embedded, and the target's recomputed digest differs from the recorded one; the status is `stale` and the diagnostic is the `PRODUCT061` warning.

**Spec references:**

- [Citation Contract → Statuses](../../../spec/citation-contract.md#statuses) - `stale`: the target resolves but canonical content changed since the citation was recorded.
- [Citation Contract → Precedence](../../../spec/citation-contract.md#precedence) - rows 1-4 do not hold (well-formed digest, resolving target and anchor, no embedded projection), so row 5 decides.
- [Validation](../../../spec/validation.md) - `PRODUCT061` is a warning, escalated only by a repository's `warnings-as-errors`, never unilaterally.

## Fixture

`repo/` carries the citation-current model - an Actor (`ACT-VALIDATOR`), a Journey (`JRN-VALIDATE`), a Use Case (`UC-VALIDATE-001`) and a Functional Requirement (`FR-VALIDATE-001`) with one verification scenario carrying the stable `id` `S1`, established by an archived `CHG-INITIAL` - one accepted Product Change later: an archived `CHG-TIGHTEN-VALIDATION` modified `FR-VALIDATE-001`, whose requirement now reads `report each of them as a validation error with a deterministic code` and hashes to `sha256:3045dbb42aef886f5a6103c50ab98f54b6432ee47f120f2418af597a1bd5ee37`.

The consumer document (`repo/specs/feature-x.md`) still carries the citation recorded before that change: its sidecar ledger (`repo/specs/feature-x.citations.yml`) uses the canonical top-level `citations` mapping and pins `FR-VALIDATE-001` at `sha256:cb93b565e529ada665c37f3c962ed50221bb6cade065fa332a4aa9ee148a4970` with anchor `S1`. That is the digest of the requirement's earlier revision - byte-identical to `citation-current`'s `fr-validate-001.md` - so a runner verifying pinned digests can reproduce it from that sibling fixture rather than trusting it. The pin MUST stay different from the artifact's current content: this case exists because it differs, and the digest check asserts the difference.

The anchor `S1` still resolves in the amended artifact. Staleness is judged exclusively by the digest of the cited target, so the surviving anchor neither masks nor softens it.

## Expected

`expected.json` asserts exactly one diagnostic: `PRODUCT061` as a warning at entry 1 of `specs/feature-x.citations.yml`, the file carrying the citation record, with `target` `FR-VALIDATE-001`. The severity is the other half of the assertion: an implementation that escalates staleness to an error on its own authority fails this case, because risk policy belongs to the repository, not the kernel.
