# Small benchmark plan — proposed

Issue #129. Prepared 2026-11-27. Status: owner approval and independent review pending; no benchmark was executed. [Protocol](experimental-protocol.md) governs fairness, freeze and evidence. These illustrative domain decisions are not accepted product knowledge.

## Domains and task size

Use a small booking model and an authorization contrast. Proposed booking decisions: what consumes capacity, when cancellation is allowed, and which identity/role may change a reservation. Proposed lifecycle vocabulary: requested, reserved, cancelled, expired; owners must approve guards/effects, time units, error outcomes, identities and preservation properties before any scoring. Authorization includes an explicitly external issuer/role assumption.

Represent only the few artifacts/interactions needed to express these decisions in PDaC cohorts; equivalent facts and history exist in non-PDaC cohorts. Do not add fields or artifact kinds to v0.3.0. Formal representations remain external experimental material, with authority reviewed per property. No domain-to-code implementation or solver syntax is selected here.

## Proposed episode sequence

| Episode | Intent input / perturbation | Independent observations |
| --- | --- | --- |
| B0 | Initial owner-approved booking intent and positive/negative scenarios | Faithful interpretation, non-empty reachable witnesses, baseline obligations and assumptions |
| B1 | Change a business rule governing capacity or cancellation | Required intent change versus an agent's extra semantic choices; old evidence applicability |
| B2 | Change domain meaning/units | Propagation to interacting rules, invariants and contracts without silent conversion decisions |
| B3 | Change interacting expiry/cancellation transition behaviour | Preservation/frame effects and previously valid evidence that no longer covers intended transitions |
| B4 | Change an external identity-domain assumption; keep a direct cited target byte-identical | Formal transitive dependency versus structural one-hop accounting and direct citation freshness |
| B5 | Change an unrelated artifact only | Spurious semantic invalidation/reconstruction and unchanged relevant evidence |
| B6 | Editorial-only change to a cited artifact | Stale citation versus unchanged formal property; no automatic pin renewal |
| A0 | Authorization model with approved external issuer/role assumptions | Contrast-domain interpretation, consistency and adequacy without claiming implementation correctness |

At least three independent decisions interact across multiple artifacts and successive changes. Each cohort receives identical change requests; only PDaC cohorts process them as Product Changes. A fresh independent agent/session continues each episode from equivalent accepted history. Evaluators seed weakened/incomplete contracts and unintended agent semantic substitutions in designated variants, recording them as faults rather than silently accepting new owner intent.

## Seeds, faults and containment

Candidate economic pilot: two controlled seed schedules (17 and 29), four cohorts, seven booking episodes plus one authorization episode: **64 authoring sessions**. These seed values were chosen before running anything; they are identifiers, not evidence of reproducibility or a powered sample. Record provider limitations on random seeds and actual task/cohort ordering. Do not infer deterministic agent output.

Adequacy checks reuse these outputs, not another 64 authoring sessions. Independent evaluators prepare a compact held-out set covering contradiction/vacuity, weak/over-strong contracts, frame/effect omission, domain ambiguity, assumption changes and agent drift. The [adequacy report input](https://github.com/product-definition-as-code/spec/pull/145) provides candidate classes, not the held-out answers. Evaluators must approve fault eligibility and distinguish equivalent/invalid mutants; unknowns/timeouts remain visible.

Keep public calibration examples separate from held-out cases. Publish only access-controlled manifests/digests until the agreed release point; do not place secret cases in agent-readable PRs. A benchmark designer who has seen held-out answers cannot serve as a blind author for that evaluation. Human product intent judgments remain separate from machine or agent assessments.

## Approval and reproduction

Pending G1: exact intent text/IDs/artifact set, intended behaviours, change semantics, finite scopes, seed/order file, fault counts and eligibility, held-out custodian and release rules, selected tools and numeric caps. Owner review may reduce the plan before freeze. Do not silently drop categories or change decisions after outcomes are known.

Every future episode preserves its intent/model/dependency revisions, inputs/handoffs, commands, outputs and limits. No fixtures, new Product Artifacts or checked formulas are introduced by this plan. Results would generalize only to the declared benchmark/assumptions; larger/adopter evaluation needs later explicit approval.
