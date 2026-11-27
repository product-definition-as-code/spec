# Independent evaluation plan — proposed

Issue #129. Prepared 2026-11-27. Status: thresholds, evaluators and protocol approval pending. No observations or scores exist. [Protocol](experimental-protocol.md) and [benchmark](benchmark-plan.md).

## Questions and measures

Primary H0 contrast is cohort 4 versus 3 on matched tasks/change episodes with identical formal tooling. Cohorts 1/2 distinguish PDaC's non-formal contribution; 3/4 versus 1/2 explore verification effects. Do not attribute one tool's advantage to PDaC. Phase-2 conclusions concern product models and independent-session continuity, not implementation proofs or general software-development effectiveness.

| Hypothesis | Predeclared observation / denominator |
| --- | --- |
| H1 | Relevant unintended intent decisions missed, and legitimate behaviours rejected, among independently adjudicated eligible cases; owner-review agreement and uncertainty |
| H2 | Actionable contradictions/consistency findings, non-empty reachable intended witnesses, false positives and excluded accepted behaviours, by fault class |
| H3 | Eligible seeded/held-out faults detected; survivors, equivalent/invalid mutants, vacuity and unknowns separately |
| H5 | Missed/spurious invalidation and correctly retained evidence across structural impact, citation freshness, semantic dependencies, mathematical validity and current-intent applicability |
| H0 | Matched fidelity/adequacy/continuity plus agent cost/tokens, reconstruction/redundant work, human attention/review and verification latency; report governance/setup/maintenance overhead |
| H4 | Product-contract/session observations only; implementation translation, executable-path proofs and runtime correspondence explicitly untested until phase 3 |

Record raw counts and eligible-case denominators per cohort/seed/episode. Invalid exclusions need independent reasons and preserved artifacts. Unknown/timeout is not detection or success; report both complete-case rates and an all-eligible lower bound treating unknowns as undetected. Never equate a model witness, a counterexample, a finite/bounded check, a proof or a sampled test.

## Candidate quantitative screening margins

These values are proposals for a small pilot decision, not findings, approved thresholds or a power analysis:

- Possible worthwhile benefit: at least **10 percentage points** fewer missed eligible semantic faults, or at least **20%** less measured human review/context-reconstruction time in cohort 4 versus 3. Report each time component separately. Either route must meet the other safeguards; no post-hoc choice of a winning metric.
- Safeguard: **zero additional rejections of owner-approved valid behaviours** on the declared benchmark; report the counts rather than infer universal non-regression.
- Candidate overhead screen: no more than **25%** additional total agent tokens, while monetary/time/attention caps also hold. Exceeding it is a cost finding requiring G2 judgment, not automatic scientific refutation.
- A falsely current proof claim, concealed assumption or silent product decision must be reported/corrected and blocks accepting the affected assurance conclusion. A missed seeded invalidation counts against H5; it is not automatically fabricated evidence or proof that every architecture fails.

The margins make a practically visible pilot difference explicit; their adequacy has not been empirically calibrated. Before freeze the owner may revise them, with rationale. Predeclare sensitivity at fault margins 5/10/15 percentage points, effort reductions 10/20/30% and token overhead 10/25/50%. Report the whole panel, not whichever boundary favours H0. If valid behaviour or other primary quality dimensions regress, do not declare H0 supported solely because another metric improves.

Two seed schedules are economical replication, not an adequate population sample by assumption. Treat episodes from one trajectory as dependent; do not fabricate statistical power, independent sample counts or a p-value. Report paired raw outcomes, ranges and inconclusiveness. No gain or excessive governance cost is evidence against H0 in this benchmark, not a universal theorem that PDaC cannot help.

## Independence, integrity and rejection taxonomy

Name evaluators separate from authors, record conflicts/exposure, mask cohort labels where feasible and disclose residual unblinding. Held-out custodians classify seed validity and expected behaviours independently; humans retain product decisions. Owner-approved intent is fixed before authors formalize it. A new session alone does not guarantee independent judgment or an unbiased oracle.

Classify: invalid experiment; correctable implementation/design defect; failed verification; unsupported/inconclusive analysis; valid evidence against a hypothesis; evidence against an architectural alternative; evidence against extending PDaC. Do not infer the latter categories automatically from the former. Withdraw unsupported claims, retain every attempt, and seek bounded repairs with versioned amendments and fresh held-out evaluation; no repeated redesign until success.

## Gate output and reproduction

Issue #134 produces independently reviewed raw/cohort comparisons, hypothesis judgments with uncertainty, cost breakdowns, protocol deviations and a proceed/narrow/revise/pause/stop recommendation. A–D can be compared only as far as actual evidence permits; no trial of C/D is implied. A valid no-extension outcome remains available.

Reproduction uses immutable manifests with source/model/dependency revisions, inputs/handoffs, seeds/order, tools/configuration, limits, commands, proof/counterexample outputs and adjudications. Check representative claims within a separately approved allowance; record failed reproduction. G2, not a score alone, decides whether correspondence/stress work may proceed. No normative RFC, package or release follows automatically.
