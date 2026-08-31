# RFC 0000: Use Case journey context is optional

- **Status:** draft
- **Author(s):** Juan G. Carmona
- **Created:** 2026-08-31

## Problem

The current warning table defines `PRODUCT102` as “Active use case not present in any journey” ([Validation → Warning codes](../spec/validation.md#warning-codes)). A conforming implementation must therefore warn whenever no Journey carries an active Use Case in `steps[].use-case`. A repository that enables `validation.warnings-as-errors` turns that warning into a failed command even though the diagnostic remains a warning.

This treats one absent contextual relationship as a structural defect, but the rest of the reference profile does not establish that invariant:

- The Use Case schema requires a `primary-actor` and has no Journey field. The canonical relationship is authored from `Journey.steps[].use-case`, so its natural inverse cardinality is zero or more Journeys.
- A Journey's `steps` list is expressly the main ordered path. Branches and exceptional paths belong in the body ([Artifacts → Journey](../spec/artifacts.md#journey-journey-jrn-)). A Use Case that occurs only on a branch cannot satisfy `PRODUCT102` without being falsely added to the main path.
- A Use Case can already have a primary actor, governing rules, domain terms, derived requirements and Structured Behaviours. Absence of one incoming Journey edge does not make that product knowledge disconnected.
- The specification already uses a different rule for a possible semantic omission: absence of a Requirement reference to a Structured Behaviour may be surfaced as non-conformance advice for human review, but not as a deterministic diagnostic ([Artifacts → Structured Behaviour](../spec/artifacts.md#structured-behaviour-structured-behaviour-sb-)).

The behavior also lacks a recorded design decision. `PRODUCT102` entered with the [initial specification extraction](https://github.com/product-definition-as-code/spec/commit/06ce4ddd0583a16e8d4b0ca2ff52eaa630895e4a), rather than through an RFC, and the diagnostic coverage table still marks it “not yet covered” ([Conformance tests → Diagnostic coverage](../conformance/README.md#diagnostic-coverage)).

The reference implementation's own model exposes the false-positive pressure. ProductShape issue [#165](https://github.com/juangcarmona/productshape/issues/165) records nine `PRODUCT102` warnings. Every reported Use Case has a primary actor and one or more derived requirements. More decisively, [`JRN-ADOPT-001`](https://github.com/juangcarmona/productshape/blob/main/docs/product/model/journeys/jrn-adopt-001.md) already identifies the Recover workflow as its brownfield variant. `UC-RECOVER-001` is correctly absent from the main `steps` list because Recover replaces Define on that branch. Adding it to `steps` merely to clear the warning would make the accepted model less truthful.

### Research basis

No reviewed standard or primary methodology source requires a Use Case to belong to a User Journey:

- The normative [OMG UML 2.5.1 specification](https://www.omg.org/spec/UML/2.5.1/) defines Use Cases, actors, subjects, `include`, `extend` and generalization. It does not define a `UserJourney` metaclass or a Use Case-to-User Journey ownership relationship. A Use Case may be owned by a Package or Classifier, while `UseCase::subject` has multiplicity `0..*`; OMG's resolved [UML25-519](https://issues.omg.org/issues/UML25-519) explicitly clarifies that a Use Case may refer to many subjects or none. Ownership, system boundary and journey context are different relationships.
- The official [ISO/IEC/IEEE 29148:2018](https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:29148:ed-2:v1:en) material defines operational scenarios and requirements traceability. It supports documenting sequences, derivation and allocation, but its public terminology does not define User Journey or support a mandatory Use Case-to-Journey link. The full normative clauses are not publicly available, so this RFC makes no stronger claim about them.
- The official [ISO 9241-210:2019](https://www.iso.org/standard/77520.html) abstract defines requirements and recommendations for human-centred design activities while expressly not providing detailed coverage of particular methods and techniques. It does not prescribe journey mapping or this cardinality.
- Ivar Jacobson and Alistair Cockburn's [Use-Case Foundation](https://www.ivarjacobson.com/publications/use-case-foundation) defines a Use Case as all the ways of using a system to achieve a goal of a particular user: a whole story from its initial event to realized value or failure. Cockburn's [actor-goal and goal-level guidance](https://www.informit.com/articles/article.aspx?p=26061) permits summary-level Use Cases to contextualize lower-level goals, but presents that as a modeling technique rather than universal parentage.
- Nielsen Norman Group defines a [journey map](https://www.nngroup.com/articles/journey-mapping-101/) as a visualization of the process a person goes through to accomplish a goal, including phases, actions, thoughts and emotions. The [GOV.UK Service Manual](https://www.gov.uk/service-manual/design/scoping-your-service) likewise presents mapping the wider journey as useful when scoping one transaction. These are broader contextual views across time, channels and activities, not ownership containers for every system interaction.

The consistent distinction is that a Use Case specifies independently valuable behavior at a system boundary, while a Journey contextualizes some behaviors inside a wider actor outcome. The relationship is useful, optional and potentially many-to-many.

## Proposal

Amend the Journey and Use Case contract in `spec/artifacts.md` with the following normative text:

> A Journey MAY reference a Use Case in `steps` when that Use Case occurs on the Journey's main ordered path. A Use Case MAY be referenced by zero, one or multiple Journeys. Absence of an incoming `steps[].use-case` relationship does not make a Use Case invalid.

> An implementation MUST NOT emit a conformance diagnostic solely because an active Use Case is not referenced by a Journey. It MAY surface the absence as non-conformance advice for human review, for example to ask whether the Use Case contributes to a wider actor outcome, occurs only on a branch, or is intentionally standalone.

Retire `PRODUCT102` in `spec/validation.md`:

- remove it from the Warning codes table;
- add it to the stable list of retired codes, which are never reissued with a new meaning; and
- make no replacement diagnostic.

The canonical `Journey.steps[].use-case` relationship, its dependency polarity, the Journey schema and the Use Case schema remain unchanged. The proposal changes inverse cardinality semantics and diagnostic behavior, not serialization.

This is a **Change** RFC: it removes an existing implementation obligation and changes command results for repositories that currently produce `PRODUCT102`.

## Impact

- **On existing conformant repositories:** No artifact or configuration changes are required. Repositories containing active Use Cases with no main-path Journey reference remain conformant and stop receiving `PRODUCT102`. A repository using `warnings-as-errors` may change from failure to success when `PRODUCT102` was its only warning.
- **On existing implementations:** Implementations stop emitting `PRODUCT102` and retire the code. They may preserve the check on an audit or review surface outside the conformance diagnostic namespace. No parser, schema, graph or serialization change is required.
- **On the conformance tests:** Add a case containing an active Use Case with a valid primary actor and derived Functional Requirement but no Journey, expecting no diagnostic. The case proves the absence of `PRODUCT102`; its model should otherwise be complete enough that no unrelated warning obscures the result. Update the diagnostic coverage table to mark `PRODUCT102` retired.
- **On the reference profile:** Journey modeling remains encouraged where it explains a genuine end-to-end outcome. The proposal prevents validators from manufacturing completeness that requires semantic judgment.

## Alternatives considered

### Keep `PRODUCT102` as an unconditional warning

Rejected. It conflates “not on a structured main path” with “orphaned,” cannot represent a Use Case that occurs only in a Journey branch, and pressures authors toward false main paths, omnibus Journeys or duplicate one-step Journeys.

### Add `standalone: true` or `journey-exempt: true` to Use Cases

Rejected. This turns a semantic review question into permanent schema ceremony, adds a reverse concern to the Use Case contract and requires every intentional absence to be annotated without improving the model's truth. If omission advice later needs suppression, that belongs to the advisory surface rather than the normative artifact schema.

### Restore a repository configuration toggle

Rejected as the normative solution. Configuration cannot make the meaning of conformance diagnostics repository-specific. An implementation may offer optional, tool-specific audit policy under its extension namespace after `PRODUCT102` is retired, but that is outside this specification.

### Extend Journey steps with main, optional and branch kinds

Deferred. Richer Journey structure could be valuable, but it is a separate modeling decision and would not establish that every Use Case must occur in a Journey. This RFC removes the invalid universal inference without expanding the serialization.

### Add one-step or omnibus Journeys until every Use Case is covered

Rejected. One-step Journeys repeat a Use Case's goal and outcome, while omnibus Journeys invent an ordering among independent utilities. Both optimize for a warning count rather than accepted product meaning.
