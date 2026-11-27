# Specification adequacy — exploratory result (#132)

Question: which weak contracts or vacuous checks can be exposed deterministically beyond an authored example?

Use the shared [ProductShape/SMT integration](../experiments/11-evolution/README.md) and [recorded evidence](../experiments/11-evolution/results/summary.json), rather than duplicating its baseline. Guard, owner-frame and double-release mutants admit counterexamples; an unreachable guard makes preservation vacuous while reachability is unsatisfiable. The fixed Structured Behaviour passes normal models, but contradicts an explicitly corrected three-slot interpretation at capacity two. Issuer-A-only examples miss the new issuer-B policy; the distinguishing contract probe exposes it.

The authorization-definition equivalence query checks consistency of a definition, not independent adequacy. Both solvers share the same authored encoding and assumptions. No mutation score, general correctness, independent intent oracle or cohort advantage is established. Negative and inconclusive earlier feasibility outcomes remain preserved. #132's independent/held-out scientific evaluation remains pending G1; this report supplies reproducible engineering inputs.
