---
id: test-graph-setlut-nodeindex-path-with-a-dctl-pat
kind: open
conflict-key: should-we-test-graph-setlut-nodeindex-path-with-a-dctl-pat
status: live
supersedes: []
proven: false
verified-on: 2026-09-22
asked-as:
  - Test Graph.SetLUT(nodeIndex, path) with a .dctl path on a colour node
  - test graph setlut nodeindex path with a dctl pat
---

**This is a PLAN, not a finding. `proven: false`. Do not build against it.**

## Test Graph.SetLUT(nodeIndex, path) with a .dctl path on a colour node

**Why it matters:** the only route that would put a DCTL on the Color page by script is unverified; .cube via SetLUT is doc-verified and the Fusion DCTL OFX is proven, so the pipeline is not blocked, but the report's boundary table carries an UNVERIFIED cell until this one-liner runs with Resolve open (docs/PLUGIN-ECOSYSTEM-2026-09-22.md §1)

Bookmarked 2026-09-22 at the moment of deferral, because the record of a deferral is what fails, not the decision to defer.
