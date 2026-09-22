---
id: the-mac-mini-has-resolve-studio-and-renders-over-ssh
kind: verdict
conflict-key: can-the-mac-mini-render-with-resolve
status: live
supersedes: []
verified-on: 2026-09-21
scope: Ryans-Mac-mini.local (ssh host `mini`), macOS 26.4.1, M1, 8 GB RAM, 29 GB free of 228 GB, DaVinci Resolve Studio 21.1.0.14 — the same build as the MacBook; measured by launching Resolve over ssh and driving it with DaVinciResolveScript
evidence: `ssh mini` probe returning app True, page 'media', version 21.1.0.14; a 4x Speed Warp render of clip0003 driven entirely over ssh from ~/render/mini_render.py
asked-as:
  - can the Mac mini render with Resolve
  - does the mini have Resolve installed
  - how do I offload a render to the mini
  - render on the second machine
---

**The mini has Resolve Studio and is scriptable over ssh. `AGENTS.md` still says it does
not, which is stale and has been wrong since at least 2026-09-12.**

Route, proven end to end 2026-09-21: `ssh mini 'open -a "DaVinci Resolve"'`, wait about 25 s,
then run a plain script with `/usr/bin/python3` over ssh; `dvr.scriptapp("Resolve")` answers
and `GetCurrentPage()` returns a page name. Media and LUTs must be pushed first —
`rsync` the clip to `~/render/`, and the matched LUTs into
`$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/LUT/film-look/matched/`,
which needs no admin password (the system-wide `/Library/...` path does).

**Two hard limits.** 8 GB of RAM against the MacBook's 16, and **29 GB of free disk**: the
4K Osmo clips are 17 GB each, so a 4K source plus its render does not fit. 1080p and
timelapse work fits comfortably. `[[resolve-21-1-installer-needs-14-gb-on-the-startup-disk]]`
is the related disk trap.

AGENTS.md row for `tools/render-ir.py --on mini` still reads "the mini (8 GB, 7 GB disk free)
has no Resolve" and also claims Resolve Remote Rendering was measured out for that reason.
The disk figure and the no-Resolve claim are both wrong now; whether Remote Rendering itself
works has NOT been re-measured.

Related: [[the-mini-renders-the-story-ir-with-ffmpeg-not-resolve]],
[[film-look-creator-renders-on-the-mini-through-a-fusion-comp]].
