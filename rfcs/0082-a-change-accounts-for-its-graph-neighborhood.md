# RFC 0082: A Product Change accounts for its graph neighborhood

- **Status:** draft
- **Author(s):** juangcarmona
- **Created:** 2026-08-25

## Problem

Overlay validation ([Product Changes → Overlay validation](../spec/product-changes.md#overlay-validation)) proves the resulting model is structurally sound. It cannot say whether the artifacts that depend on a modified artifact were ever reconsidered. Modify `BR-REFUND-001` and the overlay validates green whether or not anyone looked at the use cases it governs; the graph still resolves, so nothing is reported. Today that impact analysis lives entirely in the author's judgment, and [Elaboration](../spec/product-changes.md#elaboration) only says implementations SHOULD surface referencing artifacts as assistance. Assistance leaves no record: nothing distinguishes "considered and unaffected" from "never looked".

This gap matters most for exactly the authoring mode PDaC anticipates. An LLM elaborating a change over a large model works with wide context and reliably misses dependents; a human under deadline does too. Neighboring SDD tooling has the same hole, delta well-formedness is checked while impact completeness is not, so closing it is a differentiator, not parity work.

Issue [#48](https://github.com/product-definition-as-code/spec/issues/48) closes the model-to-consumer half: apply surfaces the affected citation set. This RFC closes the model-to-model half at change validation time. Both are needed; citations do not cover intra-model relationships, and the citation index cannot see that a journey references a use case whose governing rule just changed meaning.

## Proposal

Normative additions to [Product Changes](../spec/product-changes.md), with the diagnostic in [Validation](../spec/validation.md) and the frontmatter field in the `product-change` schema and [Frontmatter reference](../spec/frontmatter-reference.md).

**Effectively changed artifacts.** Within a Product Change, an artifact is effectively changed when it is named in `operations.remove`, or when its proposed future-state content differs from its baseline content under the normalization of [Validation → Digests](../spec/validation.md#digests). This follows the existing doctrine that impact derives from the effective change, never from declared operations alone ([Change impact](../spec/product-changes.md#change-impact)).

**Impact neighborhood.** The change's impact neighborhood is the set of baseline artifacts holding at least one canonical relationship ([Relationships → Canonical vocabulary](../spec/relationships.md#canonical-vocabulary)) targeting an effectively changed artifact, excluding artifacts that are themselves named in the change's `operations` and excluding archived changes. One hop, computed over the derived reverse relationships the graph compiler already produces; it is never authored.

**Acknowledgment.** `change.md` frontmatter gains an OPTIONAL `unaffected` list. Each entry MUST carry the `id` of a baseline artifact and a non-empty free-text `reason`:

```yaml
unaffected:
  - id: UC-REFUND-002
    reason: rule threshold changed, the use case flow does not encode the threshold
```

**Validation.** When a Product Change is validated or applied (dry-run included), under the same conditions as `PRODUCT020`-`PRODUCT028`, never against the baseline alone and never against archived changes:

1. Every artifact in the impact neighborhood that is neither named in the change's `operations` nor listed in `unaffected` MUST be reported as **`PRODUCT029`** (warning): artifact depends on an effectively changed artifact and the change neither includes it nor acknowledges it. Emission is one diagnostic per such artifact, attributed to `change.md`, with the artifact as target.
2. Every `unaffected` entry whose `id` does not name an artifact in the impact neighborhood MUST be reported as **`PRODUCT033`** (error). This keeps the ledger honest: blanket acknowledgment lists, entries left behind when a change shrinks, and entries for artifacts the change now modifies are all invalid, deterministically.

**What this is and is not.** The validator cannot know whether a use case is truly unaffected by a rule change; no tool can. It enforces that someone claimed it, with a reason, in the reviewed record. Acknowledgment is a checklist made of the graph, not a semantic proof, and it is visibility with a ratchet, not a veto: `PRODUCT029` is a warning, and escalation stays a repository decision through the existing warning-escalation mechanism, consistent with the kernel's stance that risk policy belongs to the repository, not the kernel.

**One hop, deliberately.** Acknowledging a neighbor is a claim about that neighbor only. If reviewing it reveals it must change, adding it to `operations.modify` extends the neighborhood from it, and the ratchet recurses through the change itself. A transitive closure would flood large models with unreadable acknowledgment lists and turn the reason field into noise.

## Impact

- **On existing conformant repositories:** repositories with no active changes see nothing. An active change modifying a referenced artifact starts producing `PRODUCT029` warnings until it accounts for its neighborhood; archived changes are inert and untouched.
- **On existing implementations:** ProductShape already compiles the derived reverse relationships and already surfaces them during elaboration; this moves that set from assistance into the diagnostic stream and adds the `unaffected` field to the `product-change` schema.
- **On the conformance tests:** four cases. (1) Modify `BR-X` where `UC-Y` carries `governed-by: BR-X`, no acknowledgment: one `PRODUCT029` targeting `UC-Y`. (2) Same change with an `unaffected` entry for `UC-Y`: clean. (3) An `unaffected` entry naming an artifact outside the neighborhood: `PRODUCT033`, exit 1. (4) A declared modify whose proposed content is byte-identical to baseline: empty neighborhood, no `PRODUCT029`.

## Alternatives considered

**Status quo, elaboration assistance only.** The SHOULD in Elaboration surfaces the same set but records nothing, so review cannot tell considered from missed. Rejected: the whole value is the recorded claim.

**The required `## Affected Product Areas` body section.** It already exists and stays: it is narrative intent. It is prose, not machine-checkable, carries no per-artifact accounting and cannot gate anything. This RFC adds the checkable ledger beside it.

**Transitive closure instead of one hop.** Rejected above: acknowledgment lists become co-extensive with the model, reasons degrade to boilerplate, and recursion through `operations` membership already covers the case where a neighbor genuinely changes.

**Error instead of warning for `PRODUCT029`.** Rejected as the default: severity policy belongs to the repository ([Validation](../spec/validation.md)), and mechanical wide changes would fight a hard gate. Repositories that want the hard gate escalate the code.

**Leave it to the citation layer (#48).** Citations bind consumers to the model; they do not exist between model artifacts, and inventing intra-model citations would duplicate the relationship graph the model already declares. The graph is the right instrument; #48 and this RFC together cover both directions.
