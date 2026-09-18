---
id: osmo-dusk-clip-0014-is-4k-pixels-with-less-than-1080p-detail
kind: verdict
conflict-key: why-does-the-4k-osmo-footage-not-look-4k
status: live
supersedes: []
verified-on: 2026-09-17
scope: DJI Osmo Action 5 Pro clip DJI_20260917182112_0014_D (dusk bike ride, 18:21 on 2026-09-17, D-Log M 4K 29.97 at 91 Mbps, auto exposure, the pattern-read field mostly 3200 with 6400 stretches, shutter 1/330 to 1/500) against clip DJI_20260916114233_0001_D (daylight, 1/2000 s, field near 240); frames at 750 and 300 s of 0014 and 60 s of 0001, and the FLC restrained render of 0014 at 750 s
evidence: jobs/film-look-mini/evidence/2026-09-17-osmo-dji-0014-4k-pixels-1080p-detail-crops.jpg (100% crops, each beside its own 1080p round trip)
asked-as:
  - the 4K Osmo footage does not look 4K, it looks soft and smeared
  - why is the Osmo video soft even though the files are huge
  - is the render losing resolution
  - does the DJI 4K carry real 4K detail
---

**The file is 3840x2160 and the render is 3840x2160, but the dusk clip carries less than 1080p of detail
as shot. The render did not lose anything; the camera never recorded it.**

The test (null before the metric): shrink a frame to 1080p and back to 4K, and measure what changed. A frame
with real 4K detail changes; a frame with none comes back the same.

| frame | Laplacian sharpness | changed by a 1080p round trip | by a 540p round trip |
|---|---|---|---|
| clip 0001 (daylight, 1/2000 s), 60 s | 135.7 | 1.50 codes | 4.14 codes |
| clip 0014 (dusk), 750 s, as shot | 13.0 | 0.38 codes | 0.90 codes |
| clip 0014, 300 s, as shot | 19.2 | 0.49 | 1.22 |
| clip 0014 render, FLC restrained, 750 s | 22.1 | 0.50 | 1.14 |

Clip 0014 is ten times softer than the daylight clip and survives even a 540p round trip almost unchanged.
The render is slightly sharper than its source (Film Look Creator's grain), so the pipeline is not the loss.
Both clips were written at the same 91 Mbps; at dusk the bits encode noise and smear, not detail.

Mechanism, the agent's reading and not measured separately: auto exposure at about ISO 3200 to 6400 makes the
camera's noise reduction smear texture, the ride adds motion blur, and RockSteady (whether it was on is not
in the file's metadata) crops and rescales. The cure is in the camera, not in Resolve: the settings list in
grades/film-look/README.md (ISO ceiling 1600, 24p at 1/48 with ND, sharpness and in-camera NR at minimum,
RockSteady off or a slow shutter but not both). Denoising after the fact recovers nothing that was never recorded
([[denoise-high-iso-osmo-footage-with-resolve-s-noi]]).

Related: [[osmo-clip-0004-was-shot-at-about-iso-3200]], [[render-4k-footage-at-4k]],
[[reshoot-the-osmo-test-with-nd-filters-arriving-2]], [[film-look-creator-on-osmo-clip-0014-blows-the-sky-and-breaks-on-a-dwg-timeline]].
