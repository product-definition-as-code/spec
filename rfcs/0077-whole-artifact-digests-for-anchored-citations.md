# RFC 0077: Anchored citations pin the whole artifact

- **Status:** accepted
- **Author(s):** juangcarmona
- **Created:** 2026-08-24
- **Accepted:** 2026-08-24
- **Issue:** <https://github.com/product-definition-as-code/spec/issues/28>

## Problem

A citation records an artifact `id`, a `digest` and an optional scenario `anchor`. The specification defines content digests only for whole artifact files, but calls `digest` the digest of the cited canonical text. For an anchored citation, one implementation can therefore hash the whole artifact while another hashes only the addressed verification scenario. Both readings fit part of the current text and disagree whenever another scenario in the same artifact changes.

The scenario-only reading needs a new canonical byte representation below artifact granularity: which YAML bytes belong to one array entry, how mapping keys and whitespace are serialized, and how equivalent YAML spellings compare. No such representation exists. Inventing it would create a second digest algorithm and make citation status depend on a serialization the artifact itself does not canonically carry.

Both current code paths already use whole-artifact digests. `pdac-lint` verifies every pin against the artifact file, and ProductShape records and verifies the artifact digest whether or not an anchor is present.

## Proposal

The `digest` in every citation, anchored or unanchored, MUST be the content digest of the entire target artifact under [Validation → Digests](../spec/validation.md#digests).

An anchor identifies the location within that artifact on which the consumer relies. It narrows expressed dependency scope; it does not narrow digest scope. A conforming verifier MUST first resolve the target and anchor, then compare the recorded digest with the recomputed whole-artifact digest. Any byte change to that artifact after mandatory line-ending normalization makes the citation `stale`, including a change to another verification scenario or to prose outside the anchored scenario. A change to another artifact does not.

This is deliberate review sensitivity. The anchor tells the reviewer what the consumer relied on, while whole-artifact staleness says the surrounding requirement changed and the dependency must be reconsidered. The kernel does not attempt to prove that an edit elsewhere in the artifact is semantically unrelated.

An embedded projection carrying an anchor MUST embed the whole target artifact if it relies on the citation digest for `PRODUCT062` integrity checking. Embedding only an anchored scenario would require the sub-artifact canonicalization this RFC rejects and is therefore not a conforming embedded projection. A sidecar or bodyless payload can express anchored scope without embedding the artifact.

## Conformance

Add an anchored-citation case in which:

1. `FR-X#S1` resolves and the recorded whole-artifact digest matches, so the citation is `current`;
2. `S2` or artifact prose changes without changing `S1`, so the same citation is `stale` with `PRODUCT061`;
3. an unrelated artifact changes, so the citation remains `current`; and
4. an anchored embedded projection containing only the scenario is rejected as `PRODUCT062` rather than treated as a scenario-digest citation.

The existing digest algorithm and citation precedence do not change.

## Impact

- **On existing conformant repositories:** anchored citations already produced by known implementations carry whole-artifact digests and need no migration.
- **On existing implementations:** ProductShape and `pdac-lint` already follow this decision. A scenario-digest implementation must change to hash the target artifact file.
- **On conformance tests:** `scenario-id-addressing` can now pin the whole artifact. The former `partial-scope-without-loss` expectation is replaced by an explicit whole-artifact review-sensitivity case; partial dependency scope remains expressible, not independently digestible.
- **On generated projections:** a projection may display only the anchored scenario for navigation, but that display is not an embedded block whose bytes are verified against the citation digest.

## Alternatives considered

**Hash only the anchored scenario.** Rejected. It requires canonical bytes for a YAML array entry that the specification does not define, creates a second digest algorithm, and differs from current implementations.

**Store both artifact and scenario digests.** Rejected. It expands the citation record and still requires scenario canonicalization without evidence that two hashes improve review decisions.

**Keep the artifact digest but suppress staleness when the anchor appears unchanged.** Rejected. A digest cannot reveal which bytes changed, and reconstructing the old artifact would make current-tree verification depend on unavailable history.

## Decision record

Accepted 2026-08-24 by the founding maintainer as a determination under the founder-led stabilization exception. The decision selects the only digest algorithm already defined by the specification, matches both current implementations, and makes the conservative review boundary explicit without inventing scenario canonicalization. No substantive feedback remained unresolved.

The normative citation chapter and anchored conformance cases land in a follow-up change.
