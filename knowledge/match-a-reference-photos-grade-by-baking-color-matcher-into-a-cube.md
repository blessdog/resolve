---
id: match-a-reference-photos-grade-by-baking-color-matcher-into-a-cube
kind: procedure
conflict-key: how-to-match-a-grade-from-a-reference-photo
status: live
supersedes: []
verified-on: 2026-09-19
applies-when: Ryan supplies a photo whose colour he likes and wants footage graded to match it
not-when: the reference is another CLIP in the same project; Resolve's own Shot Match handles that in the colour page with no LUT
route: .venv-colour/bin/python jobs/film-look-mini/match_reference.py <reference.jpg> <source-frame.png> <out.cube> --method hm-mkl-hm --strength 0.75, then copy the .cube under Resolve's LUT folder film-look/matched/ and apply it with NodeGraph.SetLUT(1, "film-look/matched/<name>.cube")
sibling: the-osmo-film-chain-balance-then-cdl-in-log-then-a-print-lut
asked-as:
  - can you match the colour grading from a photo I like
  - grade my footage to look like this reference image
  - how do I copy a look from a still into Resolve
  - colour transfer from a reference photo
---

**Yes, and it needs no plugin. `color-matcher` computes the transfer, this repo bakes the
fitted transform into a 33^3 .cube, and Resolve applies it on colour node 1.**

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
