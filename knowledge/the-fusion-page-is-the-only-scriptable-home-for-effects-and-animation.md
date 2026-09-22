---
id: the-fusion-page-is-the-only-scriptable-home-for-effects-and-animation
kind: verdict
conflict-key: which-resolve-surfaces-can-a-script-place-effects-and-animation-on
status: live
supersedes: []
verified-on: 2026-09-22
scope: the DaVinciResolveScript.pyi shipped with Resolve 21.1.0 (dated 2026-09-07) and its CHANGELOG, read on this MacBook; the v21.0.4 API doc mirror; grep for keyframe, AddNode, OFX in the stub. Says what the API exposes, not what a Workflow Integration panel or UI scripting could reach
evidence: docs/PLUGIN-ECOSYSTEM-2026-09-22.md §1 (the boundary table); docs/research-raw/plugins-2026-09-22/motion.md §0 and ofx-ai.md §6 (the grep results and API names)
asked-as:
  - can a script add an OFX to a colour node
  - can the Resolve API keyframe a clip on the edit page
  - which effects can the pipeline place without a click
  - is this plugin scriptable in Resolve
  - how do I place a transition or title by script
---

**Effects and animation are scriptable on the Fusion page and nowhere else; the
Edit and Color pages accept only whole templates by name.** Read from the 21.1
stub:

| you want | the API has | so |
|---|---|---|
| an OFX filter on a clip | `comp.AddTool("ofx.<id>")` inside `AddFusionComp()` / `GetFusionCompByIndex()` | Fusion only |
| an OFX node on the Color page | nothing — no `AddNode`, no OFX parameter read or write | GUI only; `ApplyGradeFromDRX(path)` replays a saved tree, and the `.drx` must have been saved where that plugin was installed |
| a LUT on a colour node | `Graph.SetLUT(nodeIndex, path)` for `.cube`; `.dctl` path untested | yes |
| a title, generator, effect template | `InsertFusionTitleIntoTimeline(name)`, `InsertFusionGeneratorIntoTimeline`, `InsertOFXGeneratorIntoTimeline` | yes, by Effects-Library name |
| a transition | `TimelineItem.AddTransition({type, category, position, alignment, duration})` | yes, 21.1 and later only |
| keyframes or retime curves on an Edit-page clip | nothing — `grep -i keyframe` finds only Color dynamics and import options; `SetProperty("Speed")` is a constant | GUI only; animate in a Fusion comp or a template |
| a Fairlight FX | nothing | GUI only |

Consequences already acted on: `dctl_film_mini.py` builds its chains in a Fusion
comp; any plugin bought "for the pipeline" must register in Fusion, checked by the
registry dump ([[an-ofx-tool-id-in-fusion-is-ofx-dot-plus-its-plugin-identifier]])
before money moves; a `.drfx` pack is placeable by name, a `.drp` template project
is not.
