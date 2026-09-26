# Candidate fixture corrections from implementation qualification

The first ProductShape v0.3 qualification run exposed missing independent findings
in ten expected-result files. These corrections apply existing normative rules;
they do not change the rules or the fixture model bytes and citation pins.

- The four removal cases now retain their dangling-reference errors and also
  expect the independently computable PRODUCT029 causes required by RFC 0082.
  Removing a product-wide Constraint includes its product-scope cause.
- The empty-scope, scope-widening and governance-addition cases now include
  PRODUCT103 for the unreachable baseline Constraint. Where the proposed document
  is also unreachable, it has its own finding at its proposed source path.
- Scope-narrowing and governance-removal PRODUCT103 findings name the proposed
  document that authors the unreachable scope, rather than the baseline document.
- The rejected Business Rule-to-Use Case scope retains PRODUCT002 and also expects
  PRODUCT007: the authored reference resolves to a kind excluded by the canonical
  relationship table. Schema invalidity does not suppress that independent check.

The flat profile validates the baseline and each live change overlay. It preserves
independent findings and their actual source paths. It may combine equivalent
baseline findings repeated by overlays without erasing authored occurrences inside
one graph. That distinction also exposed an implementation aggregation defect in
the lifecycle repeated-reference case; its existing fixture expectation was correct.
