---
id: render-clip-0002-on-the-mac-mini-to-close-ryan-s
kind: open
conflict-key: should-we-render-clip-0002-on-the-mac-mini-to-close-ryan-s
status: live
supersedes: []
proven: false
verified-on: 2026-09-21
asked-as:
  - render clip 0002 on the Mac mini to close Ryan's 'render on the mini' directive
  - render clip 0002 on the mac mini to close ryan s
  - why is resolve_render.py, already shipped to mini like this
  - what is blocking render clip 0002 on the Mac mini to clos
---

**This is a PLAN, not a finding. `proven: false`. Do not build against it.**

## render clip 0002 on the Mac mini to close Ryan's 'render on the mini' directive

**Why it matters:** Ryan said it twice (2026-09-21) and the mini has rendered ZERO of the four ride clips. All of them were rendered on the MacBook because the mini's Resolve wedged at 700% CPU. The tool, the footage and the LUTs are all in place, so the only thing missing is proof the mini can do a 4K graded render end to end; without it the directive is open, not closed.

**Where it lands:** `tools/remote/resolve_render.py, already shipped to mini:render/resolve_render.py`

**First step:** ssh mini 'cd ~/render && /usr/bin/python3 resolve_render.py /Volumes/BleSSD/render/src/DJI_20260921184748_0002_D.MP4 /Volumes/BleSSD/render/out c0002-mini --size 3840x2160 --fps 25 --quality 80000 --project ride-mini-25 --lut "film-look/matched/match-fashion-hm-mkl-hm.cube"' then compare frame count (expect 21322) and a frame's channel means at 300 s against outputs/osmo/2026-09-21-ride/graded/c0002-matched100.mp4 (R63 G51 B37), and record the elapsed time against the MacBook's 244 s

**Blocked on:** Resolve on the mini must be force-quit from its own keyboard; it has ignored scriptapp, a 300 s AppleEvent quit and open -a for over two hours. Then relaunch headless with Resolve -nogui

Bookmarked 2026-09-21 at the moment of deferral, because the record of a deferral is what fails, not the decision to defer.
