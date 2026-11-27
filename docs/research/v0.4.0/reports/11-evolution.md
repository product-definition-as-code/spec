# Product Changes and proof applicability — exploratory result (#133)

Question: what survives real ProductShape apply, and what requires explicit formal re-verification?

[Executable commands, models, assumptions](../experiments/11-evolution/README.md); [two-run evidence](../experiments/11-evolution/results/summary.json). Seven applied changes including initial population, six successive semantic/unrelated/editorial evolutions. ProductShape 0.26.1 enforces draft and neighbor-accounting gates. Dry-run writes nothing; citation forecasts match apply. Each accepted model is committed, fully rechecked by Z3/cvc5 and receives new historical evidence; prior evidence remains immutable.

Rule and issuer changes can leave direct evidence current despite new intent exceeding old contracts. Domain/example edits leave the old outcome passed while its citation becomes stale. Unrelated/editorial changes reuse identical formulas/cache keys and match full reruns; editorial source citations still become stale. Structural one-hop impact, citation freshness, formal dependencies, historical mathematical validity and current applicability remain distinct.

The reusable integration is external, with explicit source/formal pins and raw receipts. No optimized incremental prover, automatic dependency-completeness algorithm, runtime bridge or generic prose-equivalence check is implemented. Synthetic approvals are test fixture states, not human product acceptance. No independent agent-session comparison was executed. #133 remains open for that scientific acceptance, not because routine engineering needs another approval. Evidence currently supports testing governance of source/formal bindings and adequacy, without establishing a need for a normative extension.
