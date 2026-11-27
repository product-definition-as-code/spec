# Product-to-implementation correspondence

Snapshot boundary: the documentary findings and execution-status statements below describe the original phase-one report revision. Subsequent authorized [executable exploration](../experiments/README.md) and independent review are tracked separately; unavailable cost/token metering is not a current prerequisite. No historical result is silently upgraded.

Issue: [#125](https://github.com/product-definition-as-code/spec/issues/125). Retrieved 2026-11-27. Status: documentary bridge design; independent review pending. [Proposal](../../v0.4.0-formal-product-definition.md) H0/H1/H4 remain untested. No compiler, prover or implementation bridge was run.

## Available mechanisms and limits

| Primary source / inspected version | Published mechanism | Boundary relevant to PDaC |
| --- | --- | --- |
| [Dafny overview](https://dafny.org/) and [reference manual](https://dafny.org/latest/DafnyRef/DafnyRef), live latest-release snapshot; specifications, framing and assume statements | Language-integrated specifications, static verification and compilation to several implementation environments; pre/postconditions, invariants and frame specifications. | Proof obligations depend on the specified heap/effects and assumptions. Compilation and external calls need their own correspondence/trust account; availability of a target is not proof that the deployed path uses verified code. |
| [Verus guide](https://verus-lang.github.io/verus/guide/), live overview | Rust specifications/proofs and static functional verification using SMT reasoning; Rust's ownership/type system handles important aliasing obligations. | The guide excludes full Rust/library coverage and verification of the verifier or Rust/LLVM compiler. Unsupported language features must be recorded, not replaced by a weaker product promise. |
| [F* project](https://fstar-lang.org/) and [Proof-Oriented Programming introduction](https://fstar-lang.org/tutorial/book/intro.html), live documentation | Dependent/refinement types, checked proofs and extraction connect functional specifications to executable programs. | The project explicitly distinguishes a proof of a model from verification of the original implementation. Extraction, runtime and foreign components must be identified for the selected experiment. |

These describe capabilities, not a comparative ranking, pinned tool installation or reproduced soundness result. Do not choose a product notation or backend from homepage examples. Toolchain versions, supported fragments, distribution licences and platform feasibility must be checked before an approved bridge run.

## Proposed bridge contract for phase 3

A small approved booking operation or authorization decision is sufficient to test correspondence. This is a candidate experimental shape, not an implementation commitment:

1. Name the accepted property, product revision and owner-approved meaning, including units, identity assumptions, error outcomes and deliberately informal requirements.
2. State an abstraction relation between product state and code representation. Explain what is lost: for example, mathematical capacity versus machine integers, or an external identity claim versus a local principal.
3. Map the operation to executable pre/postconditions, invariants and frame/effect obligations. Distinguish safety, termination, latency and environmental guarantees; proving one does not imply the others.
4. Identify every assumed function, axiom, unverified module, verifier/solver, compiler/extraction step, library, FFI and external service. Review ownership of each assumption. Tests support trusted components without turning them into proved code.
5. Build/check the actual bridge artifact and demonstrate that the exercised entry point routes through the verified code. Record code/model/toolchain digests and exact proof/test commands; a duplicate demonstration function is insufficient.
6. Apply a permitted intent change in a fresh agent session. Measure semantic drift, proof/contract maintenance, reconstruction and human review cost against the equivalent non-PDaC formal workflow.

All steps require the later G2 authorization. Phase-2 product-model consistency/adequacy/evolution results cannot satisfy steps 2–5 or establish an implementation proof.

## Falsifiers and authority

**Proposed H4 observations:** silent strengthening/weakening during translation; a proved helper bypassed at runtime; hidden assumptions; disagreement about what a formal contract authorizes; maintenance cost that erases any H0 advantage. A failed proof attempt can reflect a correctable encoding defect, unsupported fragment or genuinely false property; retain the attempt and classify it before interpreting it.

Keep approved prose/derived formulas, selected canonical formal properties and explicitly mixed authority open. A generated contract cannot settle an unresolved business decision. Existing external verification workflows may already provide adequate traceability and maintenance; native PDaC semantics requires additional evidence, not a successful bridge alone.

## Reproduction and next action

Review the cited manual sections and proposed mapping with product and formal-methods expertise. No illustrative encoding is represented as checked. A future run must preserve source/intent/dependency revisions, assumptions, tools/configuration, executable entry point, commands, raw results, proof artifacts, limits and all failed attempts. Independent review, installation feasibility, actual proof cost and runtime correspondence are pending. Token/spend and human-attention metering are unavailable; no delegated agents or execution jobs occurred. Carry the bridge checklist and H4 boundary to synthesis/G1; do not claim evaluated phase-3 correspondence from an exploratory contract toy.
