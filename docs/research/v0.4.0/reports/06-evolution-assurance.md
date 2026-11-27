# Evolution, traceability and assurance boundaries

Snapshot boundary: the documentary findings and execution-status statements below describe the original phase-one report revision. Subsequent authorized [executable exploration](../experiments/README.md) and independent review are tracked separately; unavailable cost/token metering is not a current prerequisite. No historical result is silently upgraded.

Issue: [#127](https://github.com/product-definition-as-code/spec/issues/127). Retrieved 2026-11-27. Status: documentary findings and proposed dependency cases; independent review pending. [Proposal](../../v0.4.0-formal-product-definition.md) H0/H4/H5 remain untested.

## Established boundaries and reusable prior art

| Primary source / inspected version | Available mechanism / limit |
| --- | --- |
| Released PDaC `v0.3.0`: [Product Changes](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/product-changes.md), [citations](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/citation-contract.md), [Verification Evidence](https://github.com/product-definition-as-code/spec/blob/v0.3.0/spec/verification-evidence.md); RFCs 0082/0115/0116 | One-hop structural accounting and a direct changed-target citation forecast are explicit contracts, not semantic dependency closure. Whole-artifact normalized-byte changes make citations stale; external outcomes remain separate from freshness. Evidence does not authenticate its own execution or add Product Graph edges. |
| [AGREE README](https://github.com/loonwerks/AGREE), live `master`, overview | Composes AADL component assumptions/guarantees using model checking with k-induction. Environmental assumptions matter to higher-level conclusions. This is existing architecture/tool-specific reasoning, not evidence of product-to-runtime correspondence or a PDaC benefit. |
| OMG [SACM 2.3](https://www.omg.org/spec/SACM/2.3/PDF), formal/23-05-08, October 2023; sections 7.3–7.5 | Expresses claim/argument structures and evidence provenance. The standard explicitly separates representing an argument from establishing its correctness, completeness or acceptance. A richer evidence graph alone would not solve verification. |
| Robinson, [Event-B draft](https://wiki.event-b.org/images/SM%26D-KAR.pdf), updated 2010-10-10; chapters 3 and 7 | Refinement and representation relationships are established mechanisms to investigate before inventing equivalents. A deliberate change of accepted intent need not be a refinement of its previous meaning. |
| [Dafny reference](https://dafny.org/latest/DafnyRef/DafnyRef), live snapshot, sections 13.7.5–13.7.6 | Describes proof-dependency reporting and brittle verification after valid changes. Dependency reports and a timeout are not, by themselves, judgments about current product meaning. |

The [Gotel/Finkelstein traceability paper](https://csis.pace.edu/~ogotel/research/GOTEL94%20Making%20Requirements%20Elicitation%20Traceable.pdf) returned 502; it remains an unread primary reading lead, with no empirical finding attributed to it. None of the tools above was installed or executed.

## Five separate observations

The following are analytical experiment-design examples, not checked proofs or newly accepted product decisions.

| Observation | Proposed controlled case | What must not be inferred |
| --- | --- | --- |
| Structural impact | Change a rule linked to a requirement; inspect the released one-hop accounting | Accounting for direct neighbours does not establish all formal semantic dependencies |
| Citation freshness | Edit explanatory prose in a cited artifact while preserving the modeled predicate | A stale whole-artifact citation does not mathematically refute a proof about the earlier model |
| Formal dependency | Change an uncited issuer/capacity assumption while the direct cited target stays byte-identical | A fresh direct citation does not show that the complete assumption closure is unchanged |
| Mathematical validity | Retain a checked theorem and its original model/assumption revision | Historical validity does not imply applicability to newly accepted intent |
| Evidence applicability | An owner changes cancellation or authorization meaning, but old evidence still proves the old contract | A retained “passed” outcome is not verification of the new product decision |

Also include unrelated edits, changed domain units, interacting expiry/cancellation transitions and independent-agent weakening of a contract. Cache/reuse results must be compared with a full recheck and independent intent review. These cases belong in the small phase-2 evolution sequence; scalability and actual implementation evidence remain later work.

## Proposed dependency and trust record

For a future run, record property identity, accepted-intent revision, formal-model/translation revision, imported definitions and assumptions, code/tool versions, claimed guarantee/bounds and checked versus trusted components. Keep the semantic dependency graph experimental and separate from the normative Product Graph. It may be incomplete: audit against seeded transitive faults and label unmodeled external dependencies.

Keep old proofs/results immutable. Assess separately whether a proof needs rechecking, whether the model reflects current intent and whether the report is properly cited. No automatic citation-pin renewal, new apply gate, proof level or expansion of one-hop accounting is proposed. The closed v0.3 evidence envelope cannot silently acquire trust/proof fields; use separate non-normative reports and valid citations.

## H0/H5 evaluation and disposition

Existing assumption/guarantee, refinement, provenance and proof-dependency mechanisms may already suffice. Compare equivalent non-PDaC workflows on missed/spurious invalidation, correctly retained evidence, reconstruction/maintenance work and human review, with governance cost included. A larger dependency graph is not itself a benefit.

A reviewer should trace each boundary to the tagged specification or cited source, then audit the five-way classification using frozen examples. Future experiments need source/model digests, dependency closure, commands, full/incremental outputs, limits and reviewer verdicts. No invalidation experiment or implementation proof ran here. Independent review, actual completeness/performance and numeric limits remain pending. Token/spend and human-attention metering are unavailable; no delegated agents or reasoning jobs occurred. Carry the distinct layers, access gap and no-extension alternative into synthesis/G1.
