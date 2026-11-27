# Independent agent review — experimental methodology

Reviewed immutable `91053aadbd2f40f9ae2a3c2a0c12bcd814328169`, 2026-11-27, fresh session `/root/methodology_review`, no author conversation/history or other reviewer findings. Coordinator transcribed the returned report. Requested named model unspecified; exact resolved/provider-reported identity unavailable. Common provider/infrastructure and curator limit independence; agent critique is not human expert validation or future evaluator/held-out independence.

## Findings

**M1 — P2, high certainty.** `protocol/evaluation-plan.md:26` still requires monetary/time/attention caps to hold for its token-overhead screen, contrary to corrected resource policy. `experimental-protocol.md:20–22` can imply matching financial controls; original proposal:108 has old cap requirements without a local supersession note. Minimum correction: remove financial gating, make token-overhead observation conditional on available measurements, clarify technical matching and annotate the non-normative proposal's historical requirement. This inconsistency is not a reason to stop exploration.

**M2 — P2, high certainty about the path; occurrence unobserved.** `experiments/run.py:23–32`: the outer `subprocess.run(timeout=45)` can raise before raw-output/receipt writes, losing an attempt record required by the protocol. Ordinary systemd timeouts may return normally; no outer timeout was induced or observed by the reviewer. Minimum correction: retain partial output and failure classification for outer timeout/launch error, terminate the affected job and record failure without retry.

No evidenced P0/P1 finding. Recommendation: continue exploration, reconcile M1 and repair M2; complete existing freeze requirements before comparative scoring.

## Coverage and limitations

Read methodology/review briefs and manifest; proposal; six reports, synthesis/ledger, four protocol documents and gate changes; README, installer/runner/reproduction/check/evolution scripts and selected outputs/input manifest. Compared original documentary inputs to consolidated snapshot. No independent literature retrieval, exhaustive formula/output audit, experiment execution or reproduction. No edits, author history/memory retrieval, other reviewer findings, publication or delegation.

Positive observations: four cohorts separate from A–D; competent non-PDaC governance/history in cohort 3; matched formal tools for 3/4; independence, blinding limits, dependent trajectories, unknowns and held-out/public separation acknowledged. Thresholds are provisional, without power claims. Intent/assignment/custody/scoring openly pending; no frozen comparison or PDaC benefit established.

## Coordinator dispositions

- M1: corrected evaluation rule and technical matching; short owner-decision supersession note added beside the original non-normative proposal's phase table. Missing metering cannot block execution or justify a cost-benefit claim.
- M2: outer timeout/launch failure now produce raw files and classified JSON; timeout cleanup targets only the invocation's unique systemd unit. Previous attempt names cannot be overwritten. Two mocked failure-path tests verify partial evidence, scoped cleanup, launch failure and overwrite rejection. The successful formal suite was reproduced after the runner change. These tests do not claim a real outer timeout occurred or qualify every systemd failure mode.

Dispositions are coordinator checks, not reviewer re-acceptance of later revisions.
