# Experimental protocol — G1 candidate

Issue: [#129](https://github.com/product-definition-as-code/spec/issues/129); gate: [#130](https://github.com/product-definition-as-code/spec/issues/130). Prepared 2026-11-27. Status: **proposal, approval and independent review pending; not pre-registered evaluation**. Authority: [approved research proposal](../../v0.4.0-formal-product-definition.md).

## Inputs, aim and scope

The [provisional synthesis](https://github.com/product-definition-as-code/spec/blob/3da4c1b4dad6e0905ad9aff285708a22856bd243/docs/research/v0.4.0/reports/07-baseline-synthesis.md) and [ledger](https://github.com/product-definition-as-code/spec/blob/3da4c1b4dad6e0905ad9aff285708a22856bd243/docs/research/v0.4.0/claim-evidence-ledger.md) pin six unmerged report inputs. These are documentary findings, not accepted experimental results. Reconcile independent review before freezing. Primary foundations and access limits are linked there; in particular, [PDD's intent/proof/trust workflow](https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/), [SPOTs](https://risemsr.github.io/blog/2026-04-16-spotting-specs/) and [SACM's representation/validity distinction](https://www.omg.org/spec/SACM/2.3/PDF) inform mechanisms without proving PDaC's contribution.

H0 asks whether structured, versioned and governed product knowledge improves effectiveness, reliability and maintenance across changing intent, net of governance cost. H1/H2/H3 address fidelity, consistency and adequacy; H5 addresses continuity. Phase 2 examines agentic **product-model development**, not executed software. H4 implementation correspondence and any claim about proof-driven software implementation remain untested until the separately approved phase-3 bridge. Benchmark success cannot establish general correctness.

## Four cohorts; one matched task set

| Cohort | PDaC | Formal verification | Common task |
| --- | --- | --- | --- |
| 1 | No | No | Interpret/revise intent and assess scenarios using ordinary documents and non-formal checks |
| 2 | Released 0.3.0 / v1alpha2 | No | Same task using the existing PDaC artifacts/change/citation contracts |
| 3 | No | Yes | Same task with a competent existing requirements/traceability workflow and formal models |
| 4 | Released 0.3.0 / v1alpha2 | Yes | Same formal stack as 3, plus existing PDaC and external representations (architecture A) |

Match initial intent/facts, task/change requests, agent model/version/capabilities, ordinary tools, resource caps and evaluation facts. Cohorts 3/4 use identical formal binaries, configuration and library/translator semantics. Do not deprive cohort 3 of Git history, structured notes, assumptions or competent existing governance. Only the PDaC method/representation and formal-tool access vary as the planned treatments; record translation/governance/setup overhead and any unavoidable differences.

Use fresh authoring contexts between sessions; provide equivalent accepted history and current facts, with no hidden memory or withheld facts. Measure reconstruction effort rather than assuming equal context length. Count method instructions, tool output and repeated context against caps. Counterbalance cohort/task order across preselected seeds; record unsupported seed controls and model nondeterminism. Prevent cross-cohort copying and evaluation-case exposure. Independent evaluators receive outputs without cohort labels where feasible; representation can defeat blinding and must be disclosed.

Architectures A–D remain a separate dimension. Phase 2 starts with A; B/C/D receive documentary gap/cost assessments only unless later explicitly approved. No exhaustive factorial, native semantics or mandatory formalization is selected. Preserve prose/derived, selected-formal-canonical and explicitly mixed authority alternatives; translations expose undecided meaning to owners.

## Explore, freeze, execute, evaluate

1. **Exploratory calibration only if separately authorized at G1:** confirm access/licences, installability and supported fragments using public non-held-out examples. The [resource proposal](resource-proposal.md) bounds this option. A substitute external workflow is not a PDD Kit replication. A missing kit does not block unrelated tool candidates.
2. **Freeze before scored work:** record owner-approved intent/benchmark revision, agent/tool/library/translator revisions and digests, OS/architecture, commands, seeds/order, fault eligibility, held-out custody/manifest, reviewer identities/conflicts, budgets, thresholds and scoring. Replace all pending fields; link the immutable approved commit and owner decision. Independent evaluators keep held-out contents away from authors. No freeze or execution is claimed by merging this draft.
3. Execute only authorized issues #131–133 under the frozen design. Share approved artifacts/runs across those issues rather than rerun the same authoring episode for each. Preserve every attempt and stop at a limit or unresolved semantic decision.
4. Independent evaluation (#134) uses the [evaluation plan](evaluation-plan.md). G2 decides proceed/narrow/revise/pause/stop. No automatic phase transition.

[Benchmark plan](benchmark-plan.md) proposes two domains and a small evolving sequence. All counts, caps and quantitative decision margins below are candidates requiring approval, not empirical estimates or committed budgets.

## Evidence and reproduction

Each immutable run record identifies task/cohort/seed/attempt, accepted-intent and source revisions/digests, complete recorded formal dependencies/assumptions, model/translator/tool versions, agent inputs/handoffs/configuration, OS, limits, exact commands, raw results, proof/counterexample artifacts, costs and exclusions. Mark dependency-closure completeness unknown where unaudited. Record checked versus assumed interpretation, encodings, axioms, verifier/checker, compiler/FFI and external services. Do not publish confidential inputs or held-out contents prematurely.

Distinguish approved interpretation, satisfiable witness, counterexample/contradiction, proof under assumptions, exhaustive finite-model checking, bounded checking, sampled testing, unknown/timeout and unsupported analysis. Cite actual scopes; no bounded-search success or test pass becomes a universal proof. Structural impact, citation freshness, semantic dependency, mathematical validity and current-intent applicability remain separate. Preserve one-hop accounting, whole-artifact hashes and immutable old results; no automatic pin renewal, new proof fields or acceptance/apply gates.

A clean reproduction requires the frozen environment and authorized reproduction allowance. Retain failed attempts and raw output even if an experiment is invalid. No discretionary reruns or amendment after seeing held-out outcomes; seek an explicitly bounded versioned repair with fresh held-out evaluation. A corrected defect does not retroactively turn its earlier result into a pass.

## Entry and stop conditions

Pending: independent review of reports/protocol; named author/evaluator/product/formal-methods responsibilities; actual executable/model revisions; approved benchmark meaning and held-out custody; measurable numeric/money caps and thresholds. A full evaluation cannot start with these pending. G1 can instead authorize only the bounded calibration option.

Stop/escalate on a cap, missing metering/reviewer/access, ambiguous new intent, hidden assumption, unsupported guarantee, leaked held-out material or required scope change. Fabricated evidence and silent semantic decisions invalidate affected claims pending correction/review. Failed proof or inconclusive analysis is classified, not treated as automatic rejection of the direction. No production work, RFC, release or new methodology feature is authorized.
