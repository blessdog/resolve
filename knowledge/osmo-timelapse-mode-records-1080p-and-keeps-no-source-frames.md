---
id: osmo-timelapse-mode-records-1080p-and-keeps-no-source-frames
kind: verdict
conflict-key: what-does-osmo-timelapse-mode-actually-record
status: live
supersedes: []
verified-on: 2026-09-21
scope: DJI Osmo Action 5 Pro in timelapse mode, clips DJI_20260919190029_0002_D and DJI_20260919191044_0003_D shot at dusk on 2026-09-19 (19:00 and 19:10) on a bike; read with ffprobe and exiftool from the copies in outputs/osmo/2026-09-19-timelapse/
evidence: jobs/film-look-mini/evidence/2026-09-19-osmo-timelapse-what-you-got.jpg (four frames from each clip); graded renders in outputs/osmo/2026-09-19-timelapse/graded/ (gitignored)
asked-as:
  - what resolution does Osmo timelapse record
  - can I get 4K out of a timelapse clip
  - the camera was on timelapse by mistake, what did I lose
  - why is the timelapse footage smeared at the edges
---

**Timelapse records 1920x1080, not 4K, and the card keeps only the finished video.
There are no source frames to re-render from, so the resolution is unrecoverable.**

| | clip 0002 | clip 0003 |
|---|---|---|
| resolution | 1920x1080 | 1920x1080 |
| duration | 10.04 s | 8.91 s |
| frames | 301 | 267 |
| rate | 29.97 | 29.97 |
| size | 87.5 MB | 66.5 MB |
| audio | none | none |

A quarter of the pixels of the camera's normal 3840x2160, and nothing on the card but the
MP4 and its LRF proxy: no JPG sequence, no RAW frames. Compare
[[render-4k-footage-at-4k]] and [[osmo-dusk-clip-0014-is-4k-pixels-with-less-than-1080p-detail]].

Second cost, from the same files: shutter ran 1/40 to 1/120 (most common 1/40 and 1/50) with
the pattern-read ISO field at 1600, in dusk light. Those long exposures are why the frame
edges smear. On a moving bike that reads as speed streaks rather than as a defect, which is
the agent's reading and not Ryan's verdict.

The material itself is the best-looking Osmo footage so far: sunset cloud structure across
both clips, and a wet street under a warm streetlight at 6 s of clip 0003. Both graded with
the reference-photo LUT ([[match-a-reference-photos-grade-by-baking-color-matcher-into-a-cube]])
at 0.75 strength, 4 s and 2 s to render at 1080p.

Offload: all three clips verified by sha256 against Ryan's copy at
`~/Desktop/osmo_action/DCIM/DJI_001/` on 2026-09-21. The camera volume unmounted mid-session,
so the first verification attempt compared two empty hash strings and PASSED — a false green.
Compare a hash only after asserting it is non-empty ([[a-copy-tools-exit-code-is-not-proof-of-a-move]]).
