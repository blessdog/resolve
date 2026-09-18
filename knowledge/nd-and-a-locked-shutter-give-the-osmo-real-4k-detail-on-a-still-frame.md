---
id: nd-and-a-locked-shutter-give-the-osmo-real-4k-detail-on-a-still-frame
kind: verdict
conflict-key: does-the-osmo-record-real-4k-detail-with-nd-and-a-locked-shutter
status: live
supersedes: []
verified-on: 2026-09-18
scope: DJI Osmo Action 5 Pro clip DJI_20260918143132_0002_D (2026-09-18 14:31, 4K 25p, 1/50 s throughout, ISO field 100 to 800 with ND filters, 10-bit, handheld walking through the shed and yard, 160 s), frames at 20 / 80 / 126 / 130 / 134 / 140 s; compared with clip 0006 (this morning, auto, 1/500) and clips 0001 and 0014
evidence: jobs/film-look-mini/evidence/2026-09-18-osmo-dji-0002-nd-locked-shutter-100pct-crops.jpg
asked-as:
  - did the ND filters and locked shutter fix the soft Osmo footage
  - does the camera record real 4K detail now
  - why are some frames sharp and others blurred with the ND on
---

**With ND and the shutter locked at 1/50, a frame where the camera is still carries real 4K detail: sharpness
183 and a 1080p round trip changes it by 2.21 codes, the best of any frame measured on this camera (the daylight
reference was 136 and 1.50). Frames where the camera moves are blurred by the 1/50 shutter itself, which is the
motion blur a film camera would give and not a defect.**

| frame | sharpness | 1080p round trip |
|---|---|---|
| 0002 at 126 s, still | 182.9 | 2.21 codes |
| 0002 at 134 s, nearly still | 90.5 | 1.22 |
| 0002 at 140 s | 77.5 | 1.04 |
| 0002 at 20 / 80 / 130 s, camera moving by hand | 18.2 / 15.4 / 26.0 | 0.43 / 0.49 / 0.62 |
| 0006 this morning, street ride at 1/500 | 102 | 0.91 |
| 0001 daylight reference at 1/2000 | 136 | 1.50 |
| 0014 last night, dusk | 13 | 0.38 |

So the sensor and the encoder were never the limit; the exposure was. At 1/50 the camera has to be steadier
than at 1/500 for a frame to be sharp, and a fast handheld swing blurs every frame. This clip is a handheld walk
with big deliberate moves (frame-to-frame motion 5 to 16 px, residual shake 4 to 42 px), so it says nothing
about RockSteady; that test is still the same road ridden twice.

Related: [[osmo-auto-exposure-picks-fast-shutters-and-high-iso-lock-the-shutter]],
[[osmo-dusk-clip-0014-is-4k-pixels-with-less-than-1080p-detail]], [[reshoot-the-osmo-test-with-nd-filters-arriving-2]].
