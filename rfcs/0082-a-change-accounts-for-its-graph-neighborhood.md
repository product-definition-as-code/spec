# RFC 0082: A Product Change accounts for its graph neighborhood

- **Status:** accepted
- **Accepted:** 2026-09-25 by Juan G. Carmona
- **Author(s):** juangcarmona
- **Created:** 2026-08-25
- **Revised:** 2026-08-28 (v6; v2 added impact polarity, per-cause acknowledgments, digest pinning and the apply gate; v3 closed the no-op modify bypass, fixed diagnostic attribution, split PRODUCT002 from PRODUCT033, accounted for product-wide constraints and pinned removals; v4 fixed PRODUCT033 precedence and attribution strings, modeled product scope as an implicit edge and staged the apply preconditions; v5 moves semantic acknowledgment validation after baseline drift; v6 extracts the impact polarity column into RFC 0093 targeting 0.2.0 and depends on it)
- **Release refinement:** 2026-09-25; consumes RFC 0116 vocabulary and fixes impact edge identity
- **Depends on:** accepted [RFC 0093](0093-impact-polarity.md), implemented in v0.2, and [RFC 0116](0116-domain-behaviour-and-verification-evidence.md), which precedes this RFC in v0.3.0
- **Proposed target:** PDaC specification 0.3.0, serialization `v1alpha2` established by RFC 0116
- **Followed by:** [RFC 0115](https://github.com/product-definition-as-code/spec/pull/115), a separate decision about downstream citation visibility.

## Review in brief

A change must account for the model artifacts it directly puts in question: actually change them, or record a reason why they remain unaffected, pinned to the reviewed content. The review decision is whether to require that accounting before apply.

- Preserve one-hop impact, using the relationship vocabulary accepted in RFC 0116. Acknowledging an unchanged neighbor does not propagate impact; actually changing it expands the next calculation.
- Compare baseline and overlay edges. Repeated occurrences of the same artifact/field/target edge produce one cause; distinct fields remain distinct causes. No separate transition-level ledger is introduced.
- Missing accounting warns during elaboration (PRODUCT029) and blocks apply/dry-run (PRODUCT034). Malformed or stale acknowledgments cannot satisfy the gate (PRODUCT002/033).
- Downstream citation staleness is a separate forecast under RFC 0115 and does not itself block apply. This is a record of review over modeled relationships, not proof of semantic completeness.

This RFC targets v0.3.0/v1alpha2. Its design is accepted; schemas, diagnostics and executable cases remain follow-up implementation work.

## Decision record

Accepted for v0.3.0 by the founding maintainer, Juan G. Carmona, on 2026-09-25: Product Changes must account for their directly affected model neighborhood before apply. Keep impact one hop, count repeated identical edges once, and require reasons pinned to reviewed content for unchanged candidates. This records review without claiming complete semantic impact; stale downstream citations remain non-blocking.

The maintainer explicitly authorized recording this rationale and merging RFC #82 after RFC #116. No substantive review feedback was outstanding at the decision. The published MATURITY and ADOPTERS records show neither an independent implementation/clean-room validator nor an adopter other than the reference implementation, so CONTRIBUTING's conditional minimum elapsed comment window is not yet a merge condition. Publication, the maintainer decision and rationale, and resolution of substantive feedback remain required and are recorded here.

Acceptance records the design, not its implementation or the v0.3.0 release. RFC #115 remains a separate decision.

## Problem

Overlay validation ([Product Changes → Overlay validation](../spec/product-changes.md#overlay-validation)) proves the resulting model is structurally sound. It cannot say whether the artifacts that depend on a modified artifact were ever reconsidered. Modify `BR-REFUND-001` and the overlay validates green whether or not anyone looked at the use cases it governs; the graph still resolves, so nothing is reported. Today that impact analysis lives entirely in the author's judgment, and [Elaboration](../spec/product-changes.md#elaboration) only says implementations SHOULD surface referencing artifacts as assistance. Assistance leaves no record: nothing distinguishes "considered and unaffected" from "never looked".

This gap matters most for exactly the authoring mode PDaC anticipates. An LLM or human elaborating a large change can miss dependents, and nothing catches it. The gap is architectural, not tool-specific: validating declared deltas does not establish that every impacted artifact was declared.

[RFC 0115](https://github.com/product-definition-as-code/spec/pull/115), following issue [#48](https://github.com/product-definition-as-code/spec/issues/48), closes the model-to-consumer half: apply surfaces the affected citation set. This RFC closes the model-to-model half. Both are needed; canonical model relationships are not consumer citations, and the citation index alone cannot account for dependent model artifacts.

## Proposal

Normative additions to [Product Changes](../spec/product-changes.md), the diagnostics in [Validation](../spec/validation.md) and the frontmatter field in the `product-change` schema and [Frontmatter reference](../spec/frontmatter-reference.md). The impact polarity this RFC reads from [Relationships](../spec/relationships.md) was established by RFC 0093 and is not redefined here. RFC 0116 extends that vocabulary before this accounting contract is implemented.

### Effectively changed artifacts

Within a Product Change, an artifact is effectively changed when it is named in `operations.remove`, or when it appears under `proposed/` and its proposed content differs from its baseline content (or has no baseline content, for an addition) under the normalization of [Validation → Digests](../spec/validation.md#digests). This follows the existing doctrine that impact derives from the effective change, never from declared operations alone ([Change impact](../spec/product-changes.md#change-impact)).

### Impact polarity

Impact polarity is not defined here. Canonical authoring direction is not impact direction. The per-field `Polarity` column was merged through RFC 0093 for v0.2. This RFC consumes the column as extended by RFC 0116, rather than preserving an obsolete copy of its target sets.

An implementation of this RFC reads `dependency`, `governance` and `none` from the [canonical vocabulary](../spec/relationships.md#canonical-vocabulary). A `dependency` field makes the source a candidate when the target effectively changes. A `governance` field makes each end a candidate when the other effectively changes. A `none` field never produces a candidate, which is why Product Change operation edges do not.

Under RFC 0116 a Business Rule's `applies-to` targets only Journey or Bounded Context; Use Case governance is authored once as `Use Case.governed-by`. A changed rule questions its citing Use Cases under dependency polarity; a Use Case-only change does not question that rule through this edge. Rule broad scope still has governance polarity. An absent or empty Business Rule scope does not create a product-scope cause.

### Edge identity and duplicate causes

For impact accounting only, an implementation MUST project the valid canonical relationships in each graph to a set keyed by `(source artifact ID, canonical relationship field, target artifact ID)`. Local array indexes, Transition IDs and derived reverse views MUST NOT enter that key. This does not change the per-authored-entry granularity of ordinary relationship validation.

Thus several Lifecycle transitions naming the same Business Rule through `transitions[].governed-by` contribute one edge. Removing one occurrence while another remains leaves the edge `existing`; moving it between transitions does too. Removing the final occurrence makes the edge `removed`. The containing Lifecycle is the source artifact and its whole-artifact digest is the acknowledgment pin. There are no local-record impact nodes or pins.

Distinct fields remain distinct causes. A Lifecycle whose `subject` and `uses-terms` both name one changed term requires one disposition for each field. Compare the two projected edge sets first, then derive causes; deduplicate identical cause tuples. The baseline and overlay occurrence of one edge yields `existing`, never an additional `added` and `removed` pair. This makes the acknowledgment triple below identify at most one computed cause. It does not collapse unrelated authored assertions by semantic guesswork.

### Impact causes

An implementation MUST compute the projected canonical edge sets of both the baseline graph and the overlay graph. An **impact cause** is a tuple `(candidate, cause artifact, relationship field, disposition)` where the cause artifact is effectively changed, the candidate is a baseline artifact reachable from it across one edge under the polarity of that edge's field, the candidate is **not itself effectively changed**, and the disposition is `existing` (the edge is in both graphs), `added` (overlay only) or `removed` (baseline only). Comparing both graphs is required: a proposed Quality Requirement that adds `applies-to: UC-Y` impacts `UC-Y` even though the baseline has no such edge, and a removal severs every edge its artifact held. One candidate can carry several causes through several changed artifacts and fields; each cause stands alone. Archived changes are inert and contribute nothing, as everywhere else. Local Lifecycle state/transition selectors and external Verification Evidence are not Product Graph edges.

The exclusion is by effective change, never by mention: an artifact named in `operations.modify` whose proposed content is byte-identical to baseline is not effectively changed and remains a candidate. Excluding by mention would let a change list a dependent in `operations.modify`, propose identical bytes and thereby remove it from the worklist while neither changing nor acknowledging it, which would defeat the ledger.

**Product-wide constraints.** A Constraint with absent `applies-to` applies to the entire product. Enumerating every artifact as a candidate would be exactly the blanket acknowledgment this RFC forbids; producing nothing would make the broadest change the least governed. Instead, a Constraint with absent `applies-to` holds one **implicit edge** `applies-to → product` in whichever graph it has that form, and the ordinary baseline/overlay comparison produces at most one **product-scope cause** `(product, constraint, applies-to, disposition)` when the constraint is effectively changed or the implicit edge differs between the graphs. The dispositions fall out rather than being decreed: a new global constraint yields `added`, a modified one `existing`, a removed one `removed`, and a constraint whose `applies-to` list is dropped in the proposal widens to product scope and yields `added` for the implicit edge alongside `removed` causes for its former explicit targets. A product-scope cause is acknowledged by a single entry as below. Whether one reason can honestly dispose of a product-wide review is the reviewer's judgment; the mechanism only refuses to let it happen silently.

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

Both entry shapes are closed objects in `schemas/v1alpha2/product-change.schema.json`. An artifact entry requires exactly `id`, `cause`, `relationship`, `digest`, `cause-digest` and `reason`. A product-scope entry requires exactly `scope: product`, a Constraint `cause`, `relationship: applies-to`, `cause-digest` and `reason`; it has neither `id` nor `digest`. Artifact IDs include LC. An artifact entry's relationship is a non-blank field string whose membership in a computed cause is checked semantically. A valid acknowledgment must match the triple and pass both applicable digest checks. Malformed or semantically invalid entries MUST NOT discharge causes. Repeated valid entries for the same triple are redundant and discharge it once; each invalid entry still receives its own diagnostic.

### Validation and gating

Evaluated when a Product Change is validated or applied, under the same conditions as `PRODUCT020`-`PRODUCT028`: never against the baseline alone, never against archived changes.

1. **`PRODUCT029` (warning), one per impact cause** that is not acknowledged by an `unaffected` entry matching its `(candidate, cause, relationship)` triple (`(scope, cause, relationship)` for a product-scope cause). Reported by change validation only.
2. **`PRODUCT033` (error), one per well-formed `unaffected` entry that fails semantically.** One entry can fail several checks at once; exactly one diagnostic is emitted, decided by the first condition that holds, in this order, mirroring the first-holds rule of [Citation Contract → Precedence](../spec/citation-contract.md#precedence):

   | Order | Condition                                                             | `target`                          |
   | ----- | --------------------------------------------------------------------- | ---------------------------------- |
   | 1     | `id` does not name a baseline artifact                                 | the entry's `id` as authored       |
   | 2     | the triple matches no computed cause                                   | the entry's `cause` as authored    |
   | 3     | `digest` does not match the candidate's baseline digest                | the entry's `id` as authored       |
   | 4     | `cause-digest` does not match the cause content defined above          | the entry's `cause` as authored    |

   Each later condition presupposes the earlier ones: digests are only comparable once the triple resolves to a cause. Product-scope entries carry no `id`, so conditions 1 and 3 do not apply to them. Malformed entries never reach `PRODUCT033`: a missing or unknown field, a syntactically invalid ID or digest, both or neither of `id` and `scope`, or a blank `reason` violate the `product-change` schema and are reported as `PRODUCT002`, exactly one layer each.
3. **`PRODUCT034` (error), apply precondition** in the `PRODUCT027`/`PRODUCT028` pattern: apply, dry-run included, MUST refuse while any unacknowledged impact cause remains, evaluated before anything is written, working tree untouched, exit `1`, one per cause. At apply, `PRODUCT034` is emitted for each unacknowledged cause and `PRODUCT029` MUST NOT additionally be emitted for the same cause, in the spirit of the one-condition-one-diagnostic rule of [Citation Contract → Precedence](../spec/citation-contract.md#precedence).

**Apply evaluation is staged**, so identical inputs refuse identically everywhere. After configuration succeeds, this RFC fixes where its diagnostics sit relative to the existing preconditions: (1) change status (`PRODUCT028`); (2) structural, schema and overlay validation of the change (`PRODUCT002`, overlay errors); (3) baseline drift (`PRODUCT027`); (4) semantic acknowledgment validation (`PRODUCT033`); (5) impact causes (`PRODUCT034`). Within a stage every computable instance is reported, ordered by the standard deterministic sort; a stage with any error stops evaluation, and later stages MUST NOT run or report. A normative warning escalated through `validation.warnings-as-errors` also stops the stage without changing its severity. The order is by presupposition: acknowledgment digests and cause matching compare against baseline content, so a drifted baseline would misreport a reviewed-and-correct ledger as invalid when the instruction is to rebase. PRODUCT033 and PRODUCT034 fire only when everything they depend on is sound.

At change validation, where apply's preconditions do not exist, implementations MUST report all computable independent PRODUCT002, overlay, PRODUCT033 and PRODUCT029 findings together as the elaboration worklist against the current baseline. Malformed entries receive only PRODUCT002 at the ledger-entry layer and cannot acknowledge a cause. Semantic checks MUST NOT guess through malformed or ambiguous artifact identities, relationship fields or operations: skip only the dependent computation while reporting independent findings. A schema-valid entry reaches PRODUCT033 only when the graph data needed to determine its cause is valid and unambiguous.

Attribution uses the existing diagnostic vocabulary ([Validation → Diagnostic model](../spec/validation.md)) without new fields. For `PRODUCT029` and `PRODUCT034`: `change` = the Product Change, `artifact` = the candidate, the resolved Product Artifact the diagnostic is about, `target` = the cause, the operated-on ID, `field` = the relationship field; a product-scope cause omits `artifact`. The disposition travels in `message`, a deliberate tradeoff: a machine consumer that needs it recomputes it from the two graphs rather than the diagnostic model growing a field for one code family. This attribution deliberately does not reuse the source-edge orientation of `PRODUCT006`-`PRODUCT008`: an impact diagnostic is about the candidate whichever end of the edge authored it, and `artifact`/`target` are defined by subject roles, not by edge direction. For `PRODUCT033`: `change`, `field` = the exact string `unaffected[<n>]` with the entry's one-based position (for example `unaffected[1]`), `target` per the precedence table above, so identical inputs produce identical JSON and identical sort order everywhere.

During elaboration the ledger is therefore a warning-level worklist; at apply it is a completed record or the apply does not happen. This is not a veto on content, unlike the deliberate visibility-only stance of [#48](https://github.com/product-definition-as-code/spec/issues/48) for consumer citations, where breaking consumers is often the purpose of a change. Intra-model coherence is the change's own job, the author fully controls both `operations` and `unaffected`, and the gate can always be satisfied by writing down the disposition it demands. `PRODUCT029` remains a warning and participates in `validation.warnings-as-errors` like every other warning; the kernel offers no per-code escalation, and the enforcement point is the apply gate, not severity configuration.

### What this is and is not

The validator cannot know whether a use case is truly unaffected by a rule change; no tool can. It enforces that someone claimed it, per cause, with a reason, against pinned content, in the reviewed record. The result is a record of disposition over the **modeled** relationships, not a proof of impact completeness: a dependency that was never authored as a relationship is invisible to this mechanism and stays the reviewer's job. Implementations SHOULD generate `unaffected` entries mechanically (ids, causes, digests) during elaboration and prompt only for reasons; the ledger is meant to be filled by tooling and reviewed by humans in the change review, not hand-typed.

### One hop, deliberately

Acknowledging a candidate is a claim about that candidate only. If reviewing it reveals it must change, adding it to the change makes it effectively changed, which removes it as a candidate and extends the neighborhood from it, and the ratchet recurses through the change itself. A transitive closure would flood large models with unreadable acknowledgment lists and turn the reason field into noise.

For example, a changed rule can question a Lifecycle through `transitions[].governed-by`. An unchanged Structured Behaviour related only through `covers-transition.lifecycle` is two hops from that rule, so it is not a candidate yet. If review changes the Lifecycle, the next calculation questions the Structured Behaviour; if the Lifecycle is acknowledged unchanged, propagation stops. A Structured Behaviour directly illustrating that rule is already a one-hop candidate through `illustrates`. This distinction preserves the narrow structural claim and does not make any claim about complete semantic impact.

### Composition with apply's citation forecast

RFC 0115 runs after the staged preconditions above and before any writes. It uses the prospective effective product diff, not this cause set. An unchanged neighbor acknowledged in `unaffected` does not thereby make its citations stale. Forecast citation statuses do not enter PRODUCT029/033/034 or the warning-escalation gate. A failed earlier stage does not require a forecast and MUST NOT be presented as a computed zero affected set. The ordinary action preflight, rollback, archiving and human-merge acceptance rules remain in force.

### Implementation checklist

| Files | Required changes |
| --- | --- |
| `spec/product-changes.md` | Define effective change, projected edge identity, one-hop causes, product scope, acknowledgment pins and staged apply once; retain baseline sentinel, action preflight, rollback, archive and human acceptance rules. |
| `schemas/v1alpha2/product-change.schema.json`, `spec/frontmatter-reference.md`, `templates/product-change.md` | Add the closed artifact/product-scope unaffected union and examples. Use the new ID union including LC. Keep schema errors as PRODUCT002 JSON Pointers and semantic errors as PRODUCT033. |
| `spec/validation.md` | Allocate PRODUCT029/033/034 with the exact units, attribution and precedence above; preserve retired PRODUCT030–032. |
| `spec/conformance.md`, `conformance/README.md`, `conformance/cases/` | Add accounting requirements and validation/apply cases, explicitly distinguishing executable coverage from review criteria and unsupported cases. |
| `.github/workflows/conformance.yml` and the separate `pdac-conformance` runner | Pin a runner supporting selected-change apply/dry-run, Git-history setup, diagnostics/exit and before/after tree assertions before claiming the apply cases execute. Keep existing flat validation cases supported. |

The original fifteen cases below remain required. Add these focused families alongside them:

- `impact-{br-to-uc,uc-not-to-br,br-to-broad-scope,br-absent-scope}`: RFC 0116's changed target set and asymmetric dependency; only an absent Constraint scope creates an implicit product edge, never an absent BR scope or an empty authored Constraint list.
- `impact-{lc-subject,lc-uses-terms,lc-governed-by,lc-initiated-by,lc-realized-by,sb-covers-lc,fr-derived-lc,qr-scope-lc,constraint-scope-lc}`: every new field's direction, candidate, cause and attribution.
- `impact-{repeated-transition-edge,distinct-fields,baseline-overlay-single-cause,duplicate-ledger}`: one cause for repeated occurrences, two for distinct fields, valid repeated acknowledgments count once and invalid entries remain errors.
- `impact-{one-hop-acknowledged,ratchet-effective-change,no-op-dependent,scope-widened,scope-narrowed,empty-constraint-scope}`: bounded impact, no-op bypass prevention and implicit versus explicit scope.
- `impact-ledger-{candidate-drift,cause-drift,removed-cause-drift,both-or-neither-id-scope,unknown-property,malformed-digest,invalid-entry-not-acknowledged}`: closed shape, content pins and exactly one layer per entry failure.
- `apply-impact-{status-first,structure-before-drift,ledger-before-causes,dry-run,warning-escalation}` and a combined valid-ledger/stale-citation case: staged failure, untouched tree, no PRODUCT029 alongside PRODUCT034, and no citation forecast veto.

Canonical edge projection and transitions moving between local records require implementation checks; portable diagnostics assert observable cause counts, fields and ledger behavior rather than implementation-defined disposition messages. The existing runner cannot express apply/history/tree outcomes, so unsupported cases must remain explicitly uncovered until its extension executes them. That extension is a follow-up implementation dependency, not a prerequisite for accepting this design.

## Impact

- **On existing conformant repositories:** repositories with no active changes see nothing. An active change modifying a referenced artifact starts producing `PRODUCT029` warnings, and stops applying, until it accounts for its causes; archived changes are untouched.
- **On existing implementations:** implementations must consume the RFC 0116 graph vocabulary, compare projected edge sets, compute causes, validate the `unaffected` ledger and enforce the staged apply precondition. Existing polarity support alone does not implement this RFC.
- **On the conformance tests:** at least these cases. (1) Modify `BR-X` with `UC-Y` carrying `governed-by: BR-X`, unacknowledged: one `PRODUCT029` with `artifact: UC-Y`, `target: BR-X`. (2) Modify `QR-X` carrying `applies-to: UC-Y`: one `PRODUCT029` with `artifact: UC-Y`, the polarity case a reverse-only walk misses. (3) The same changes with matching `unaffected` entries: clean. (4) A proposed artifact adding an `applies-to` edge to an untouched `UC-Y`: one cause with disposition `added`. (5) A removal producing causes at both polarities, acknowledged with the removed artifact's baseline `cause-digest`. (6) A byte-identical `operations.modify` listing of a dependent: the dependent remains a candidate and one `PRODUCT029` is reported, the bypass case. (7) A modified product-wide constraint: one product-scope cause with disposition `existing`, silent only when a `scope: product` entry acknowledges it; an added global constraint yields `added` and a removed one `removed`. (8) An entry whose triple matches no cause: `PRODUCT033` with `target` = the `cause` as authored, `field: unaffected[<n>]`, exit `1`. (9) An entry failing several checks at once, unknown `id` and mismatched `cause-digest`: exactly one `PRODUCT033` with `target` = the `id`, the precedence case. (10) An entry with a blank `reason`: `PRODUCT002`, never `PRODUCT033`. (11) A declared modify whose proposed content is byte-identical to baseline and has no dependents: no causes. (12) Apply with one unacknowledged cause: `PRODUCT034`, exit `1`, working tree untouched, no `PRODUCT029` for that cause. (13) Apply with both an invalid ledger entry and an unacknowledged cause: `PRODUCT033` only, stage 4 stops evaluation and `PRODUCT034` is not reported, the staging case. (14) Apply with baseline drift and an unacknowledged cause: `PRODUCT027` only. (15) Apply with baseline drift and an acknowledgment whose digests no longer match: `PRODUCT027` only, never `PRODUCT033`, since the mismatch may be nothing but the drift.

`PRODUCT030`-`PRODUCT032` are retired and never reused, so the codes here are `029`, `033` and `034`; the change band is fragmented by history, not by choice.

## Alternatives considered

**Status quo, elaboration assistance only.** The SHOULD in Elaboration surfaces a similar set but records nothing, so review cannot tell considered from missed. Rejected: the whole value is the recorded claim.

**The required `## Affected Product Areas` body section.** It already exists and stays: it is narrative intent. It is prose, not machine-checkable, carries no per-cause accounting and cannot gate anything. This RFC adds the checkable ledger beside it.

**Reverse edges only, as v1 proposed.** Rejected as incorrect: a changed Quality Requirement's constrained Use Cases are outbound `applies-to` targets and a reverse-only walk misses them. RFC 0093 supplied polarity per field in v0.2; this RFC consumes it.

**Keeping the polarity column inside this RFC.** Rejected and extracted into the now-accepted RFC 0093. The vocabulary belongs in Relationships and remains independently useful for elaboration; this RFC owns accounting and gating, not a duplicate polarity definition.

**Excluding candidates named in `operations`, as v2 proposed.** Rejected as a bypass: a byte-identical `modify` listing would silently remove a dependent from the worklist. Exclusion is by effective change only.

**New diagnostic fields (`candidate`, `cause`, `disposition`).** Rejected: they would extend the diagnostic model, its JSON schema and the deterministic sort order for one code family. The existing vocabulary already carries the roles, `artifact` is the subject and `target` is the operated-on ID, both within their normative definitions.

**Coarse per-candidate acknowledgment (`{id, reason}`), as v1 proposed.** Rejected: one candidate impacted through three causes would be acknowledged once, and the reviewer cannot tell which causes were considered. Per-cause entries with digest pins cost more YAML and buy an audit trail that survives rebases; tooling generates everything but the reason.

**Preserving both BR/UC authoring directions.** Superseded by RFC 0116: the duplicate Use Case target is removed from BR scope and migrated to UC governance. This RFC therefore cannot justify inverse-pair boilerplate as a modeling choice. It keeps distinct valid canonical fields separate and deduplicates repeated occurrences of the same edge as specified above.

**Warning-only, no apply gate, as v1 proposed.** Rejected: a warning the default configuration ignores lets apply archive a change with unconsidered dependents, and the kernel deliberately offers no per-code escalation. The two-stage form (warning while elaborating, precondition at apply) matches the existing `PRODUCT027`/`PRODUCT028` pattern and keeps severities fixed per code.

**Transitive closure instead of one hop.** Rejected above: acknowledgment lists become co-extensive with the model, reasons degrade to boilerplate, and recursion through effective-change membership already covers the case where a candidate genuinely changes.

**Leave it to the citation layer (#115).** Citation status does not account for canonical model relationships. This RFC records disposition within the graph; RFC 0115 forecasts consequences for consumers. Neither substitutes for the other.
