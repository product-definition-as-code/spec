# RFC 0000: Acceptance criteria live in `verification[]`; the body does not restate them

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-06

## Problem

A requirement carries its acceptance criteria twice, and the specification does not say which copy is authoritative.

A Functional Requirement declares `verification` (required, non-empty, each entry optionally carrying a stable `id`) and is also required to contain the body section `## Acceptance Scenarios` ([Artifacts → Functional Requirement](../spec/artifacts.md#functional-requirement-functional-requirement-fr-)). A Quality Requirement has the same shape with the sharper naming: the frontmatter field `verification` beside the required body section `## Verification` ([Artifacts → Quality Requirement](../spec/artifacts.md#quality-requirement-quality-requirement-qr-)). `## Verification` is the only required body section in the chapter with no clause explaining what it holds, while its sibling `## Measurement` has one.

Every Functional Requirement in the conformance corpus writes both copies, keyed by the same scenario ids, and the two copies are not the same string. In [`citation-current`](../conformance/cases/citation-current/repo/docs/product/model/requirements/functional/fr-validate-001.md) the frontmatter reads `code PRODUCT006.` and the body reads ``code `PRODUCT006`.``; [`greenfield-first-increment`](../conformance/cases/greenfield-first-increment/repo/docs/product/model/requirements/functional/fr-greenfield-001.md) diverges the same way on `CHG-INITIAL` and `current`. Human-equivalent, machine-different, and nothing detects it, because no rule relates the two surfaces. Re-statement inside the kernel is the defect the kernel exists to make impossible.

The duplication is not inert, because content digests are computed over the whole artifact ([Validation → Digests](../spec/validation.md#digests)). The restated copy sits inside the digested bytes, so reformatting it alone changes the artifact digest and reports every citation to that requirement as `stale` with no criterion having changed. That contradicts the guarantee that "unrelated commits, unrelated artifact edits and generated-file churn MUST NOT make a citation stale" ([Citation Contract → Statuses](../spec/citation-contract.md#statuses)).

## Proposal

`verification[]` is the canonical carrier of a requirement's acceptance criteria. The criteria are structured, schema-validated, individually addressable through `verification[].id`, and already the only thing a citation anchor can resolve against. The body prose is a copy with none of those properties.

1. The required body sections of a Functional Requirement are `## Requirement` and `## Rationale`. `## Acceptance Scenarios` is removed from the required set.
2. The required body sections of a Quality Requirement are `## Requirement` and `## Measurement`. `## Verification` is removed from the required set. The `## Measurement` obligation is unchanged: it MUST state how conformance is measured.
3. A requirement's acceptance criteria are carried by `verification[]`. A body section that reproduces them is a projection, not a second source: an artifact MAY carry one, and when it does it MUST follow the embedding rules of the [Citation Contract](../spec/citation-contract.md#embedding), so that a hand-edited projection is detectable as `PRODUCT062` rather than silently divergent.
4. No change to `verification[]` itself: presence, cardinality, `scenario`, the optional `id` and its uniqueness within the artifact stay exactly as the [Frontmatter reference](../spec/frontmatter-reference.md) defines them.

Additional sections MAY still follow the required ones, per the common contract, so nothing forbids prose about verification. What ends is the obligation to write the criteria a second time in a form no tool can check.

## Impact

- **On existing conformant repositories:** none. Removing a section from the required set cannot invalidate an artifact that has it, because additional sections are already permitted. An existing `## Acceptance Scenarios` or `## Verification` becomes an additional section. Repositories that want the prose gone may delete it; those that keep it as a projection bring it under the embedding rules.
- **On existing implementations:** drop `PRODUCT009` enforcement of `## Acceptance Scenarios` on `functional-requirement` and of `## Verification` on `quality-requirement`. No diagnostic is added, retired or renumbered.
- **On the conformance corpus:** the four Functional Requirement fixtures (`citation-current`, `citation-tampered-and-stale`, `change-open-questions`, `greenfield-first-increment`) drop the duplicated section, which also removes the string divergence they currently ship. `citation-tampered-and-stale` pins a digest of text that is not in the fixture, so its expectation is unaffected. A Quality Requirement fixture should be added; none exists today, which is why the `## Verification` collision went unexercised. The planned `scenario-id-addressing` and `partial-scope-without-loss` cases are unaffected.

## Out of scope

Digest granularity under an anchor. For an anchored citation the specification does not say what `digest` covers: if the whole artifact, then a citation anchored to `S1` goes `stale` when `S2` is edited and partial scope is expressible but not independently verifiable; if the anchored scenario's own text, then `validation.md` defines no digest below artifact granularity and fixes no normalization for a scenario-sized string. That question is separable from this one, it changes what `stale` means rather than what an author writes, and it wants its own determination alongside the first `scenario-id-addressing` fixture.

## Alternatives considered

- **Keep both surfaces and declare frontmatter authoritative.** Settles which copy wins and nothing else. The second copy still has to be authored, still drifts, and still sits inside the digest, so the false `stale` reports remain.
- **Make the body section canonical and derive the frontmatter.** Loses schema validation and per-criterion identity. Anchors resolve against `verification[].id`, so the addressable surface would have to be regenerated from prose, and the citation contract would depend on parsing Markdown list items.
- **Require the body section to be generated from `verification[]`.** Achieves consistency, but mandates a generated file where a repository may reasonably want none, and adds a regeneration obligation to every requirement. This RFC permits it as a projection instead of requiring it.
- **Add an acceptance-criterion artifact kind.** Rejected. The criteria already have stable ids and are already addressable, so a tenth kind adds identity that exists, gives criteria a lifecycle they cannot independently have, and opens a third place for the same sentence to live. Durable knowledge that is genuinely reusable across requirements is already a Business Rule, and [Artifacts → Business Rule](../spec/artifacts.md#business-rule-business-rule-br-) explicitly names acceptance criteria as a place such knowledge MUST NOT be hidden.
