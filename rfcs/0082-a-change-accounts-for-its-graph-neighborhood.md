# RFC 0082: A Product Change accounts for its graph neighborhood

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-25
- **Revised:** 2026-08-25 (v2 after adversarial review: impact polarity, per-cause acknowledgments, digest pinning, apply gate)

## Problem

Overlay validation ([Product Changes → Overlay validation](../spec/product-changes.md#overlay-validation)) proves the resulting model is structurally sound. It cannot say whether the artifacts that depend on a modified artifact were ever reconsidered. Modify `BR-REFUND-001` and the overlay validates green whether or not anyone looked at the use cases it governs; the graph still resolves, so nothing is reported. Today that impact analysis lives entirely in the author's judgment, and [Elaboration](../spec/product-changes.md#elaboration) only says implementations SHOULD surface referencing artifacts as assistance. Assistance leaves no record: nothing distinguishes "considered and unaffected" from "never looked".

This gap matters most for exactly the authoring mode PDaC anticipates. An LLM elaborating a change over a large model works with wide context and reliably misses dependents; a human under deadline does too. Neighboring SDD tooling has the same hole, delta well-formedness is checked while impact completeness is not.

Issue [#48](https://github.com/product-definition-as-code/spec/issues/48) closes the model-to-consumer half: apply surfaces the affected citation set. This RFC closes the model-to-model half. Both are needed; citations do not exist between model artifacts, and the citation index cannot see that a journey references a use case whose governing rule just changed meaning.

## Proposal

Normative additions to [Product Changes](../spec/product-changes.md), with the impact polarity in [Relationships](../spec/relationships.md), the diagnostics in [Validation](../spec/validation.md) and the frontmatter field in the `product-change` schema and [Frontmatter reference](../spec/frontmatter-reference.md).

### Effectively changed artifacts

Within a Product Change, an artifact is effectively changed when it is named in `operations.remove`, or when it appears under `proposed/` and its proposed content differs from its baseline content (or has no baseline content, for an addition) under the normalization of [Validation → Digests](../spec/validation.md#digests). This follows the existing doctrine that impact derives from the effective change, never from declared operations alone ([Change impact](../spec/product-changes.md#change-impact)).

### Impact polarity

Canonical authoring direction is not impact direction. On a dependency field the author cites what the artifact builds on, so a change to the target puts the source in question. On a governance field the edge couples both ends: the governed artifact must be reconsidered when its rule changes, and the rule's continued applicability must be reconsidered when the governed artifact changes. The [canonical vocabulary](../spec/relationships.md#canonical-vocabulary) gains a normative impact-polarity column:

| Source, field                       | Polarity   | Candidates when the other end effectively changes                     |
| ----------------------------------- | ---------- | ---------------------------------------------------------------------- |
| Journey `primary-actor`             | dependency | the journey, when the actor changes                                     |
| Journey `steps[].use-case`          | dependency | the journey, when the use case changes                                  |
| Use Case `primary-actor`            | dependency | the use case, when the actor changes                                    |
| Use Case `supporting-actors`        | dependency | the use case, when the actor changes                                    |
| Use Case `bounded-context`          | dependency | the use case, when the bounded context changes                          |
| Use Case `governed-by`              | dependency | the use case, when the business rule changes                            |
| Use Case `uses-terms`               | dependency | the use case, when the domain term changes                              |
| Domain Term `defined-in`            | dependency | the domain term, when the bounded context changes                       |
| Functional Requirement `derived-from` | dependency | the requirement, when the use case, rule or constraint changes        |
| Business Rule `applies-to`          | governance | both ends, when the other changes                                       |
| Quality Requirement `applies-to`    | governance | both ends, when the other changes                                       |
| Constraint `applies-to`             | governance | both ends, when the other changes                                       |

A Constraint with absent `applies-to` applies to the entire product; a change to it produces no per-artifact candidates. Its review unit is the change itself, and enumerating every artifact would be exactly the blanket acknowledgment this RFC forbids. Product Change operation edges never produce candidates.

### Impact causes

An implementation MUST compute the canonical relationship edges of both the baseline graph and the overlay graph. An **impact cause** is a tuple `(candidate, cause artifact, relationship field, disposition)` where the cause artifact is effectively changed, the candidate is a baseline artifact reachable from it across one edge under the polarity above, the candidate is not itself named in the change's `operations`, and the disposition is `existing` (the edge is in both graphs), `added` (overlay only) or `removed` (baseline only). Comparing both graphs is required: a proposed artifact that adds `applies-to: UC-Y` impacts `UC-Y` even though the baseline has no such edge, and a removal severs every edge its artifact held. One candidate can carry several causes through several changed artifacts and fields; each cause stands alone. Archived changes are inert and contribute nothing, as everywhere else.

### Acknowledgment

`change.md` frontmatter gains an OPTIONAL `unaffected` list. Each entry acknowledges one cause triple and pins what was reviewed:

```yaml
unaffected:
  - id: UC-REFUND-002                # the candidate
    cause: BR-REFUND-001             # the effectively changed artifact
    relationship: governed-by        # the relationship field
    digest: sha256:...               # baseline digest of the candidate as reviewed
    cause-digest: sha256:...         # digest of the cause's proposed content; forbidden for removals
    reason: rule threshold changed, the flow does not encode the threshold
```

`reason` MUST be non-blank. `digest` MUST equal the candidate's current baseline digest, so an acknowledgment written against a candidate that has since moved is invalid rather than silently stale. `cause-digest` MUST equal the digest of the cause artifact's proposed content and is forbidden when the cause is a removal, so editing the proposal after the review invalidates the acknowledgment that reviewed the older proposal.

### Validation and gating

Evaluated when a Product Change is validated or applied, under the same conditions as `PRODUCT020`-`PRODUCT028`: never against the baseline alone, never against archived changes.

1. **`PRODUCT029` (warning), one per impact cause** that is neither covered by the change's `operations` nor acknowledged by an `unaffected` entry matching its `(candidate, cause, relationship)` triple. Attribution: `change`, `target` = candidate, `artifact` = cause, `field` = relationship field.
2. **`PRODUCT033` (error), one per invalid `unaffected` entry**: its triple matches no computed cause, its `id` does not name a baseline artifact, its `digest` or `cause-digest` does not match, `cause-digest` is present for a removal or absent otherwise, or `reason` is blank. Attribution: `change`, `field` = the entry's list position, `target` = the entry's `id`.
3. **`PRODUCT034` (error), apply precondition** in the `PRODUCT027`/`PRODUCT028` pattern: apply MUST refuse while any unacknowledged impact cause remains, evaluated before anything is written, working tree untouched, exit `1`, dry-run included, same per-cause granularity as `PRODUCT029`.

During elaboration the ledger is therefore a warning-level worklist; at apply it is a completed record or the apply does not happen. This is not a veto on content, unlike the deliberate visibility-only stance of [#48](https://github.com/product-definition-as-code/spec/issues/48) for consumer citations, where breaking consumers is often the purpose of a change. Intra-model coherence is the change's own job, the author fully controls both `operations` and `unaffected`, and the gate can always be satisfied by writing down the disposition it demands. `PRODUCT029` remains a warning and participates in `validation.warnings-as-errors` like every other warning; the kernel offers no per-code escalation, and the enforcement point is the apply gate, not severity configuration.

### What this is and is not

The validator cannot know whether a use case is truly unaffected by a rule change; no tool can. It enforces that someone claimed it, per cause, with a reason, against pinned content, in the reviewed record. The result is a record of disposition over the **modeled** relationships, not a proof of impact completeness: a dependency that was never authored as a relationship is invisible to this mechanism and stays the reviewer's job. Implementations SHOULD generate `unaffected` entries mechanically (ids, causes, digests) during elaboration and prompt only for reasons; the ledger is meant to be filled by tooling and reviewed by humans in the change review, not hand-typed.

### One hop, deliberately

Acknowledging a candidate is a claim about that candidate only. If reviewing it reveals it must change, adding it to `operations` extends the neighborhood from it, and the ratchet recurses through the change itself. A transitive closure would flood large models with unreadable acknowledgment lists and turn the reason field into noise.

## Impact

- **On existing conformant repositories:** repositories with no active changes see nothing. An active change modifying a referenced artifact starts producing `PRODUCT029` warnings, and stops applying, until it accounts for its causes; archived changes are untouched.
- **On existing implementations:** ProductShape already compiles both graphs and surfaces referencing artifacts during elaboration; this adds the polarity table, the cause computation, the `unaffected` schema field and the apply precondition.
- **On the conformance tests:** at least these cases. (1) Modify `BR-X` with `UC-Y` carrying `governed-by: BR-X`, unacknowledged: one `PRODUCT029` targeting `UC-Y`. (2) Modify `QR-X` carrying `applies-to: UC-Y`: one `PRODUCT029` targeting `UC-Y`, the polarity case a reverse-only walk misses. (3) The same changes with matching `unaffected` entries: clean. (4) A proposed artifact adding an `applies-to` edge to an untouched `UC-Y`: one cause with disposition `added`. (5) A removal producing causes at both polarities. (6) An `unaffected` entry whose triple matches no cause: `PRODUCT033`, exit `1`. (7) An entry whose `digest` no longer matches the candidate: `PRODUCT033`. (8) A declared modify whose proposed content is byte-identical to baseline: no causes. (9) A product-wide constraint change: no per-artifact causes. (10) Apply with one unacknowledged cause: `PRODUCT034`, exit `1`, working tree untouched. Blank `reason` and malformed entries are schema violations under the existing `PRODUCT002` band.

`PRODUCT030`-`PRODUCT032` are retired and never reused, so the codes here are `029`, `033` and `034`; the change band is fragmented by history, not by choice.

## Alternatives considered

**Status quo, elaboration assistance only.** The SHOULD in Elaboration surfaces a similar set but records nothing, so review cannot tell considered from missed. Rejected: the whole value is the recorded claim.

**The required `## Affected Product Areas` body section.** It already exists and stays: it is narrative intent. It is prose, not machine-checkable, carries no per-cause accounting and cannot gate anything. This RFC adds the checkable ledger beside it.

**Reverse edges only, as v1 of this RFC proposed.** Rejected as incorrect: `applies-to` is authored on the rule pointing at what it constrains, so a changed quality requirement's constrained use cases are outbound targets and a reverse-only walk never sees them. Polarity per field is the fix, at the cost of one normative column.

**Coarse per-candidate acknowledgment (`{id, reason}`), as v1 proposed.** Rejected: one candidate impacted through three causes would be acknowledged once, and the reviewer cannot tell which causes were considered. Per-cause entries with digest pins cost more YAML and buy an audit trail that survives rebases; tooling generates everything but the reason.

**Warning-only, no apply gate, as v1 proposed.** Rejected: a warning the default configuration ignores lets apply archive a change with unconsidered dependents, and the kernel deliberately offers no per-code escalation. The two-stage form (warning while elaborating, precondition at apply) matches the existing `PRODUCT027`/`PRODUCT028` pattern and keeps severities fixed per code.

**Transitive closure instead of one hop.** Rejected above: acknowledgment lists become co-extensive with the model, reasons degrade to boilerplate, and recursion through `operations` membership already covers the case where a candidate genuinely changes.

**Leave it to the citation layer (#48).** Citations bind consumers to the model; they do not exist between model artifacts, and inventing intra-model citations would duplicate the relationship graph the model already declares. The graph is the right instrument; #48 and this RFC together cover both directions.
