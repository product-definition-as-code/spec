# ProductShape changes and deterministic formal re-verification

Public exploratory work for #131–133, following merged #149. Released method **0.3.0**, serialization **v1alpha2**, published **ProductShape 0.26.1**, Z3 **5.3.3**, cvc5 **1.4.2**. This is a multi-artifact evolving research fixture, not a four-cohort evaluation, adopter study or normative proposal. The artifact forms and CLI operations are real; approval states and review reasons are **synthetic test inputs**, not claims of human product approval.

## What ran

`CHG-INITIAL` establishes eleven draft artifacts through the CLI. Six subsequent changes exercise an inclusive 60→30-day rule, issuer A→A/B, expiry from REQUESTED as well as CONFIRMED, a one→two-slot booking footprint with an updated concrete behaviour, unrelated report retention and an editorial Structured Behaviour edit. Each uses `change create`, overlay validation, exact neighbor accounting, `apply --dry-run`, `apply` and post-apply validation. The driver commits its isolated test history explicitly; ProductShape never commits or merges it.

| Observation | Actual result | Boundary |
| --- | --- | --- |
| Draft apply and missing neighbor judgments | ProductShape refuses them. Snapshot checks verify no product file changed. `PRODUCT034` identifies unaccounted neighbors. | Gate exercise, not semantic certification of the synthetic judgments later supplied. |
| Forecast before write | Dry-run leaves product files unchanged; all six affected-citation forecasts equal apply outputs. | Successful apply path and precondition failures; no new I/O fault-injection/transactional rollback qualification. |
| Invariants and adequacy | Eleven declared queries per model: reachable confirmation, confirm/cancel/expire preservation, lead compliance, concrete SB, authorization-definition consistency, guard/frame/double-release mutants and unreachable vacuous guard. Both engines agree before and after apply. | Conditional integer models, atomic effects and explicit assumptions; no runtime, concurrent-system or unbounded temporal proof. The authorization identity check is definition consistency, not an independent fidelity oracle. |
| Rule change | Consumer citing BR-A becomes stale; direct UC/SB citations and old evidence remain current. An old 60-day contract admits day 31, outside the new 30-day policy. | Current citation does not imply complete rule dependence or coverage of changed intent. |
| Cross-domain assumption | TERM-IDENTITY changes while UC-A/SB-AUTH stay byte-identical. Direct evidence remains current; issuer B distinguishes the new policy from the old A-only contract. | Authenticity/editor role are assumptions, not verified identity-provider behavior. The A example alone misses the policy difference. |
| Interacting lifecycle paths | REQUESTED expiry consumes/releases zero slots; CONFIRMED expiry releases its footprint. Both preservation obligations re-verify. | Topology is read from LC frontmatter; guards/effects still need an explicit interpretation. |
| Domain change | TERM-A and SB-A change. Live evidence participates in the forecast: SB-A becomes stale while its old external outcome remains `passed`. A new full recheck emits a new run document. | Old run documents/pins are retained; no renewal of the old evidence. |
| Unrelated/editorial | Both retain identical encoded formulas/cache keys and match full reruns. Editorial SB edit still makes whole-artifact citations/evidence stale. | Unchanged formulas establish mathematical reuse only. Declared editorial equivalence is a fixture judgment, not automatic natural-language equivalence detection. |
| Contradictory draft | Overlay has zero structural errors; encoded `days<=60 && days>=61` is unsatisfiable. Proposal rejected/archived, never applied. | Structural and semantic validation answer different questions; not a ProductShape conformance defect. |
| Unmapped semantic drift | Proposed two→three-slot meaning passes structural validation. Re-running the unchanged two-slot formula still passes. After explicitly updating the interpretation to three, the existing capacity-2 SB is unsatisfiable in both engines. No new evidence is published and the proposal is rejected. | Source-pin mismatch can require review; neither hashes nor solver success establish translation fidelity. |

One complete suite executes **334 satisfiability queries**, including repeated before/after checks, two engines and deliberate negative controls. These are not 334 independent observations or a fault-detection-rate estimate. Record wall latency is about one minute on this machine; see the receipt for exact runs. Human/agent authoring, installation and review are excluded from tool-job timing. Missing usage metering is unavailable, not zero, and does not block execution.

## Source intent, semantics and authority

The [fixture](fixture/) evolves the existing research booking model, with generic footprint references and an authorization rule/example. `formal.py` reads actual LC state/transition topology. The coordinator supplied footprint, lead-time, issuer and example interpretations explicitly; none is inferred or approved by a solver. Integer arithmetic, single-booking atomicity, whole-day lead times, fixed state mapping and trusted credentials are declared abstractions. The per-run `semantic-inputs.json` records exact source pins, formal dependencies, interpretation values, Git revision and dirty state.

This external interpretation is experimental derived material, not a new canonical PDaC artifact or formal language. Prose-derived, selected-formal-canonical and mixed authority remain open alternatives. The synthetic `unaffected` reasons are supplied fixture judgments with machine-computed pins, **not algorithmically discovered human judgments**. Their truth is not certified by structural validation.

Every full post-apply query uses a committed model checkpoint. New evidence records that actual run revision; the next Git commit merely stores the evidence. Immediate post-apply citation/evidence inspection may occur on the applied working tree before its commit: its reported model HEAD and content digests must be read together, not treated as a clean immutable tree. Historical provider outcomes and pins are never rewritten. Generic consumer citations deliberately omit some transitive semantic dependencies to test the documented completeness boundary; this is not a claim of complete traceability.

The closed v0.3 evidence envelope carries outcome/level/citations. Formal method, fragment, assumptions, dependency pins, source/model correspondence and cache provenance remain in an external manifest. Existing external files suffice for this experiment; no missing PDaC field is inferred merely because that data lives externally.

## Reproduction without an LLM

Prerequisites: the previously pinned formal tools, Linux/user systemd cgroups, Node >=22, Python and the repository's `scripts/requirements.txt`, Git. Existing infrastructure only. Install the exact npm lock without lifecycle scripts:

```sh
mkdir -p /tmp/pdac-v040-productshape
cp docs/research/v0.4.0/experiments/11-evolution/tools/package*.json /tmp/pdac-v040-productshape/
npm ci --prefix /tmp/pdac-v040-productshape --ignore-scripts --no-audit --no-fund
python3 docs/research/v0.4.0/experiments/install-tools.py /tmp/pdac-v040-tools
python3 docs/research/v0.4.0/experiments/11-evolution/experiment.py \
  --productshape /tmp/pdac-v040-productshape --tools /tmp/pdac-v040-tools \
  /tmp/pdac-v040-new-run
python3 docs/research/v0.4.0/experiments/11-evolution/verify.py /tmp/pdac-v040-new-run
```

Output directory must be new. Each job has 30 seconds, 2 GiB, no swap, 64 tasks and whole-cgroup termination; no automatic retries. The scripts make zero LLM calls. Recorded source hashes must remain unchanged during execution. Package-lock integrity pins the published dependency tree. Semantic inputs and all failure/unknown statuses are retained; an unexpected verdict or execution failure stops the suite.

[Results](results/) contain the manifest, receipt and compressed raw evidence. Extract the evidence archive into a new directory and run `verify.py` there to audit hashes, gate results, full/cache consistency, provider revisions and immutable accepted change containers. `history.bundle` reconstructs the isolated Git history. Plain `.smt2` files run directly with Z3/cvc5 without ProductShape or an LLM; this demonstrates computational separation, not a non-PDaC cohort comparison.

## Limitations and methodological implications

All negative cases and interpretations are public and author-designed. Source fidelity, adequacy, formal dependency completeness and the synthetic review decisions were not independently adjudicated. No independent agent-session maintenance, held-out cases, cohort scoring, H0 advantage or production implementation correspondence is established. Solver agreement is not independent certificate checking.

The experiment exposes two genuine **research questions**, not accepted feature requirements: how to govern/review source-to-formal bindings across changes, and how to assess contract adequacy beyond authored examples. Native structured lifecycle topology contributes deterministic input; prose guards/effects and domain meaning remain interpretation boundaries. Existing Git, PDaC changes/citations and external formal manifests may already solve these adequately. Recommending no specification change remains possible. Scored comparisons still meet the existing G1 freeze/independence requirements; ordinary engineering work does not gain a new approval gate.

Development attempts are recorded separately: a syntax error before any tool execution, an invalid `get-value` request after an expected `unsat` during a negative probe, and checker/test-fixture corrections. Original incomplete outputs are preserved as development evidence, not counted as completed replications or scientific negative results. The last defect is fixed by keeping the fixed scenario query's status without asking for a nonexistent model. Subsequent full runs and receipt audits must pass before merging.
