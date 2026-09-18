---
id: film-look-creator-on-osmo-clip-0014-blows-the-sky-and-breaks-on-a-dwg-timeline
kind: verdict
conflict-key: how-does-film-look-creator-behave-on-osmo-d-log-m-footage-by-script
status: live
supersedes: []
verified-on: 2026-09-17
scope: DJI Osmo Action 5 Pro clip DJI_20260917182112_0014_D (25 min bike ride at dusk, 4K 29.97 D-Log M, auto exposure, field 3-2-3-1 mostly 3200 with 6400 stretches, shutter 1/330 to 1/500), 20 s window 740-760 s and the 750 s frame, Resolve Studio 21.1 on the MacBook through jobs/film-look-mini/dctl_film_mini.py; Ryan's verdict on the look is PENDING
evidence: jobs/film-look-mini/evidence/2026-09-17-osmo-dji-0014-film-look-creator-taste-sheet.jpg; renders in outputs/osmo/2026-09-17-clip-0014/taste/ and taste-dwg/ (gitignored); logs taste.log, taste-di.log, taste-dwg.log beside them
asked-as:
  - does Film Look Creator work on the Osmo footage
  - why does the sky blow out through Film Look Creator
  - white blocks in the Film Look Creator render
  - how long does Film Look Creator take at 4K
---

**Film Look Creator runs by script after the D-Log M DCTL on the Rec.709 / Linear timeline and renders 20 s of
4K in 80 to 88 s, but it blows a dusk sky to white that DJI's own LUT holds. On a DaVinci WG / Intermediate
timeline with DaVinci tone mapping it renders corrupted frames: white rectangles and black blobs over the sky.**

The 750 s frame, luma darkest 1% / brightest 1% / pixels with a channel at 255:

| chain | dark | bright | at 255 |
|---|---|---|---|
| as shot (log) | 108 | 246 | 1.02% |
| DJI's D-Log M LUT (ffmpeg lut3d) | 14 | 237 | 1.49% |
| Thatcher conversion, linear, no tone curve | 54 | 255 | 24.07% |
| FLC 'Cinematic' preset, linear timeline, fed linear Rec.709 | 0 | 254 | 12.90% |
| FLC Default65 restrained, linear timeline | 44 | 254 | 22.40% |
| same two, FLC told it was fed DWG / Intermediate (input dji-action5-dlogm-di) | 0 / 44 | 255 | 13.12% / 23.77% |
| `--timeline dwg`, DaVinci tone mapping, conversion only | 57 | 255 | 26.60% |
| `--timeline dwg`, FLC either recipe | 0 | 255 | 17% and CORRUPT |

So the clipping is upstream of Film Look Creator and independent of the space it is told it receives: the Thatcher
DCTL puts this sky far above display white, nothing in either chain rolls it off, and DaVinci tone mapping on the
SDR output did not fold it either. Measured on project osmo-0014-dwg: timelineWorkingLuminanceMode 'HDR 1000',
timelineWorkingLuminance 1000, colorSpaceOutputToneLuminanceMax 100, so the mapping was 1000 to 100 nits and the sky
still clipped; why is OPEN. DJI's LUT
has a roll-off built in. The corrupted DWG frames (white blocks of tile size, the shape of a bloom or halation pass
meeting out-of-range values) are the agent's reading, not measured; the mechanism is OPEN. Renders match their
stills within 0.8 to 1.8 codes mean, so the renders are what the stills show.

Recipes `flc-cinematic`, `flc-documentary` (and their `-di`, `-dwg` twins) are in `dctl-film-recipes.json`;
the restrained numbers (contrast 1.15, halation 0.1, bloom 0.1, grain 0.08, flicker and gate weave off) are CHOSEN
from Ryan's 2026-09-17 note, not measured. The 'Cinematic' preset ships with a 2.4:1 film gate, which is why that
panel is letterboxed. The camera conversion alone at 4K took 14 to 20 s per 20 s of picture.

Not yet tried: a highlight roll-off ahead of FLC (Resolve's own D-Log M is missing, DJI's LUT is display-referred so
FLC would have to follow it in the colour page, not the comp); FLC `colorExposure` down; the print LUTs.
Related: [[the-approved-film-look-fails-on-osmo-clip-0004]], [[compare-other-free-film-emulators-on-osmo-d-log-]],
[[osmo-d-log-m-into-resolve-goes-through-the-idt-dctl]], [[film-look-creator-renders-on-the-mini-through-a-fusion-comp]].
