# Specification adequacy — exploratory result (#132)

Question: which weak contracts or vacuous checks can be exposed deterministically beyond an authored example?

Use the shared [ProductShape/SMT integration](../experiments/11-evolution/README.md) and [recorded evidence](../experiments/11-evolution/results/summary.json), rather than duplicating its baseline. Guard, owner-frame and double-release mutants admit counterexamples; an unreachable guard makes preservation vacuous while reachability is unsatisfiable. The fixed Structured Behaviour passes normal models, but contradicts an explicitly corrected three-slot interpretation at capacity two. Issuer-A-only examples miss the new issuer-B policy; the distinguishing contract probe exposes it.

The authorization-definition equivalence query checks consistency of a definition, not independent adequacy. Both solvers share the same authored encoding and assumptions. No mutation score, general correctness, independent intent oracle or cohort advantage is established. Negative and inconclusive earlier feasibility outcomes remain preserved. #132's independent/held-out scientific evaluation remains pending G1; this report supplies reproducible engineering inputs.

## Controlled attempt after G1

The approved controlled attempt was executed once and is [invalid due to common tool-transport failure](12-independent-evaluation.md). Eight authors produced no models; successor slots remain blocked and all case outcomes unknown. Earlier exploratory observations above remain engineering evidence only. This issue's controlled scientific acceptance is not completed; [G2 recommends bounded revision](../gates/phase-2-decision.md).
