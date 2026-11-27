# Automated reasoning and model checking

Snapshot boundary: the documentary findings and execution-status statements below describe the original phase-one report revision. Subsequent authorized [executable exploration](../experiments/README.md) and independent review are tracked separately; unavailable cost/token metering is not a current prerequisite. No historical result is silently upgraded.

Issue: [#124](https://github.com/product-definition-as-code/spec/issues/124). Retrieved 2026-11-27. Status: documentary capability map; independent review pending. [Approved proposal](../../v0.4.0-formal-product-definition.md): H0/H2/H3/H5 are untested. No solver was installed or run.

## Mechanisms, bounds and trust

| Primary source / inspected version | Available mechanism | Guarantee boundary / experimental implication |
| --- | --- | --- |
| [SMT-LIB language index](https://smt-lib.org/language.shtml), standard 2.7 listing | Common language, theories and logics separate problem encoding from one solver API. | A standard version does not establish that a candidate binary supports every construct. Pin the selected fragment, semantics and solver version before evaluation. |
| Z3 guide, [logic introduction](https://microsoft.github.io/z3guide/docs/logic/intro/) and [basic commands](https://microsoft.github.io/z3guide/docs/logic/basiccommands/), live deployment identifying documentation revision `72e37427` | Satisfiability/model queries; `sat`, `unsat`, `unknown`; assertion scopes with `push`/`pop`. | A model witnesses the encoded constraints; `unknown` is inconclusive. Incremental assertion management does not determine which changed product assumptions invalidate an old conclusion. The site's browser-package version is not a selected experiment binary. |
| [Alloy 6](https://alloytools.org/alloy6.html), “Time horizon” and “Complete model-checking” | Relational/temporal models, counterexamples, bounded traces and complete temporal checking over signature-bounded finite state spaces. | Unbounded time does not remove object/signature bounds. Complete finite-model checking is distinct from bounded search and from an unrestricted theorem. Backend, integer and time scopes must be recorded. |
| Lamport, [Specifying Systems](https://lamport.azurewebsites.net/tla/book-21-07-04.pdf), first-printing text, 2002; PDF recreated 2021-07-04; chapters 8, 10 and 14 | Temporal specifications, fairness, composition and TLC model checking. | A TLC configuration is part of the evidence boundary; do not label a checked instance as a proof for arbitrary model sizes. Runtime correspondence is a separate experiment. |
| [ProB documentation](https://prob.hhu.de/w/index.php?title=The_ProB_Animator_and_Model_Checker&oldid=6263), wiki revision 6263; [licence page](https://prob.hhu.de/w/index.php?title=ProBLicence&oldid=6149) | B/Event-B animation, model finding, model/refinement checking and multiple backends. | Language/backend coverage and finite abstractions need per-case confirmation. Source licence is documented as EPL 1.0; bundled-component conditions are version dependent, so inspect the selected distribution rather than infer unrestricted reuse. |
| [cvc5 documentation](https://cvc5.github.io/docs/latest/), live index with versioned documentation links | Another SMT engine with documented proof-production and resource-limit interfaces. | A relevant portability/cross-check candidate, not a selected backend or independent proof certificate already checked here. Pin an actual release, supported logic and checker before claiming portability. |

## Candidate comparisons, without selection

**Proposed approach:** start with a product-constraint task (capacity/permission consistency) and a state-evolution task (reservation/cancellation and changed identity assumptions). Consider an SMT encoding family and a relational/state-transition family; use the smallest subset that the owner-approved protocol can afford. An inability to represent a required property is a recorded limitation, not permission to weaken the property.

Cohorts 3/4 must use the same chosen formal tooling, versions and limits. Otherwise a solver effect could be mistaken for a PDaC effect. A–D remain a separate design dimension; no benchmark result here supports a PDaC extension.

For each query record whether it asks for a witness, a contradiction, invariant violation or theorem obligation. Require reachable intended scenarios as well as safety checks. Make assumptions explicit; empty models and false preconditions can make apparently successful verification useless. Keep counterexamples explainable to the owner.

## Reproduction contract and disposition

Before a future run, pin OS/architecture, executable and translator digests, source/model revisions, logic, backend, finite scopes, fairness assumptions, seeds, timeout/memory limits, commands, raw output and any certificate/checker. Compare incremental results with full rechecking; record unsupported syntax, unknowns and timeouts separately. Successful syntax parsing, `unsat` and proof-certificate validation are different observations.

The documentation supports available mechanisms, not their relative speed, owner usability, installation success or portability in this workspace. Those remain unmeasured. Token/spend and human-attention metering are unavailable; no delegated agent or reasoning job ran. Carry candidate families, version/fragment checks and scope-sensitive verdicts to synthesis/G1. No solver, architecture or normative language is selected.
