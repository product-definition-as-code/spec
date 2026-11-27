# Formal product and requirements specification

Issue: [#123](https://github.com/product-definition-as-code/spec/issues/123). Retrieved 2026-11-27. Status: documentary comparison; independent review pending. Authority: [approved proposal](../../v0.4.0-formal-product-definition.md). H0/H1/H2 remain untested.

## Primary-source comparison

The last column is a research interpretation requiring evaluation, not an empirical usability ranking.

| Method / inspected source | Established mechanism | Boundary and adoption question |
| --- | --- | --- |
| [Design by Contract, Eiffel introduction](https://www.eiffel.com/values/design-by-contract/introduction/), live article, sections 2–3 | Mutual obligations express caller preconditions and supplier postconditions; specifications need not be exhaustive. | A contract alone does not show implementation correctness. Could owners review partial obligations without taking on language-specific development? |
| Spivey, [Z reference manual](https://www.rose-hulman.edu/class/cs/cs415/zrm.pdf), second edition (1992; author republication 1998), chapters 1, 2 and 5 | Schemas describe state and operations; operation/data refinement relate specifications and designs. | The PDF is a primary work hosted by an academic mirror; the proposal's Nottingham mirror timed out. Notation and refinement expertise add a training question, not an automatic reason to reject Z. |
| CLEARSY, [Atelier B guide](https://github.com/CLEARSY/Atelier-B-User-Guide/blob/main/atelierb-user-guide.md), dated 2024-12-13, targeting 24.04; “Principles” | Modular B models and proof obligations support formal development. The guide explicitly leaves requirements-to-model transformation to independent human review. | Formal modelling cannot by itself validate the selected requirements. The guide labels itself work in progress; document licence is CC BY-NC-SA 4.0, not an inferred tool licence. |
| Robinson, [Event-B draft](https://wiki.event-b.org/images/SM%26D-KAR.pdf), updated 2010-10-10, chapters 3, 5–7 | Contexts, machines, events, invariant preservation and refinement offer a vocabulary for state evolution and representation changes. | A refinement relationship is not evidence that a changed business decision preserves old intent. Evaluate model construction and obligation maintenance separately. |
| OMG, [OCL 2.4](https://www.omg.org/spec/OCL/2.4/PDF), formal/2014-02-03, sections 7.1 and 7.3 | Side-effect-free expressions specify invariants and pre/postconditions in model context. | Constraint evaluation does not execute a lifecycle transition. Model/type interpretation and supported tool fragments still need explicit selection for an experiment. |
| van Lamsweerde, [GORE Guided Tour](https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf), RE 2001, sections 2–6 | Goal structures connect elicitation, specification, refinement, conflict analysis and assumptions. | This is substantial prior art for linking intent to formal reasoning; it does not establish PDaC's distinctive contribution. The DOI endpoint required JavaScript; the author's full text was accessible. |
| [LiquidHaskell project documentation](https://ucsd-progsys.github.io/liquidhaskell/), live overview | Logical predicates refine Haskell types, with examples of input contracts, termination and functional properties. | A language-bound implementation mechanism is not an implementation-independent product notation. Tool/version/fragment and proof assumptions require later verification. |

These sources establish available concepts; no comparative performance, general owner comprehension or scalability was measured here. Live documents were retrieved on the date above and do not constitute pinned executable distributions.

## Reuse and authority alternatives

**Proposed interpretation:** external models can already express many candidate properties. The initial experiment should ask what PDaC adds to their fidelity and evolution, rather than count predicates as new methodological features. Keep a capable non-PDaC requirements/refinement workflow in cohort 3.

Compare the approved alternatives without choosing one:

- Approved prose, derived formulas: audit translation fidelity; extra decisions require owner approval.
- Approved formulas canonical for selected properties: owners must understand what they accepted and how the property relates to informal intent.
- Mixed representation: define authority per property, disagreement handling and change review explicitly.

None permits two independent, silently conflicting product truths. Study whether existing traceability and human review suffice before considering a profile or native semantics. Use Cases and Lifecycle text in released v0.3.0 remain prose contracts, not newly interpreted formulas.

## Verification, limitations and next input

Review the cited definitions against the report, then assess one booking rule and one authorization assumption using concrete alternatives understandable to the owner. Such an exercise would be calibration, not a scored experiment or a language selection; no encoding or prover was run here. No source access failure was concealed and no licence clearance for executing tools is claimed.

Carry to synthesis: reusable state/operation/refinement mechanisms; requirements-to-model review as a distinct obligation; uncertain training/maintenance cost; all authority models open. Independent review and quantitative evaluation are pending. Token/spend and human-attention metering are unavailable; no delegated agents, installations or solver jobs occurred.
