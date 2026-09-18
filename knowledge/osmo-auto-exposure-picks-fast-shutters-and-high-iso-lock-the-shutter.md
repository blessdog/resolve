---
id: osmo-auto-exposure-picks-fast-shutters-and-high-iso-lock-the-shutter
kind: verdict
conflict-key: what-exposure-does-the-osmo-choose-on-auto-and-what-to-lock
status: live
supersedes: []
verified-on: 2026-09-18
scope: DJI Osmo Action 5 Pro on auto exposure, three clips read through the pattern field Dvtm_ac204_3-2-3-1 (ISO by pattern, unverified against the camera's own display) and ShutterSpeed, 4K 29.97 at about 90 Mbps; clip DJI_20260918091439_0006_D (2026-09-18 09:14, 10-bit Normal, not log, shed then street ride), DJI_20260917182112_0014_D (dusk ride) and DJI_20260916114233_0001_D (daylight)
evidence: jobs/film-look-mini/evidence/2026-09-18-osmo-dji-0006-normal-10bit-100pct-crops.jpg (100% crops with sharpness and 1080p-round-trip numbers in the labels)
asked-as:
  - what settings should the Osmo use
  - why is the ISO so high on the Osmo in daylight
  - is the stabilisation working on the Osmo test clip
  - how sharp is the new Osmo test footage
---

**On auto, the camera spends light on a fast shutter and buys it back with ISO: 1/500 s at ISO 800 to 3200 on a
sunny morning street. Lock the shutter (1/60 at 29.97, 1/48 at 24) and the ISO falls about eight times. Indoors in
the shed it ran ISO 12800 to 25600 and there is nothing to lock; that room needs light.**

Clip 0006 by 100 s bins (most common ISO field value, most common shutter):

| section | ISO field | shutter |
|---|---|---|
| 0 to 400 s, inside the shed | 7816 to 25600 | 1/110, 1/31 |
| 400 to 787 s, street ride, morning sun | 800 to 3200 | 1/500, 1/220 |

Detail (Laplacian sharpness, and how much a 1080p round trip changes the frame; both higher is more real 4K):

| frame | sharpness | 1080p round trip |
|---|---|---|
| clip 0001 daylight, 1/2000 s (reference best) | 136 | 1.50 codes |
| clip 0006 at 600 s, street ride | 102 | 0.91 |
| clip 0006 at 300 s, shed doorway | 57 | 0.73 |
| clip 0006 at 30 s, inside the shed | 30 | 0.60 |
| clip 0014 at 750 s, dusk ride | 13 | 0.38 |

Shake, RMS deviation of the frame from its half-second-smoothed path in 4K pixels, 2 s windows: today's ride
0.5 to 3.2 px (six windows), last night's 1.8 to 10.4 px (five). Today is steadier, but this measure cannot say
whether that is RockSteady, the lower frame mount, the road or the light; only the same ride shot with RockSteady
on and off can. Whether RockSteady was on is not in the file's metadata.

Related: [[osmo-dusk-clip-0014-is-4k-pixels-with-less-than-1080p-detail]],
[[osmo-clip-0004-was-shot-at-about-iso-3200]], [[reshoot-the-osmo-test-with-nd-filters-arriving-2]].
