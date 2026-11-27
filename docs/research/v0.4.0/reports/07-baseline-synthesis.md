# Synthesis against released PDaC v0.3.0

Issue: [#128](https://github.com/product-definition-as-code/spec/issues/128). Date: 2026-11-27. Status: provisional synthesis; independent review pending. Authority: [approved proposal](../../v0.4.0-formal-product-definition.md). The owner authorized preparing dependent drafts without waiting for earlier approvals; that instruction does not establish the findings' independent acceptance.

## Inputs and evidential strength

All six reports below are unmerged documentary inputs authored in this session. Immutable links prevent later branch edits from silently changing this synthesis. Reconcile any reviewed changes before freezing the protocol; do not close dependencies merely because a draft exists.

| Work item | Exact report input | Revision / review |
| --- | --- | --- |
| #122 / [PR #141](https://github.com/product-definition-as-code/spec/pull/141) | [01-microsoft-github-next.md](https://github.com/product-definition-as-code/spec/blob/094f1204e9b8a03597ff174302c2a7619d27a9ef/docs/research/v0.4.0/reports/01-microsoft-github-next.md) | `094f120`; independent review pending |
| #123 / [PR #142](https://github.com/product-definition-as-code/spec/pull/142) | [02-formal-requirements.md](https://github.com/product-definition-as-code/spec/blob/1de520ef8510f66fc2226f61aa5fbace151178c7/docs/research/v0.4.0/reports/02-formal-requirements.md) | `1de520e`; independent review pending |
| #124 / [PR #143](https://github.com/product-definition-as-code/spec/pull/143) | [03-reasoning-model-checking.md](https://github.com/product-definition-as-code/spec/blob/3286ac0d339e4edf7b956bd7d6b4e068bff2aa5f/docs/research/v0.4.0/reports/03-reasoning-model-checking.md) | `3286ac0`; independent review pending |
| #125 / [PR #144](https://github.com/product-definition-as-code/spec/pull/144) | [04-proof-oriented-implementation.md](https://github.com/product-definition-as-code/spec/blob/d4b763b60b7317373a099d9e93ab24af124da3e1/docs/research/v0.4.0/reports/04-proof-oriented-implementation.md) | `d4b763b`; independent review pending |
| #126 / [PR #145](https://github.com/product-definition-as-code/spec/pull/145) | [05-specification-adequacy.md](https://github.com/product-definition-as-code/spec/blob/e6ab4355ebbfd4dae6579cac76435bdb8572c582/docs/research/v0.4.0/reports/05-specification-adequacy.md) | `e6ab435`; independent review pending |
| #127 / [PR #146](https://github.com/product-definition-as-code/spec/pull/146) | [06-evolution-assurance.md](https://github.com/product-definition-as-code/spec/blob/6ef902045c39e7d67d92843187a47ecaa957f9f2/docs/research/v0.4.0/reports/06-evolution-assurance.md) | `6ef9020`; independent review pending |

The [claim/evidence ledger](../claim-evidence-ledger.md) separates contracts, published findings, interpretations and untested hypotheses. The pinned documentary inputs contained no new formal results. Subsequent [executable exploration](../experiments/README.md) supplies actual small-model results and handwritten contract feasibility, with failed/inconclusive attempts retained. No scored cohort or implementation correspondence result is claimed; repository CI is not research qualification.

## Mapping mechanisms to the baseline

| Mechanism / primary basis | Released v0.3.0 contribution | Remaining question |
| --- | --- | --- |
| Explicit intent and reviewed decisions: [PDD walkthrough](https://www.microsoft.com/en-us/research/blog/formally-verifying-agent-written-full-stack-web-apps-with-pdd-kit/), steps 1–7 | Stable product artifacts and governed Product Changes provide an existing place for accepted intent. | Is maintenance across independent sessions better than a competent non-PDaC formal workflow? |
| State/operation/refinement: [Z](https://www.rose-hulman.edu/class/cs/cs415/zrm.pdf), chapters 1/5; [Event-B](https://wiki.event-b.org/images/SM%26D-KAR.pdf), chapters 3/7; [GORE](https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf), sections 2–6 | Lifecycle/Use Case/Rule text and relationships provide product context, not a general formal interpretation. | Can external representations suffice without a new formalism? |
| Adequacy checks: [SPOTs](https://risemsr.github.io/blog/2026-04-16-spotting-specs/) and [QuickChick](https://github.com/QuickChick/QuickChick) | Structured Behaviours carry accepted concrete examples. | Does structured context improve held-out contract adequacy beyond those examples? |
| Semantic dependencies and assumptions: [AGREE](https://github.com/loonwerks/AGREE); [Dafny proof dependencies](https://dafny.org/latest/DafnyRef/DafnyRef) | One-hop structural review and direct citation forecasts expose defined consequences. | Can existing dependency tools maintain applicability without extending the Product Graph? |
| Assurance/provenance: [SACM 2.3](https://www.omg.org/spec/SACM/2.3/PDF), sections 7.3–7.5 | Optional Verification Evidence separates external outcome from citation status; it is a closed envelope, not proof authentication. | Is a separate experimental report sufficient to explain trust and guarantees? |

Baseline claims above refer to tagged [artifacts](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/artifacts.md), [relationships](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/relationships.md), [Product Changes](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/product-changes.md), [citations](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/citation-contract.md) and [evidence](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/verification-evidence.md). No released semantics changed.

## Options, exclusions and genuine gaps

**Provisional interpretation, not an experimental result:** formal mechanisms already exist. No source establishes that PDaC is necessary for their usefulness. The unresolved H0 contribution is net fidelity, adequacy and continuity across changes, including reconstruction, redundant work and human review versus added governance cost.

- A, unchanged v0.3 plus external tools, is the approved starting point and a valid final outcome. Feasibility depends on actual access/versions and owner-readable intent review.
- B, external integration/reporting, warrants consideration only for a measured reporting/coordination gap; existing citations and separate reports may suffice.
- C, optional profile, needs an inadequately solved interoperability/adoption problem. No such measured gap is established yet.
- D, native semantics, needs a demonstrated gap A/B cannot adequately address and an acceptable complexity/authority cost. It is neither selected nor disproved.

Exclude from this initial work the already out-of-scope custom prover/language, mandatory formalization, production implementation and exhaustive tool-by-architecture factorial. Do not shortlist a method merely because it proves a toy model. These scope exclusions are not evidence that an architecture is false.

Retain approved prose with derived formulas, selected canonical formal properties and explicitly mixed authority as experimental alternatives. Generated translations cannot silently introduce product decisions. Do not widen one-hop accounting or add proof fields/gates to the released specification.

## Minimum useful comparison and uncertainties

Prepare two small domains: evolving booking decisions and authorization with external identity assumptions. Use four matched agentic cohorts, the same formal stack in cohorts 3/4 and a capable requirements/traceability control without PDaC. Include independently scored held-out faults, non-empty intended witnesses, partial contracts and independent-session handoffs. Measure costs and failed/inconclusive attempts as well as successful checks.

Phase 2 tests product models and continuity. H4 implementation correspondence and claims about executed software stay untested until an approved phase-3 bridge. Seeded success would support only the benchmark, not general product correctness.

Access gaps in the original documentary review: a replicable/licensed PDD Kit bundle was not established; ART timed out; traceability full text returned 502. GORE and Z full texts were accessible. Subsequent exploration installed pinned Z3/cvc5/Alloy/Dafny, checked a shared fragment, inspected licences and ran public models. Alloy distribution/source licensing remains ambiguous; no blanket clearance or redistribution is claimed. Source access gaps do not block independent tools.

Current evidence supports continuing A (unchanged v0.3 plus external tools), without selecting a final architecture. Deterministic tools can execute verification, counterexample/witness checks, graph/hash comparisons and reproduction without an LLM once encodings and dependency assumptions are supplied. Semantic translation, dependency completeness and current-intent applicability remain judgment boundaries. The Structured Behaviour encoding correction demonstrates why solver success alone is insufficient. No measured distinctive PDaC benefit, native-semantics need or H0–H5 confirmation is established.

The owner authorizes public exploration and documentary review without monetary/token prerequisites. No purchases or paid provisioning. Frozen intent/controls/held-out custody and independent evaluation remain necessary before scored comparative claims. G1 stays open for that decision; routine exploration and corrections continue.
