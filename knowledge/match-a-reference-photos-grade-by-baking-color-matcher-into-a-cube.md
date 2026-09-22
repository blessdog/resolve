---
id: match-a-reference-photos-grade-by-baking-color-matcher-into-a-cube
kind: procedure
conflict-key: how-to-match-a-grade-from-a-reference-photo
status: live
supersedes: []
verified-on: 2026-09-22
applies-when: Ryan supplies a photo whose colour he likes and wants footage graded to match it
not-when: the reference is another CLIP in the same project; Resolve's own Shot Match handles that in the colour page with no LUT
route: FIRST render an UNGRADED still of the clip out of Resolve (resolve_render.py --still-at S with no --lut) and use THAT as the source frame, never an ffmpeg decode. Then .venv-colour/bin/python jobs/film-look-mini/match_reference.py <reference.jpg> <resolve-still.jpg> <out.cube> --method <the one whose residual is smallest> --strength 1.0, read the printed affine residual and reject any method above ~2 codes, copy the .cube under Resolve's LUT folder film-look/matched/, RESTART Resolve so it sees the new LUT, and apply with NodeGraph.SetLUT(1, "film-look/matched/<name>.cube")
sibling: the-osmo-film-chain-balance-then-cdl-in-log-then-a-print-lut
asked-as:
  - can you match the colour grading from a photo I like
  - grade my footage to look like this reference image
  - how do I copy a look from a still into Resolve
  - colour transfer from a reference photo
---

**Yes, and it needs no plugin. `color-matcher` computes the transfer, this repo bakes the
fitted transform into a 33^3 .cube, and Resolve applies it on colour node 1.**

**AMENDED 2026-09-22, and the amendment is the whole ballgame: the source frame must come
OUT OF RESOLVE, not out of ffmpeg.** The .cube is fitted to map source pixels to reference
pixels, so it is only correct on the value range it was fitted on -- and Resolve's managed
input transform means the node receives different numbers than ffmpeg's rgb24 decode of the
same frame. Measured on one frame of clip 0002:

| | R | G | B | p1 | midtone |
|---|---|---|---|---|---|
| ffmpeg decode | 55.5 | 75.5 | 99.8 | 20.5 | 62.0 |
| Resolve still | 80.5 | 98.7 | 120.8 | 47.6 | 86.7 |

Fitted on the ffmpeg frame, the LUT overshot badly in Resolve: target midtone 42, delivered
71 to 101, with the road blown out and the trees posterised acid yellow. Refitted on the
Resolve still, the same method landed at RGB 63/49/71 against the reference's 62/49/66 with
blacks at 1. Same reference, same method, same clip -- only the fitting domain changed.

This is the same mechanism as
[[applying-a-cube-offline-does-not-predict-what-resolve-renders]], hitting from the other
direction: there it made a PREDICTION wrong, here it makes the ARTEFACT wrong.

**Choose the method by its printed residual, not by what worked last time.** The residual is
how far the baked lattice is from the library's own result, and it is reference-dependent:

| reference | mkl | reinhard | hm-mkl-hm |
|---|---|---|---|
| warm fashion photo (2026-09-19) | -- | -- | used, worked |
| dark studio podcast (2026-09-22) | **1.9 codes** | 12.9 | 15.7 |

Above roughly 2 codes the transform is not affine, the tool falls back to per-channel curves,
and the result shows it -- the 15.7-code bake came out magenta with a yellow building. Anything
that crushes blacks or is lit very differently from the footage will be non-affine, so a
crushed-black interior matched onto an outdoor dusk ride wants MKL.

PRIOR ART, searched 2026-09-19 before writing anything: `color-matcher` (hahnec, PyPI 0.6.0)
implements Reinhard 2001, Pitie's Monge-Kantorovich linear transform, histogram matching and
the combined `hm-mkl-hm`. Also found and NOT needed: ColorCast (PyPI), the REFGRADE Resolve
panel (github Aasishmuchala/DavinciPlugin), Resolve's own Shot Match (clip-to-clip only, not
scriptable to a still). Installed into `.venv-colour` because macOS system Python refuses
pip (PEP 668).

**The one thing the library does not do is produce a LUT** — it maps one image to another,
while a film needs the same map on every frame. `match_reference.py` runs the library on a
representative frame, then recovers the fitted transform by least squares (MKL and Reinhard
are affine in RGB, so a 3x4 solve is exact) and applies it to an identity lattice. It prints
the residual; `mkl` came back at 2.32 display codes, and the non-affine methods fall back to
per-channel curves fitted from the same result.

Measured on Osmo clip 0002 at 60 s against a warm fashion-show photo, channel means R/G/B:

| | colour | blacks | whites | RGB |
|---|---|---|---|---|
| the reference photo | 41.6% | 12 | 239 | 102, 86, 67 |
| footage as shot | 26.6% | 28 | 255 | 105, 121, 135 |
| hm-mkl-hm, full | 58.0% | 22 | 229 | 100, 74, 42 |
| **hm-mkl-hm, 0.75** | **36.4%** | 31 | 233 | **100, 84, 63** |
| hm-mkl-hm, 0.50 | 19.2% | 40 | 236 | 100, 95, 83 |
| mkl only | 39.9% | 23 | 222 | 92, 80, 59 |

0.75 strength lands within 4 codes of the reference on every channel. **Full strength
overshoots** because a statistical match copies the reference's CONTENT as well as its grade:
that photo is mostly cream fabric and skin, so a full match drags a green garden toward those
means. `--strength` is the control for that and 0.7 to 0.8 is the useful range.

Evidence: `jobs/film-look-mini/evidence/2026-09-19-osmo-0002-matched-to-reference-photo.jpg`.
Reference kept at `jobs/film-look-mini/reference-fashion-warm.jpg`, LUTs at
`grades/film-look/assets/matched/`.
