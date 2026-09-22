---
id: a-resolve-project-locks-its-frame-rate-once-it-has-a-timeline
kind: verdict
conflict-key: what-happens-when-clips-of-different-frame-rates-go-through-one-project
status: live
verified-on: 2026-09-21
supersedes: []
scope: DaVinci Resolve Studio 21.1.0 driven by script; SetSettings({"timelineFrameRate": ...}) on a project that already contains at least one timeline, MacBook and Mac mini alike
evidence: project ride-0921 built at 25 fps for clip 0002, then asked for 29.97 for clip 0003 (89 source frames, 2.987 s); SetSettings reported nothing wrong, GetSettings still read 25.0, and the render came out 74 frames at 25 fps with the duration unchanged
asked-as:
  - my render came out at the wrong frame rate
  - Resolve will not change the project frame rate
  - can I put 25p and 29.97p clips through the same project
---

**A Resolve project's frame rate is settable only while the project has no timelines. After
that `SetSettings({"timelineFrameRate": ...})` is a no-op that reports nothing, and every clip
at a different rate is silently conformed.**

Measured: clip 0003 is 89 frames at 30000/1001. Rendered through a project left at 25 fps by an
earlier clip, it came out **74 frames at 25 fps** — same duration, fifteen frames of motion
dropped, no warning anywhere in the log. Only `ffprobe` on the output showed it.

**One project per frame rate**, named for the rate, and the rate is READ BACK before rendering.
`tools/remote/resolve_render.py` now exits non-zero when the project's achieved rate differs
from the requested one by more than 0.01, and names the project to use instead.

This is the same shape of failure as
[[resolve-only-reads-the-system-lut-folder-and-a-hard-kill-breaks-scripting]]: the API's return
value is not the test, the read-back is. Two silent conformances found in one day on the same
tool — **anything passed to Resolve by SetSettings or SetLUT must be read back and asserted, as
a rule, not per-field as each one burns you.**

How to spell the rate is a different question, answered by
[[resolve-ntsc-rates-compile-as-non-drop-frame-strings]].
