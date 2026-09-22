---
id: applying-a-cube-offline-does-not-predict-what-resolve-renders
kind: refuted
conflict-key: can-a-grade-be-solved-offline-instead-of-rendering-stills
status: live
supersedes: []
verified-on: 2026-09-21
mechanism: the .cube on a colour node does not receive the file's code values; Resolve's managed input transform runs first (clip space -> timeline Rec.709 / Gamma 2.4), and ffmpeg's rgb24 decode of limited-range YUV is a third encoding again. Reading the file with ffmpeg and applying the cube models neither.
asked-as:
  - can I solve a LUT grade in numpy instead of rendering
  - why does my offline LUT preview not match Resolve
  - how do I find the right exposure lift without rendering
---

**Applying a `.cube` to an ffmpeg-decoded frame does NOT predict Resolve's output. Measured on
three clips it was 1.6x too dark on the midtone, every time. Solve exposure with real Resolve
STILLS, which cost about 3 seconds each.**

| clip | source p50 | offline prediction | what Resolve rendered |
|---|---|---|---|
| 0002 | 60.1 | 23.5 | **38.1** |
| 0004 | 52.1 | 18.0 | **31.3** |
| 0005 | 44.3 | 16.3 | **28.0** |

The error is consistent in direction and rough magnitude, so the offline path is fine for
answering *"does this LUT darken or lighten, and does anything clip?"* — it correctly showed the
cube darkens midtones and clips nothing. It is useless for choosing a NUMBER. Exposure lifts
solved against it (1.16 and 1.38) were roughly double the ones real stills gave (1.08 and 1.16).

The near-miss worth remembering: this was on the way to writing an offline solver as a repo
tool, and only a control against the actual render stopped it. **Build the control before
believing the number** — the offline figures were plausible, self-consistent and wrong.

`colour-science` is still the right library for reading a cube (`read_LUT`, `LUT3D.apply`,
`table_interpolation_tetrahedral`, which is the interpolation Resolve uses) and is now pinned
in `requirements-colour.txt`. Do not hand-roll trilinear interpolation. The library was never
the problem; the pipeline it was fed was.

Related: [[a-reference-matched-lut-already-carries-the-white-balance]].
