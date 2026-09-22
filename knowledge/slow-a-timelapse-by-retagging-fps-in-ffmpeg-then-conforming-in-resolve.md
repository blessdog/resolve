---
id: slow-a-timelapse-by-retagging-fps-in-ffmpeg-then-conforming-in-resolve
kind: procedure
conflict-key: how-to-slow-a-clip-down-in-resolve-by-script
status: live
supersedes: []
verified-on: 2026-09-21
applies-when: a clip must be slowed and rendered without anyone dragging a speed handle in Resolve's UI
not-when: the slowdown is a ramp rather than a constant rate; retime curves are not in the scripting API at all
route: ffmpeg demux to a raw elementary stream and remux at the lower rate (lossless), then import to a 29.97 timeline and let Resolve conform it up with TimelineItem.SetProperty("RetimeProcess", 3) and ("MotionEstimation", 5). ffmpeg -i in.mp4 -map 0:v:0 -c copy -bsf:v hevc_mp4toannexb -f hevc raw.h265 ; ffmpeg -fflags +genpts -r 15 -i raw.h265 -c copy out.mp4
sibling: none
asked-as:
  - how do I slow down a clip by script in Resolve
  - SetSpeed does not change the clip length
  - slow motion from a timelapse
  - frame interpolation for a slowed clip
---

**`SetSpeed` works but does not lengthen the timeline item, and frame-rate conform is
refused by script. Retag the frame rate in ffmpeg first, then let Resolve interpolate.**

Measured 2026-09-21 on the Osmo timelapse clips:

- `TimelineItem.SetSpeed(50)`, `(0.5)`, `("50")` all return False. Only
  `SetSpeed({"Percentage": 50})` returns True, and the item's duration stays at the original
  frame count, so it plays the first half of the source slowed rather than the whole clip.
- `MediaPoolItem.SetClipProperty("Video Frame Rate", "15")` returns False for every value.
- `SetProperty("RetimeProcess", n)` accepts 0-3 (project / nearest / frame blend / optical
  flow); 4 is refused. `SetProperty("MotionEstimation", n)` accepts 0-7, which is where
  Speed Warp lives.
- `-r` before `-i` with `-c copy` does NOT retime an mp4; the original timebase survives.
  Going out to a raw elementary stream and back does, with no re-encode.

Render cost at 1080p on the MacBook, clip 0003 (267 frames):

| output | length | retime | time |
|---|---|---|---|
| 2x | 17.8 s | optical flow + Speed Warp | 482 s |
| 4x | 35.6 s | optical flow + Speed Warp | ~480 s |
| 2x | 17.8 s | frame blend | **4 s** |

Frame blend is two orders of magnitude cheaper. Whether Speed Warp is worth it on THIS
material is Ryan's eyes: timelapse frames carry large inter-frame motion and 1/40-shutter
blur, which is the hard case for optical flow.

Related: [[osmo-timelapse-mode-records-1080p-and-keeps-no-source-frames]].
