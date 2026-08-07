---
id: FR-EVALUATE-001
type: functional-requirement
title: Report one verdict per case, with the revision it was measured at
status: active
derived-from:
  - UC-EVALUATE-001
  - BR-EXPECTATIONS-ARE-FIXED
verification:
  - id: S1
    scenario: Every case in the fixtures receives exactly one verdict, and a case that could not be run is reported as unrun rather than passed.
  - id: S2
    scenario: The report names the revision of the fixtures it was measured at.
---

## Requirement

The product MUST report exactly one verdict for each case, and MUST report the revision of the fixtures the verdicts were measured at. A case that could not be evaluated MUST be reported as unrun, with a reason, and MUST NOT be counted as passed.

## Rationale

A verdict that cannot be attributed to a revision cannot be reproduced or contested, and an unrun case counted as a pass turns absent evidence into a claim.
