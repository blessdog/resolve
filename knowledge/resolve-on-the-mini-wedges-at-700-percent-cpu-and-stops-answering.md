---
id: resolve-on-the-mini-wedges-at-700-percent-cpu-and-stops-answering
kind: open
conflict-key: how-to-recover-a-resolve-that-has-stopped-answering-scripting
status: live
verified-on: 2026-09-21
supersedes: []
proven: false
asked-as:
  - Resolve is running but scriptapp returns None
  - Resolve on the mini will not quit
  - the mac mini stopped answering scripting mid-session
---

**Resolve Studio 21.1.0 on the Mac mini wedged at ~700% CPU for two hours after a scripted
render and stopped answering both `dvr.scriptapp("Resolve")` and AppleEvents. Recovery is
NOT established.**

Measured 2026-09-21. It had rendered correctly at 18:59 (the graded Speed Warp job, LUT
readback True). By 20:15 the same process, up 1 h 43, sat at 694-720% CPU holding
`~/render/timelapse/clip0003-4x-src.mp4` open, with:

- `dvr.scriptapp("Resolve")` → `False`, from the /Applications library AND from the running
  bundle's own library (the mini carries two 21.1.0 installs, one on `/Volumes/BleSSD`)
- `osascript ... to quit` → AppleEvent timed out (-1712), at both the default timeout and 300 s
- `open -a` → exits 0, changes nothing; only one instance runs
- `screencapture` over ssh → "could not create image from display"; `launchctl asuser` →
  "Could not switch to audit session"

`scripts/restart_resolve.py` stops exactly here by design, printing "did not exit within 60s
(dialog blocking?)". Whether a dialog is actually up is unknown — nothing over ssh can see the
mini's screen.

**This matters because it breaks the causal story in
[[resolve-only-reads-the-system-lut-folder-and-a-hard-kill-breaks-scripting]]**, which says a
`pkill` is what leaves Resolve "running but scriptapp returns None forever". This session
reached that identical state with **no kill of any kind**. So a hard kill is not NECESSARY to
produce it; that claim stays live (its LUT half is separately measured and its advice against
pkill costs nothing), but do not treat the kill as the explanation when this state appears.

**Untried, in order, next time:** force-quit from the mini's own keyboard (Cmd-Opt-Esc), then
relaunch headless with `Resolve -nogui` — the `--nogui` path `restart_resolve.py` already
implements, which needs no GUI login session and may be the right way to run the mini
permanently. Only if a human is not available: `kill -TERM`, accepting the risk the other claim
warns about.

Related: [[the-mac-mini-has-resolve-studio-and-renders-over-ssh]],
[[the-mini-must-pull-footage-the-macbook-cannot-push-it]].
