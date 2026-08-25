# RFC 0082: A Product Change accounts for its graph neighborhood

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-25
- **Revised:** 2026-08-25 (v3; v2 added impact polarity, per-cause acknowledgments, digest pinning and the apply gate; v3 closes the no-op modify bypass, fixes diagnostic attribution, splits PRODUCT002 from PRODUCT033, accounts for product-wide constraints and pins removals)

## Problem

Overlay validation ([Product Changes → Overlay validation](../spec/product-changes.md#overlay-validation)) proves the resulting model is structurally sound. It cannot say whether the artifacts that depend on a modified artifact were ever reconsidered. Modify `BR-REFUND-001` and the overlay validates green whether or not anyone looked at the use cases it governs; the graph still resolves, so nothing is reported. Today that impact analysis lives entirely in the author's judgment, and [Elaboration](../spec/product-changes.md#elaboration) only says implementations SHOULD surface referencing artifacts as assistance. Assistance leaves no record: nothing distinguishes "considered and unaffected" from "never looked".

This gap matters most for exactly the authoring mode PDaC anticipates. An LLM or human elaborating a large change can miss dependents, and nothing catches it. Neighboring SDD tooling has the same hole, delta well-formedness is checked while impact completeness is not.

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

Product Change operation edges never produce candidates.

A pair connected through two inverse edges, such as a use case carrying `governed-by` toward a rule that also carries `applies-to` toward the use case, produces one cause per edge, deliberately. The two edges are distinct authored assertions: one is the use case declaring what it builds on, the other is the rule declaring its scope. Coalescing them would require an equivalence relation over relationship fields that the vocabulary does not define, and a repository that finds the pair redundant fixes its model, not the validator. Tooling generates the entries either way; only the reasons are human.

### Impact causes

An implementation MUST compute the canonical relationship edges of both the baseline graph and the overlay graph. An **impact cause** is a tuple `(candidate, cause artifact, relationship field, disposition)` where the cause artifact is effectively changed, the candidate is a baseline artifact reachable from it across one edge under the polarity above, the candidate is **not itself effectively changed**, and the disposition is `existing` (the edge is in both graphs), `added` (overlay only) or `removed` (baseline only). Comparing both graphs is required: a proposed artifact that adds `applies-to: UC-Y` impacts `UC-Y` even though the baseline has no such edge, and a removal severs every edge its artifact held. One candidate can carry several causes through several changed artifacts and fields; each cause stands alone. Archived changes are inert and contribute nothing, as everywhere else.

The exclusion is by effective change, never by mention: an artifact named in `operations.modify` whose proposed content is byte-identical to baseline is not effectively changed and remains a candidate. Excluding by mention would let a change list a dependent in `operations.modify`, propose identical bytes and thereby remove it from the worklist while neither changing nor acknowledging it, which would defeat the ledger.

**Product-wide constraints.** A Constraint with absent `applies-to` applies to the entire product. When such a constraint is effectively changed, enumerating every artifact as a candidate would be exactly the blanket acknowledgment this RFC forbids; producing nothing would make the broadest change the least governed. Instead it produces exactly one **product-scope cause** `(product, constraint, applies-to, existing)`, acknowledged by a single entry as below. Whether one reason can honestly dispose of a product-wide review is the reviewer's judgment; the mechanism only refuses to let it happen silently.

### Acknowledgment

`change.md` frontmatter gains an OPTIONAL `unaffected` list. Each entry acknowledges one cause and pins what was reviewed:

```yaml
unaffected:
  - id: UC-REFUND-002                # the candidate
    cause: BR-REFUND-001             # the effectively changed artifact
    relationship: governed-by        # the relationship field
    digest: sha256:...               # baseline digest of the candidate as reviewed
    cause-digest: sha256:...         # digest of the cause content as reviewed
    reason: rule threshold changed, the flow does not encode the threshold
  - scope: product                   # acknowledges a product-scope cause; carries no id or digest
    cause: CON-DATA-RESIDENCY
    relationship: applies-to
    cause-digest: sha256:...
    reason: reviewed against every current product area, residency wording only tightened
```

`reason` MUST be non-blank. `digest` MUST equal the candidate's current baseline digest, so an acknowledgment written against a candidate that has since moved is invalid rather than silently stale. `cause-digest` MUST equal the digest of the cause content as reviewed: the proposed content for an addition or modification, the baseline content for a removal, so the archived ledger records which version of the cause's meaning the reviewer assessed in every case.

### Validation and gating

Evaluated when a Product Change is validated or applied, under the same conditions as `PRODUCT020`-`PRODUCT028`: never against the baseline alone, never against archived changes.

1. **`PRODUCT029` (warning), one per impact cause** that is not acknowledged by an `unaffected` entry matching its `(candidate, cause, relationship)` triple (`(scope, cause, relationship)` for a product-scope cause). Reported by change validation only.
2. **`PRODUCT033` (error), one per well-formed `unaffected` entry that fails semantically**: its triple matches no computed cause, its `id` does not name a baseline artifact, or its `digest` or `cause-digest` does not match the content defined above. Malformed entries never reach `PRODUCT033`: a missing or unknown field, a syntactically invalid ID or digest, both or neither of `id` and `scope`, or a blank `reason` violate the `product-change` schema and are reported as `PRODUCT002`, exactly one layer each.
3. **`PRODUCT034` (error), apply precondition** in the `PRODUCT027`/`PRODUCT028` pattern: apply, dry-run included, MUST refuse while any unacknowledged impact cause remains, evaluated before anything is written, working tree untouched, exit `1`, one per cause. At apply, `PRODUCT034` is emitted for each unacknowledged cause and `PRODUCT029` MUST NOT additionally be emitted for the same cause, in the spirit of the one-condition-one-diagnostic rule of [Citation Contract → Precedence](../spec/citation-contract.md#precedence).

Attribution uses the existing diagnostic vocabulary ([Validation → Diagnostic model](../spec/validation.md)) without new fields. For `PRODUCT029` and `PRODUCT034`: `change` = the Product Change, `artifact` = the candidate, the resolved Product Artifact the diagnostic is about, `target` = the cause, the operated-on ID, `field` = the relationship field; a product-scope cause omits `artifact`. The disposition travels in `message`. This deliberately does not reuse the source-edge orientation of `PRODUCT006`-`PRODUCT008`: an impact diagnostic is about the candidate whichever end of the edge authored it, and `artifact`/`target` are defined by subject roles, not by edge direction. For `PRODUCT033`: `change`, `field` = the entry's one-based list position, `target` = the entry's `id` or `cause` exactly as authored.

During elaboration the ledger is therefore a warning-level worklist; at apply it is a completed record or the apply does not happen. This is not a veto on content, unlike the deliberate visibility-only stance of [#48](https://github.com/product-definition-as-code/spec/issues/48) for consumer citations, where breaking consumers is often the purpose of a change. Intra-model coherence is the change's own job, the author fully controls both `operations` and `unaffected`, and the gate can always be satisfied by writing down the disposition it demands. `PRODUCT029` remains a warning and participates in `validation.warnings-as-errors` like every other warning; the kernel offers no per-code escalation, and the enforcement point is the apply gate, not severity configuration.

### What this is and is not

The validator cannot know whether a use case is truly unaffected by a rule change; no tool can. It enforces that someone claimed it, per cause, with a reason, against pinned content, in the reviewed record. The result is a record of disposition over the **modeled** relationships, not a proof of impact completeness: a dependency that was never authored as a relationship is invisible to this mechanism and stays the reviewer's job. Implementations SHOULD generate `unaffected` entries mechanically (ids, causes, digests) during elaboration and prompt only for reasons; the ledger is meant to be filled by tooling and reviewed by humans in the change review, not hand-typed.

### One hop, deliberately

Acknowledging a candidate is a claim about that candidate only. If reviewing it reveals it must change, adding it to the change makes it effectively changed, which removes it as a candidate and extends the neighborhood from it, and the ratchet recurses through the change itself. A transitive closure would flood large models with unreadable acknowledgment lists and turn the reason field into noise.

## Impact

- **On existing conformant repositories:** repositories with no active changes see nothing. An active change modifying a referenced artifact starts producing `PRODUCT029` warnings, and stops applying, until it accounts for its causes; archived changes are untouched.
- **On existing implementations:** ProductShape already compiles both graphs and surfaces referencing artifacts during elaboration; this adds the polarity table, the cause computation, the `unaffected` schema field and the apply precondition.
- **On the conformance tests:** at least these cases. (1) Modify `BR-X` with `UC-Y` carrying `governed-by: BR-X`, unacknowledged: one `PRODUCT029` with `artifact: UC-Y`, `target: BR-X`. (2) Modify `QR-X` carrying `applies-to: UC-Y`: one `PRODUCT029` with `artifact: UC-Y`, the polarity case a reverse-only walk misses. (3) The same changes with matching `unaffected` entries: clean. (4) A proposed artifact adding an `applies-to` edge to an untouched `UC-Y`: one cause with disposition `added`. (5) A removal producing causes at both polarities, acknowledged with the removed artifact's baseline `cause-digest`. (6) A byte-identical `operations.modify` listing of a dependent: the dependent remains a candidate and one `PRODUCT029` is reported, the bypass case. (7) A product-wide constraint change: one product-scope cause, silent only when a `scope: product` entry acknowledges it. (8) An entry whose triple matches no cause: `PRODUCT033`, exit `1`. (9) An entry whose `digest` no longer matches the candidate: `PRODUCT033`. (10) An entry with a blank `reason`: `PRODUCT002`, never `PRODUCT033`. (11) A declared modify whose proposed content is byte-identical to baseline and has no dependents: no causes. (12) Apply with one unacknowledged cause: `PRODUCT034`, exit `1`, working tree untouched, no `PRODUCT029` for that cause.

`PRODUCT030`-`PRODUCT032` are retired and never reused, so the codes here are `029`, `033` and `034`; the change band is fragmented by history, not by choice.

## Alternatives considered

**Status quo, elaboration assistance only.** The SHOULD in Elaboration surfaces a similar set but records nothing, so review cannot tell considered from missed. Rejected: the whole value is the recorded claim.

**The required `## Affected Product Areas` body section.** It already exists and stays: it is narrative intent. It is prose, not machine-checkable, carries no per-cause accounting and cannot gate anything. This RFC adds the checkable ledger beside it.

**Reverse edges only, as v1 proposed.** Rejected as incorrect: `applies-to` is authored on the rule pointing at what it constrains, so a changed quality requirement's constrained use cases are outbound targets and a reverse-only walk never sees them. Polarity per field is the fix, at the cost of one normative column.

**Excluding candidates named in `operations`, as v2 proposed.** Rejected as a bypass: a byte-identical `modify` listing would silently remove a dependent from the worklist. Exclusion is by effective change only.

**New diagnostic fields (`candidate`, `cause`, `disposition`).** Rejected: they would extend the diagnostic model, its JSON schema and the deterministic sort order for one code family. The existing vocabulary already carries the roles, `artifact` is the subject and `target` is the operated-on ID, both within their normative definitions.

**Coarse per-candidate acknowledgment (`{id, reason}`), as v1 proposed.** Rejected: one candidate impacted through three causes would be acknowledged once, and the reviewer cannot tell which causes were considered. Per-cause entries with digest pins cost more YAML and buy an audit trail that survives rebases; tooling generates everything but the reason.

**Coalescing inverse governance pairs into one cause.** Rejected for now: it needs an equivalence relation over relationship fields the vocabulary does not define, and the duplication only arises when a repository authored both inverse edges, which is a modeling choice. Revisit with evidence if real ledgers show boilerplate pairs dominating.

**Warning-only, no apply gate, as v1 proposed.** Rejected: a warning the default configuration ignores lets apply archive a change with unconsidered dependents, and the kernel deliberately offers no per-code escalation. The two-stage form (warning while elaborating, precondition at apply) matches the existing `PRODUCT027`/`PRODUCT028` pattern and keeps severities fixed per code.

**Transitive closure instead of one hop.** Rejected above: acknowledgment lists become co-extensive with the model, reasons degrade to boilerplate, and recursion through effective-change membership already covers the case where a candidate genuinely changes.

**Leave it to the citation layer (#48).** Citations bind consumers to the model; they do not exist between model artifacts, and inventing intra-model citations would duplicate the relationship graph the model already declares. The graph is the right instrument; #48 and this RFC together cover both directions.
